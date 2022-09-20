#!/usr/bin/env python
# coding: utf-8

# In[1]:


from datetime import timedelta

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator


# In[ ]:


with DAG(
    dag_id = 'retrain',
    description = 'Retrain Dag',
    start_date = days_ago(1),
    schedule_interval= ' 0 0 * * *',
    tags = ['my_dags']
)as dag:
    save_retrained_model = BashOperator(
        task_id = 'retrain',
        bash_command = 'python /workspace2/model/retrain.py',
        owner = 'hyunwoo',
        dag=dag
    )
    save_retrained_model

