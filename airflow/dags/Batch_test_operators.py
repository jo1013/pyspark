from datetime import datetime


import pendulum
from airflow import models,DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from my_operators import MyFirstOperator
from datetime import datetime, timedelta

local_tz = pendulum.timezone("Asia/Seoul")


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2021, 7, 8, tzinfo=local_tz),
    'email': ['airflow@airflow.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)}


def sleep_seconds(seconds, **kwargs):
    print('=' * 60)
    print('seconds:' + str(seconds))
    print('=' * 60)
    pprint(kwargs)
    print('=' * 60)
    print('sleeping...')
    time.sleep(seconds)
    return 'sleep well!!!'

with models.DAG(
    dag_id='batch_test', description='two DAG',
#    schedule_interval='2021 07 08 15 15', tzinfo=KST)
    schedule_interval='15 16 0 * *',
    start_date=datetime(2017, 3, 20)) as dag:
    
    
    t3 = PythonOperator(task_id='pythonoperator',
                        provide_context=True,
                        python_callable=sleep_seconds,
                        op_kwargs={'seconds': 10},
                        dag=dag)
    


    dummy_task = DummyOperator(task_id='dummy_task', dag=dag)

    operator_task = MyFirstOperator(my_operator_param='This is a test.',
                                    task_id='my_first_operator_task', dag=dag)
    
    
    
    
    
    templated_command="""
        docker exec -it py_spark_air python3 /home/pyspark/batch_test.py
    """



    t1 = BashOperator(
            task_id='print_date',
            bash_command= templated_command,
            dag=dag)
 

    t3 >> t1 
    t3 >> dummy_task
    t1 >> operator_task
    dummy_task >> operator_task
