#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import torch
import numpy as np
from kobert import get_tokenizer
from kobert import get_pytorch_kobert_model
import gluonnlp as nlp
from torch.utils.data import Dataset, DataLoader
from tqdm import tqdm


# In[27]:


class data2txt():
    def pd2txt(path):
        tsv = pd.read_csv(path).drop('Unnamed: 0',axis=1)
        path = './temp.txt'
        with open(path,'w',encoding='UTF-8') as f:
            for name in list(tsv['관광지소개']):
                f.write(name+'\n')
        print('pd2txt done')
        return path
    def word2txt(word_list):
        path = './temp.txt'
        with open(path,'w',encoding='UTF-8') as f:
            for name in word_list:
                f.write(name+'\n')
        print('word2txt done')
        return path


# In[28]:


class BERTDataset(Dataset):
    def __init__(self, dataset, sent_idx, bert_tokenizer, max_len,
                 pad, pair):
        transform = nlp.data.BERTSentenceTransform(
            bert_tokenizer, max_seq_length=max_len, pad=pad, pair=pair)

        self.sentences = [transform([i[sent_idx]]) for i in dataset]
        self.dataset = dataset

    def __getitem__(self, i):
        return self.sentences[i]

    def __len__(self):
        return (len(self.dataset))


# In[29]:


class Custom_Bert():
    def __init__(self,df_path = None,word_list = None):
        self.word_list = word_list
        self.df_path = df_path
        
    def config(self,txt_path):
        self.model, vocab = get_pytorch_kobert_model(cachedir=".cache")
        tokenizer = get_tokenizer()
        tok = nlp.data.BERTSPTokenizer(tokenizer, vocab, lower=False)

        tsv_txt = nlp.data.TSVDataset(txt_path,field_indices=[0])
        return tsv_txt,tok
    
    def BertDL(self,tsv,sent_idx,bert_tokenizer,max_len,pad,pair):
        dataset = BERTDataset(tsv,sent_idx,bert_tokenizer,max_len,pad,pair)
        DL = torch.utils.data.DataLoader(dataset,batch_size = 1)

        return DL
    
    def gen_attention_mask(self,token_ids, valid_length):
        attention_mask = torch.zeros_like(token_ids)
        for i, v in enumerate(valid_length):
            attention_mask[i][:v] = 1
        return attention_mask.float()
    
    def get_vector(self,DL):
        device = torch.device("cpu")
        embed_layer = torch.empty([1,768])
        for input_ids,valid_length,token_type_ids  in tqdm(DL):
            input_ids = input_ids.long().to(device)
            input_mask = self.gen_attention_mask(input_ids,valid_length).long().to(device)
            _,pooled_output = self.model(input_ids,input_mask,token_type_ids)
            embed_layer = torch.cat([embed_layer,pooled_output])
        return embed_layer
    
    def get_df_vector(self):
        path = data2txt.pd2txt(self.df_path)
        tsv,tok = self.config(path)
        DL = self.BertDL(tsv,0,tok,15,True,False)
        embed_layer = self.get_vector(DL)
        return embed_layer
    
    def get_word_vector(self):
        path = data2txt.word2txt(self.word_list)
        tsv,tok = self.config(path)
        DL = self.BertDL(tsv,0,tok,15,True,False)
        embed_layer = self.get_vector(DL)
        return embed_layer


# In[30]:


# word = ['휴식','체험','문화','복합']
# bert_config = Custom_Bert(word_list = word)
# bert_config = Custom_Bert(df_path = '../tourismData.csv')


# In[31]:


# embed_layer = bert_config.get_df_vector()


# In[ ]:




