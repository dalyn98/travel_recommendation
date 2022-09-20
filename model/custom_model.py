#!/usr/bin/env python
# coding: utf-8

# In[1]:


import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset

import pandas as pd
from datetime import datetime


# In[2]:


class MyDataset(Dataset):
    def __init__(self,df):
        self.df = df
        self.data = self.df.iloc[:,:-1].values
        self.target = self.df.iloc[:,-1].values
    
    def __getitem__(self,index):
        self.x = self.data[index]
        self.y = self.target[index]
        
        return torch.Tensor(self.x), self.y
    def __len__(self):
        return len(self.df)


# In[3]:


class Net(nn.Module):

  def __init__(self):
    super(Net, self).__init__()
    self.fc1 = nn.Linear(13, 96)
    self.fc2 = nn.Linear(96, 3)
    
  def forward(self, x):
    x = F.relu(self.fc1(x))
    x = self.fc2(x)
    return F.log_softmax(x)


# In[93]:


class Trainer():
    def __init__(self,model,train_loader,epochs,criterion, optimizer):
        self.model = model
        self.train_loader = train_loader
        self.epochs = epochs
        self.criterion = criterion
        self.optimizer = optimizer
        
    def fit(self,re_train = False):
        for epoch in range(self.epochs):
            total_loss = 0
            
            for x,y in self.train_loader:
                self.optimizer.zero_grad()
                _x = self.model(x)
                loss = self.criterion(_x, y)
                loss.backward()
                self.optimizer.step()
                
                total_loss += loss.data.item()
                
            if (epoch + 1) % 50 == 0:
                print(epoch +1, total_loss)
        now = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
        if re_train == False:
            torch.save(self.model.state_dict(), './model/save_model/test_model'+now+'.pt')
        else:
            torch.save(self.model.state_dict(), './model/save_model/test_model'+now+'re_train.pt')

