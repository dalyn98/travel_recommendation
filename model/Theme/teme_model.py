#!/usr/bin/env python
# coding: utf-8

# In[223]:


import argparse
import compress_fasttext
from datetime import datetime
from konlpy.tag import Mecab
import pandas as pd
import numpy as np
import operator
import os
def get_config():
    parser = argparse.ArgumentParser()
    parser.add_argument('--df_path', type=str, default='',
                        help='df path, (default : X')

    args = parser.parse_args()
    return args

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)
        
class regist_teme:
    def __init__(self,args):
        try:
            self.df = pd.read_csv(args.df_path).drop('Unnamed: 0.1',axis=1).drop('Unnamed: 0',axis=1)
        except:
            pass
        self.tourism_list = list(pd.read_csv(args.df_path)['관광지소개'])
        self.tem = ['휴식','체험','문화','복합']
        self.wv = self.load_model() 
        self.mecab = Mecab()
        
    def load_model(self):
        print(f"== LOAD fasttext START at {datetime.now()}")
        wv = compress_fasttext.models.CompressedFastTextKeyedVectors.load(
            'cc.ko.300.small.bin'
        )
        print(f"== LOAD fasttext   END at {datetime.now()}")
        return wv
    def once_cosine(self,tourism_name):
        '''
        해당 단일 관굉지에 대한 유사도
        '''
        tourism_intro = self.df.loc[self.df['관광지명']==tourism_name]['관광지소개'].iloc[0]
        print(f'{tourism_name} : {tourism_intro}')
        cosine_list = self.cal_cosine(tourism_intro = tourism_intro)
        
        
        return cosine_list
    def cal_cosine(self,tourism_intro):
        nouns = self.mecab.nouns(tourism_intro)
        tem = self.tem
        temp = np.zeros(300)
        try:
            for em in self.wv[nouns]/5:
                temp = temp + em
        except:
            pass
        tem_dic ={}
        for t in tem:
            tem_dic[t] = self.wv[t]

        cosine_dict = {}
        for tem in tem_dic:
            cosine = self.wv.cosine_similarities(temp,tem_dic[tem].reshape(1,-1))
            print(f'{tem} : ',cosine)
            if np.isnan(cosine):
                cosine_dict[tem] = np.NaN
            else:
                cosine_dict[tem] = cosine
        return cosine_dict
    def regist_full_tem(self):
        temp_df = self.df.copy()
        for i in range(len(temp_df)):
            cosine_dict = self.once_cosine(temp_df.iloc[i]['관광지명'])
            max_by_value = max(cosine_dict.items(), key=operator.itemgetter(1))
            if np.isnan(max_by_value[1]):
                temp_df['테마'][i] = '없음'
            else:
                temp_df['테마'][i] = max_by_value[0]
            
        return temp_df


# In[224]:


if __name__ == '__main__':
    args = get_config()
    regist = regist_teme(args)
    df = regist.regist_full_tem()
    now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    createFolder('./regist_tem')
    df.to_csv('./regist_tem/regist_teme'+now+'.csv')


# In[218]:


# class regist_teme:
#     def __init__(self):
#         try:
#             self.df = pd.read_csv('data_0.1.csv').drop('Unnamed: 0.1',axis=1).drop('Unnamed: 0',axis=1)
#         except:
#             pass
#         self.tourism_list = list(pd.read_csv('data_0.1.csv')['관광지소개'])
#         self.tem = ['휴식','체험','문화','복합']
#         self.wv = self.load_model() 
#         self.mecab = Mecab()
        
#     def load_model(self):
#         print(f"== LOAD fasttext START at {datetime.datetime.now()}")
#         wv = compress_fasttext.models.CompressedFastTextKeyedVectors.load(
#             'cc.ko.300.small.bin'
#         )
#         print(f"== LOAD fasttext   END at {datetime.datetime.now()}")
#         return wv
#     def once_cosine(self,tourism_name):
#         '''
#         해당 단일 관굉지에 대한 유사도
#         '''
#         tourism_intro = df.loc[df['관광지명']==tourism_name]['관광지소개'].iloc[0]
#         print(f'{tourism_name} : {tourism_intro}')
#         cosine_list = self.cal_cosine(tourism_intro = tourism_intro)
        
        
#         return cosine_list
#     def cal_cosine(self,tourism_intro):
#         nouns = self.mecab.nouns(tourism_intro)
#         tem = self.tem
#         temp = np.zeros(300)
#         try:
#             for em in self.wv[nouns]/5:
#                 temp = temp + em
#         except:
#             pass
#         tem_dic ={}
#         for t in tem:
#             tem_dic[t] = self.wv[t]

#         cosine_dict = {}
#         for tem in tem_dic:
#             cosine = self.wv.cosine_similarities(temp,tem_dic[tem].reshape(1,-1))
#             print(f'{tem} : ',cosine)
#             if np.isnan(cosine):
#                 cosine_dict[tem] = np.NaN
#             else:
#                 cosine_dict[tem] = cosine
#         return cosine_dict
#     def regist_full_tem(self):
#         temp_df = self.df.copy()
#         for i in range(len(temp_df)):
#             cosine_dict = self.once_cosine(temp_df.iloc[i]['관광지명'])
#             max_by_value = max(cosine_dict.items(), key=operator.itemgetter(1))
#             if np.isnan(max_by_value[1]):
#                 temp_df['테마'][i] = '없음'
#             else:
#                 temp_df['테마'][i] = max_by_value[0]
            
#         return temp_df


# In[ ]:




