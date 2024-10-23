from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner' : 'airscholar',
    'start_date' : datetime(2024, 10, 22, 10, 00)
}

def stream_data():
    import json
    import requests
    requests.get()
with DAG('user_automation',
         default_args = default_args,
         schedule_interval = '@daily',
         catchup = False) as dag :
    streaming_task = PythonOperator(
        task_id = 'stream_data_from_api'
        python_callable = stream_data
    )