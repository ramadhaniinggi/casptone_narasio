from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from faker import Faker
import random
import pandas as pd
import requests
import psql

def extrac():
    print('process extract')
    fake=Faker()

    # data = []
    # for i in range(10):
    #     data_tmp = {
    #         'nik': fake.random_int(min=20000, max=100000),
    #         'user_name':fake.name().lower(),
    #         'email': fake.email(),
    #         'user_address':fake.street_address() + ' | ' + fake.city() + ' | ' + fake.country_code(),
    #         'platform': random.choice(['Mobile', 'Laptop', 'Tablet']),
    #         'signup_at': str(fake.date_time_this_month())    
    #         }
        
    #     data.append(data_tmp)
    data = requests.get("link")
    df = pd.DataFrame(data)
    df['date'] = datetime.now().strftime('YYYY-mm-dd')
    df.to_csv('result.csv')

def read_and_load():
    data = pd.read_csv("")
    psql.load(host, db_name, passwro)

def transform():
    a = 2
    print(a = 3)

def load_spreadsheet(SCOPES,SPREADSHEET_ID,DATA_TO_PULL):
    creds = gsheet_api_check(SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=DATA_TO_PULL).execute()
    values = result.get('values', [])
    
    if not values:
        print('No data found.')
    else:
        rows = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                  range=DATA_TO_PULL).execute()
        data = rows.get('values')
        print("COMPLETE: Data copied")
        return data

default_args = {
    'start_date':datetime(2022,1,1),
    'depends_on_past' : True,
    'wait_for_downstream' : False,
    'retries':5,
    'retry_delay' : timedelta(minutes=5),
}

with DAG(dag_id="hello_world_dag", default_args=default_args, 
    schedule_interval="@daily", catchup=False, tags=['main_productions']) as dag:

    # start = BashOperator(
    #     task_id="start_run",
    #     bash_command='echo start')
    task_extrac = PythonOperator(
        task_id="extrac",
        python_callable=extrac)

    task_load = PythonOperator(
        task_id="read_and_load",
        python_callable=read_and_load)
    
    task_extrac >> task_load

    # task_transform = PythonOperator(
    #     task_id="task_transform",
    #     python_callable=transform)

    # task_hello = PythonOperator(
    #     task_id="hello_world_task",
    #     python_callable=helloWorld)

    # end = BashOperator(
    #     task_id="end_run",
    #     bash_command='echo end')

    # start >> task_extrac >> [task_transform , task_hello] >> end

