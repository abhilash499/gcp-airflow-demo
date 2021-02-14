from datetime import timedelta
from airflow import DAG
import sys
import airflow
from airflow.operators.bash_operator import BashOperator

airflow_home = "/home/airflow/gcs/dags/"
sys.path.append(airflow_home)

template_path = airflow_home + '/workflow/workflow_data_cleaner.yaml'
dataproc_region = 'northamerica-northeast1'


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}


dag = DAG('dag_dataproc_data_cleaner_workflow',
          default_args=default_args,
          start_date=airflow.utils.dates.days_ago(1),
          catchup=False,
          schedule_interval=None)


task = BashOperator(
    task_id='test',
    bash_command='gcloud dataproc workflow-templates instantiate-from-file --file={{ template }}  --region={{ region }}',
    env={'template': template_path, 'region': dataproc_region},
    dag=dag
)
