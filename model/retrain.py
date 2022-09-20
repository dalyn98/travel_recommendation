#!/usr/bin/env python
# coding: utf-8

# In[1]:


'''
데이터를 불러와서 -> 기존 모델을 가져온뒤 -> 학습 -> 다시 업로드
'''


# In[1]:


import pandas as pd
import numpy as np
import random
import os

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import argparse
import custom_model
import model_setting
import test_train


# In[3]:


def get_config():
    
    train_parser = test_train.get_config(re_train = True)
    retrain_parser = argparse.ArgumentParser(parents = [train_parser])
    
    retrain_parser.add_argument('--model_path', type = str, default = './model/save_model/',
                       help = 'Load model path (default : ./model/save_model/)')
    retrain_parser.add_argument('--retrain_path', type = str , default = '../data/',
                       help = 'retrain csv path (default : ../data/)')
    
    args = retrain_parser.parse_args()
    
    return args


if __name__ == '__main__' :
    args = get_config()
    
    setting = model_setting.setting(args)
    #model = setting['model'].load_state_dict(torch.load(args.model_path + args.model_name),strict=False)
    model = setting['model']
    model.load_state_dict(torch.load(args.model_path + args.model_name),strict=False)
    train = custom_model.Trainer(model = model,
                                train_loader = setting['loader'],
                                epochs = args.epochs,
                                criterion = setting['criterion'],
                                optimizer = setting['optimizer'])
    print('setting complete')
    train.fit()


# In[ ]:




