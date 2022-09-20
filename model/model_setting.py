#!/usr/bin/env python
# coding: utf-8

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


# In[3]:


def seed_everything(seed):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = True

def seed_setting(args):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    seed_everything(args.seed)
    print('seed setting complete')
    
def dataset_setting(args):
    df = pd.read_csv(args.train_path + 'train_wine.csv').drop('Unnamed: 0',axis=1)
    train_dataset = custom_model.MyDataset(df = df)
    train_loader = DataLoader(train_dataset, batch_size = args.batch_size, shuffle = True)
    print('dataset setting complete')
    
    return {'df' : df,
           'dataset' : train_dataset,
           'loader' : train_loader}
def model_setting(args,set_dict):
    model = custom_model.Net()
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=args.lr)
    train = custom_model.Trainer(model = model,
                                train_loader = set_dict['loader'],
                                epochs = args.epochs,
                                criterion = criterion,
                                optimizer = optimizer)
    set_dict['model'] = model
    set_dict['criterion'] = criterion
    set_dict['optimizer'] = optimizer
    set_dict['train'] = train    
    return set_dict
    
def setting(args):
    save_dir = args.save_dir
    
#     device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
#     seed_everything(args.seed)
#     print('seed setting complete')
    
#     df = pd.read_csv(args.train_path + 'train_wine.csv').drop('Unnamed: 0',axis=1)
#     train_dataset = custom_model.MyDataset(df = df)
#     train_loader = DataLoader(train_dataset, batch_size = args.batch_size, shuffle = True)
#     print('dataset setting complete')
    
#     model = custom_model.Net()
#     criterion = nn.CrossEntropyLoss()
#     optimizer = optim.SGD(model.parameters(), lr=args.lr)
#     train = custom_model.Trainer(model = model,
#                                 train_loader = train_loader,
#                                 epochs = args.epochs,
#                                 criterion = criterion,
#                                 optimizer = optimizer)
#     print('model setting complete')
    seed_setting(args)
    
    set_dict = dataset_setting(args)
    set_dict = model_setting(args,set_dict)
    set_dict['save_dir'] = save_dir
    
    return set_dict


# In[ ]:




