import os.path as osp
from ...smp import *
from ...utils import can_infer, track_progress_rich
from ..utils import build_judge
from .function4eval import functions as mmereasoning_eval_functions
from .prompts4eval import prompts as mmereasoning_eval_prompts
import json
import pandas as pd
import re
import math

FAIL_MSG = 'Failed to obtain answer via API.'

def extract_json_from_markdown(text):
    pattern = r'```json\s*(.*?)\s*```'
    match = re.search(pattern, text, re.DOTALL)
    
    if match:
        json_str = match.group(1)
        return json_str
    else:
        return None

def extract_json_from_markdown_1(text):
    pattern = r'```\s*(.*?)\s*```'
    match = re.search(pattern, text, re.DOTALL)
    
    if match:
        json_str = match.group(1)
        return json_str
    else:
        return None

def extract_json_from_markdown_2(text):
    pattern = r'```JSON\s*(.*?)\s*```'
    match = re.search(pattern, text, re.DOTALL)
    
    if match:
        json_str = match.group(1)
        return json_str
    else:
        return None

def MMEReasoning_extract(model, line):
    res = None
    question = line['question']
    ans = line['answer']
    response = line['prediction']
    eval_function = line['function_id']
    eval_prompt = line['prompt_id']
    if eval_function == None:
        if line['question_type'].lower() == 'choice':
            eval_prompt, eval_function = 'choice_prompt', 'choice_function'
        elif line['question_type'].lower() == 'open':
            eval_prompt, eval_function = 'open_question_prompt', 'open_function'
        else:
            raise NotADirectoryError(f"Question type that requires specifying the function_id: {line['question_type']}")

    prompt = mmereasoning_eval_prompts[eval_prompt].format(question=question, response=response)
    log = ''
    retry = 5

    for i in range(retry):
        prediction = line['prediction']
        if prediction == FAIL_MSG:
            log += f'Try {i}: output is {prediction}, failed to parse.\n'
            return dict(log=log, res='')
        res = model.generate(prompt, temperature=i * 0.5)
        if eval_prompt not in ['open_question_prompt', 'choice_prompt', 'points24_prompt']:
            try:
                json.loads(res)
            except:
                try: 
                    json.loads(extract_json_from_markdown(res))
                    res = extract_json_from_markdown(res)
                except:
                    try:
                        json.loads(extract_json_from_markdown_1(res))
                        res = extract_json_from_markdown_1(res)
                    except:
                        try:
                            json.loads(extract_json_from_markdown_2(res))
                            res = extract_json_from_markdown_2(res)
                        except:
                            continue

        if FAIL_MSG in res:
            log += f'Try {i}: output is {prediction}, failed to parse.\n'
        else:
            log += 'Succeed'
            return dict(log=log, res=res)
    log += 'All 5 retries failed.\n'
    return dict(log=log, res='')

def MMEReasoning_openeval(model, line):
    prompt_openeval = """
Please read the following example. Then judge the answer and type it at the end of the prompt.
Below are two examples. Question is [Question], [Standard Answer] is the standard answer to the question, and [Model_answer] is the answer extracted from a model's output to this question.  Determine whether these two answers are consistent.
Note:
    Different expressions of the same number should also be considered consistent, for example, \\frac{{7}}{{2}} and 3.5.
    If a conversion results in a decimal approximation, the expressions can be considered consistent if the values are equal up to two decimal places, for example, \\sqrt{{3}} and 1.73.
If they are consistent, Judgement is 1; if they are different, Judgement is 0.\n
Example 1: 
    [Question]: What is the minimize length of the line?
    [Standard answer]: \\sqrt{{2}}
    [Model answer]: 1.414
    [Judgement]: 1
Example 2:
    [Question]: Given an image of a 3x3 maze. How to reach the end cell marked 'E' from the start cell is marked 'S'.
    [Standard answer]: ['Left', 'Right']
    [Model answer]: 'Left', 'Right' 
    [Judgement]: 1

Now, judge the anwser for the following question:
    [Question]: {question}
    [Standard answer]: {answer}
    [Model answer]: {response}
    [Judgement]: 
You should only output the judgement without any other texts.
"""
    log = ''
    retry = 5
    prompt = prompt_openeval.format(question=line['question'], answer=line['answer'], response=line['res'])
    for i in range(retry):
        try:
            prediction = line['res']
            if prediction == None or FAIL_MSG in prediction:
                log += f'Try {i}: output is {prediction}, failed to parse.\n'
                return dict(log_score=log, score=False)
            res = model.generate(prompt, temperature=i * 0.5)
            if FAIL_MSG in res or res.strip() not in ['0', '1']:
                log += f'Try {i}: output is {prediction}, res is {res}, failed to parse.\n'
            else:
                log += 'Succeed'
                return dict(log_score=log, score=int(res) == 1)
        except:
            continue
    log += 'All 5 retries failed.\n'
    return dict(log_score=log, score=False)


def MMEReasoning_acc(result_file):
    df = load(result_file)

    capabilities = ['planning and exploring', 'calculation', 'spatial-temporal', 'casual chaining analysis', 'pattern analysis']
    reasoning_types = ['inductive', 'deductive', 'abductive']

    res = defaultdict(list)

    # Overall Acc
    res['Overall'].append(np.mean(df['score']) * 100)
    for capability in capabilities:
        sub = df[df['capability'].apply(lambda x: capability in x)]
        res[capability].append(np.mean(sub['score']) * 100)
    
    for r_type in reasoning_types:
        sub = df[df['reasoning_type'].apply(lambda x: r_type in x)]
        res[r_type].append(np.mean(sub['score']) * 100)

    return pd.DataFrame(res)


def evaluate(eval_file, **judge_kwargs):
    model = judge_kwargs['model']
    suffix = eval_file.split('.')[-1]
    storage_extract = eval_file.replace(f'.{suffix}', f'_{model}_extract.xlsx')
    tmp_file_extract = eval_file.replace(f'.{suffix}', f'_{model}_extract.pkl')
    nproc = judge_kwargs.pop('nproc', 4)

    # stage 1: extract answers using LLM
    if not osp.exists(storage_extract):
        data = load(eval_file)
        data = data.replace({float('nan'): None})
        model = build_judge(max_tokens=1024, **judge_kwargs)
        assert model.working(), ('MMEReasoning evaluation requires a working OPENAI API\n')
        lt = len(data)
        lines = [data.iloc[i] for i in range(lt)]
        tups = [(model, line) for line in lines]
        indices = [line['index'] for line in lines]

        ans = {}
        if osp.exists(tmp_file_extract):
            ans = load(tmp_file_extract)
        tups = [x for x, i in zip(tups, indices) if i not in ans]
        indices = [i for i in indices if i not in ans]
        if len(indices):
            new_results = track_progress_rich(
                MMEReasoning_extract,
                tups,
                nproc=nproc,
                chunksize=nproc,
                keys=indices,
                save=tmp_file_extract,
            )
            ans = load(tmp_file_extract)
            for k, v in zip(indices, new_results):
                assert k in ans
                assert ans[k]['log'] == v['log'] and ans[k]['res'] == v['res']
        
        res_list = []
        log_list = []
        for idx in data['index']:
            if not isinstance(ans[idx], dict):
                res_list.append(ans[idx])
                log_list.append('use previous answer')
            else:
                res_list.append(ans[idx]['res'])
                log_list.append(ans[idx]['log'])
        data['res'] = res_list
        data['log'] = log_list
        dump(data, storage_extract)
    
    storage_score = eval_file.replace(f'.{suffix}', f'_{model}_score.xlsx')
    tmp_file_score = eval_file.replace(f'.{suffix}', f'_{model}_score.pkl')
        
    # stage 2: evaluate score
    if not osp.exists(storage_score):
        data = load(storage_extract)
        data = data.replace({float('nan'): None})
        model = build_judge(max_token=1024, **judge_kwargs)
        assert model.working(), ('MMEReasoning evaluation requires a working OPENAI API\n')
        lt = len(data)
        lines = [data.iloc[i] for i in range(lt)]
        lines_scores_gpt = []
        lines_scores_other = []
        for line in lines:
            if (line['question_type'].lower() == 'open' and line.get('function_id', None) == None) or line.get('function_id', None) == 'open_function':
                lines_scores_gpt.append(line)
            else:
                lines_scores_other.append(line)
        
        # for open question, use LLM     
        tups_scores_gpt = [(model, line) for line in lines_scores_gpt]
        indices_scores_gpt = [line['index'] for line in lines_scores_gpt]
        if len(indices_scores_gpt):
            new_results_score = track_progress_rich(
                MMEReasoning_openeval,
                tups_scores_gpt,
                nproc=nproc,
                chunksize=nproc,
                keys=indices_scores_gpt,
                save=tmp_file_score,
            )
            ans = load(tmp_file_score)
            for k, v in zip(indices_scores_gpt, new_results_score):
                assert k in ans
                assert ans[k]['log_score'] == v['log_score'] and ans[k]['score'] == v['score']

        # for other questions, use corresponding function
        res = {}
        indices_scores_other = [line['index'] for line in lines_scores_other]
        for k, line in zip(indices_scores_other, lines_scores_other):
            if line['res'] == None or FAIL_MSG in line['res']:
                log_score = f'Failed to evaluate'
                res.update({
                    k: {
                        "log_score": log_score,
                        "score": False
                    }
                })
                continue

            if line['function_id'] == None:
                assert line['question_type'].lower() == 'choice'
                function_id = 'choice_function'
                function = mmereasoning_eval_functions[function_id]
                
            else:
                function_id = line['function_id']
                function = mmereasoning_eval_functions[function_id]
            
            if function_id not in ['open_function', 'choice_function']:
                if function_id == "judge_24points_function":
                    response = line['res']
                else:
                    response = json.loads(line['res'])
                if line['answer'] != None:
                    answer = eval(line['answer'])
                else:
                    answer = None

                if function_id in [
                    "calculate_answer_function_hashi",
                    "calculate_answer_function_skyscraper",
                    "calculate_answer_function_sudoku_4", 
                    "calculate_answer_function_sudoku_6",
                    "calculate_answer_function_yinyang",
                    "judge_24points_function"
                    ]:
                    assert line["special_info"] is not None
                    special_info = eval(line['special_info'])
                else:
                    special_info = None

            else:
                response = line['res']
                answer = line['answer']
                special_info = None

            if special_info is None:
                answer_judge = function(response, answer)
            else:
                answer_judge = function(response, answer, special_info)

            if answer_judge not in [True, False]:
                log_score = 'Failed to evaluate'
                score = False
            else:
                log_score = 'Succeed'
                score = answer_judge    
            res.update({
                k: {
                    "log_score": log_score,
                    "score": score
                }
            })
        
        ans.update(res) 
        data['score'] = [ans[idx]['score'] for idx in data['index']]
        data['log_score'] = [ans[idx]['log_score'] for idx in data['index']]
        dump(data, storage_score)
    
    score = MMEReasoning_acc(storage_score)
    score_pth = storage_score.replace('.xlsx', '.csv')
    dump(score, score_pth)
    return score    


if __name__ == "__main__":
    model = build_judge(max_tokens=128, **judge_kwargs)
    evaluate("/fs-computility/MA4Tool/yuanjiakang/code/MM-Reasoning-Bench/VLMEvalKit/outputs/InternVL3-38B/T20250509_Gb643eed3/InternVL3-38B_MMELogicBench.xlsx")