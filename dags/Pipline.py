import requests
import json
from airflow import DAG
from datetime import datetime, timedelta
# Operators; we need this to operate!
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from helpers import happinessData
from helpers import countriesData
from helpers import lifeData
from helpers import integrateData


# step 2 - define default args
# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization

default_args = {
    'owner': 'gardel-el-data',
    'depends_on_past': False,
    'start_date': datetime(2020, 12, 26),
    'email_on_retry': False,
    # 'retries': 3,
    # 'retry_delay': timedelta(minutes=5),
}
# step 3 - instantiate DAG
dag = DAG(
    'Pipline',
    default_args=default_args,
    description='Transform data and prepare it for getting insights',
    schedule_interval='@once'
    
)

# step 4 Define tasks

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

end_operator = DummyOperator(task_id='end_execution',  dag=dag)

clean_happiness_data= PythonOperator(
    task_id='clean_happiness_data',
    provide_context=True,
    python_callable=happinessData.clean_data,
    dag=dag,
)

clean_countries_data= PythonOperator(
    task_id='clean_countries_data',
    provide_context=True,
    python_callable=countriesData.clean_data,
    dag=dag,
)
clean_life_data= PythonOperator(
    task_id='clean_life_data',
    provide_context=True,
    python_callable=lifeData.clean_data,
    dag=dag,
)
integrate_data= PythonOperator(
    task_id='integrate_data',
    provide_context=True,
    python_callable=integrateData.integrate_data,
    dag=dag,
)
# t2 = PythonOperator(
#     task_id='transform_data',
#     provide_context=True,
#     python_callable=happinessData.transform_data,
#     dag=dag,
# )

# step 5 - define dependencies
start_operator >> clean_happiness_data
clean_happiness_data >> clean_countries_data
clean_countries_data >> clean_life_data
clean_life_data >> integrate_data

integrate_data >> end_operator