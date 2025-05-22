import json
import argparse
import torch
import torch.distributed as dist
from vlmeval.dataset.mmereasoning import mmereasoning_utils
from vlmeval.smp import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Extracting and evaluating the MME-Reasoning")
    parser.add_argument('--file_path', type=str, help='Names of Datasets')
    args = parser.parse_args()

    load_env()
    judge_dict = {
        "model": "gpt-4o-mini",
        "nproc": 4
    }
    mmereasoning_utils.evaluate(args.file_path, **judge_dict)
