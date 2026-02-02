from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
import sys
import os

# Add ingestion script path
sys.path.append("/opt/airflow/api-request")

# Import the ingestion function
try:
    from insert_record import main as ingest_main
except ImportError:
    def ingest_main():
        print("Error: Could not import insert_record. Check volume mounts.")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    dag_id='weather_api__dbt_orchestrator',
    default_args=default_args,
    description='Orchestrator DAG for Weather ETL',
    # Changed to daily as per user request
    schedule_interval='@daily',
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['weather', 'etl'],
)

with dag:
    # Task 1: Ingest data using PythonOperator (runs inside Airflow container)
    task1 = PythonOperator(
        task_id='ingest_weather_data',
        python_callable=ingest_main,
    )

    # Task 2: Run dbt using a simple docker exec command 
    # (Since we have the docker socket, we can tell the dbt container to run)
    task2 = BashOperator(
        task_id='transform_data_task',
        bash_command='docker exec dbt_container dbt run --project-dir /usr/app/dbt/weather_project --profiles-dir /usr/app/dbt',
    )

    task1 >> task2