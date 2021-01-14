import requests
import json
from airflow import DAG
from datetime import datetime, timedelta
# Operators; we need this to operate!
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from helpers import Sentiment



# step 2 - define default args
# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
# today=datetime.today().strftime("%d/%m/%Y")
default_args = {
    'owner': 'gardel-el-data',
    'depends_on_past': False,
    'start_date': datetime(2021, 1, 10),
    'email_on_retry': False,

}
# step 3 - instantiate DAG
dag = DAG(
    'Twitter_Pipline',
    default_args=default_args,
    description='Gathering tweets and perfome sentimate analysis',
    schedule_interval='@daily'
    
)

# step 4 Define tasks

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

end_operator = DummyOperator(task_id='end_execution',  dag=dag)

FinlandDailyScore= PythonOperator(
    task_id='FinlandDailyScore',
    provide_context=True,
    python_callable=Sentiment.TwitterPipline,
    op_kwargs={ 'country': 'Finland'},
    dag=dag,
)

KenyaDailyScore= PythonOperator(
    task_id='KenyaDailyScore',
    provide_context=True,
    python_callable=Sentiment.TwitterPipline,
    op_kwargs={'country': 'Kenya'},
    dag=dag,
)
start_operator >> FinlandDailyScore
FinlandDailyScore >> KenyaDailyScore
KenyaDailyScore >> end_operator