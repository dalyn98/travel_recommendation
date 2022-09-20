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
import model_setting


# In[2]:


# def get_config():
#     parser = argparse.ArgumentParser()
    
#     '''path, model option'''
#     parser.add_argument('--seed', type = int, default= 42,
#                        help = 'random seed (default:42)')
#     parser.add_argument('--save_dir', type = str , default = '/workspace2/model/save_model/',
#                        help = 'model save dir path (default : /workspace2/model/save_model/)')
#     parser.add_argument('--train_path', type = str , default = '/workspace2/data/',
#                        help = 'train csv path (default : /workspace2/data/)')
#     parser.add_argument('--save_model_name', type = str, default = 'test_model.pt',
#                        help = 'model type (default : test_model.pt)')
    
    
    
#     ''' hyperparameter '''
#     parser.add_argument('--epochs', type = int, default = 100,
#                        help = 'number of epohcs train (default : 100)')
#     parser.add_argument('--lr', type = float, default = 1e-5,
#                        help = 'learning rate (default : 1e-5)')
#     parser.add_argument('--batch_size', type = int, default = 32,
#                        help = 'input batch size for training (default : 32)')
#     args = parser.parse_args()
    
#     return args

# def seed_everything(seed):
#     random.seed(seed)
#     os.environ['PYTHONHASHSEED'] = str(seed)
#     np.random.seed(seed)
#     torch.manual_seed(seed)
#     torch.cuda.manual_seed(seed)
#     torch.backends.cudnn.deterministic = True
#     torch.backends.cudnn.benchmark = True 
    
# if __name__ == "__main__":
    
#     args = get_config()
#     save_dir = args.save_dir
    
#     device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#     seed_everything(args.seed)
#     print('seed seting complete')
    
#     df = pd.read_csv(args.train_path + 'train_wine.csv').drop('Unnamed: 0',axis=1)
#     train_dataset = custom_model.MyDataset(df = df)
#     train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True)
#     print('dataset seting complete')
    
#     model = custom_model.Net()
#     criterion = nn.CrossEntropyLoss()
#     optimizer = optim.SGD(model.parameters(), lr=args.lr)
#     #model.load_state_dict(torch.load(args.save_dir + args.save_model_name))
#     train = custom_model.Trainer(model = model,
#                                 train_loader = train_loader,
#                                 epochs = args.epochs,
#                                 criterion = criterion,
#                                 optimizer = optimizer)
#     print('model load complete')
#     train.fit()


# In[ ]:


def get_config(re_train = False):
    parser = argparse.ArgumentParser(add_help = False)
    
    '''path, model option'''
    parser.add_argument('--seed', type = int, default= 42,
                       help = 'random seed (default:42)')
    parser.add_argument('--save_dir', type = str , default = './model/save_model/',
                       help = 'model save dir path (default : ./model/save_model/)')
    parser.add_argument('--train_path', type = str , default = '/workspace2/data/',
                       help = 'train csv path (default : ../data/)')
    parser.add_argument('--model_name', type = str, default = 'test_model.pt',
                       help = 'model type (default : test_model.pt)')
    
    
    
    ''' hyperparameter '''
    parser.add_argument('--epochs', type = int, default = 100,
                       help = 'number of epohcs train (default : 100)')
    parser.add_argument('--lr', type = float, default = 1e-5,
                       help = 'learning rate (default : 1e-5)')
    parser.add_argument('--batch_size', type = int, default = 32,
                       help = 'input batch size for training (default : 32)')
    if re_train == False:
        args = parser.parse_args()
        return {'args' : args,
               'parser' : parser}
    else:
        return parser
if __name__ == '__main__':
    args = get_config()
    
    setting = model_setting.setting(args['args'])
    train = setting['train']
    train.fit()


# In[ ]:




