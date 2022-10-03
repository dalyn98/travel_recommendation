#!/usr/bin/env python
# coding: utf-8

# In[1]:


from utils import bert_config
import argparse


# In[ ]:


def args_config():
    parser = argparse.ArgumentParser()
    parser.add_argument('--df_path',type = str, default=None,
                       help = 'Enter data if df(default = None)')
    parser.add_argument('--word_list',nargs='+', type = str, default = None,
                       help = 'Function for theme classification, data must be word_list(default=None) \
                            input ex : 휴식 체험')
    
    args = parser.parse_args()
    
    return args


# In[ ]:


if __name__ == '__main__':
    args = args_config()
    # 데이터가 df 일 경우
    if args.df_path != None:
        embed_bert = bert_config.Custom_Bert(df_path = args.df_path)
        embed_layer = embed_bert.get_df_vector()
        print('df embeding done')
        
    elif args.word_list != None:
        print(args.word_list)
        embed_bert = bert_config.Custom_Bert(word_list = args.word_list)
        embed_layer = embed_bert.get_word_vector()
        print('word embeding done')


# In[ ]:




