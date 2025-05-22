# from vlmeval import *
import json
import pandas as pd
from ...smp import *

def toliststr(s):
    if isinstance(s, str) and (s[0] == '[') and (s[-1] == ']'):
        return [str(x) for x in eval(s)]
    elif isinstance(s, str):
        return [s]
    elif isinstance(s, list):
        return [str(x) for x in s]
    raise NotImplementedError

class MMEReasoning():

    MODALITY = "Image"
    TYPE = 'VQA'
    DATASET_URL = {'MMEReasoning': ''}
    def __init__(self, dataset='MMEReasoning', **kwargs):
        ROOT = LMUDataRoot()
        self.dataset_name = dataset
        self.img_root = osp.join(ROOT, 'images', 'MMEReasoning')

        data_path = ""
        data = self.load_tsv(data_path)
        data = data.rename(columns={'image':'image_path'})
        self.data = data
        self.meta_only = True
        self.use_cot = kwargs.get('use_cot', False)

    def build_prompt(self, line):
        if isinstance(line, int):
            line = self.data.iloc[line]
        
        tgt_path = toliststr(line['image_path'])
        question = line['question']
        if self.use_cot:
            question += " Let's think step-by-step."
        msgs = []
        if isinstance(tgt_path, list):
            msgs.extend([dict(type='image', value=p) for p in tgt_path])
        else:
            msgs = [dict(type='image', value=tgt_path)]
        msgs.append(dict(type='text', value=question))
        return msgs
    
    def dump_image(self, line):
        os.makedirs(self.img_root, exist_ok=True)

        if 'image' in line:
            if isinstance(line['image'], list):
                tgt_path = []
                assert 'image_path' in line
                for img, im_name in zip(line['image'], line['image_path']):
                    path = osp.join(self.img_root, im_name)
                    if not read_ok(path):
                        decode_base64_to_image_file(img, path)
                    tgt_path.append(path)
            else:
                tgt_path = osp.join(self.img_root, f"{line['index']}.jpg")
                if not read_ok(tgt_path):
                    decode_base64_to_image_file(line['image'], tgt_path)
                tgt_path = [tgt_path]
        else:
            assert 'image_path' in line
            if isinstance(line['image_path'], str):
                if not os.path.exists(line['image_path']):
                    tgt_path = os.path.join(self.img_root, line['image_path'])
                else:
                    tgt_path = line['image_path']
            else:
                tgt_path = []
                for img in line['image_path']:
                    if not os.path.exists(img):
                        tgt_path.append(os.path.join(self.img_root, line['image_path']))
                    else:
                        tgt_path.append(img)
            tgt_path = toliststr(tgt_path)

        return tgt_path
    
    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return dict(self.data.iloc[idx])

    @classmethod
    def supported_datasets(cls):
        return list(cls.DATASET_URL)
    
    @staticmethod
    def load_tsv(f):
        return pd.read_csv(f, sep='\t')
        

if __name__ == "__main__":
    df = pd.read_json("/fs-computility/MA4Tool/yuanjiakang/code/MM-Reasoning-Bench/data_version_25_04_28/mmelogic_4_30_refine_2.json")
    df.to_csv("/fs-computility/MA4Tool/yuanjiakang/code/MM-Reasoning-Bench/data_version_25_04_28/mmelogic_4_30_refine_2.tsv", sep='\t', index=False, header=True)
    df = pd.read_csv("/fs-computility/MA4Tool/yuanjiakang/code/MM-Reasoning-Bench/data_version_25_04_28/mmelogic_4_30_refine_2.tsv", sep='\t')
    print(df.iloc[0])
