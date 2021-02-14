import sys
import airflow
from airflow import DAG
from datetime import timedelta
from airflow.providers.google.cloud.operators import dataproc

airflow_home = "/home/airflow/gcs/dags/"
sys.path.append(airflow_home)

dataproc_region = 'northamerica-northeast1'
PROJECT_ID = "rich-karma-007"
CLUSTER_NAME = "dataproc-clean-data"

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('dag_dataproc_data_cleaner_operator',
          default_args=default_args,
          start_date=airflow.utils.dates.days_ago(1),
          catchup=False,
          schedule_interval=None)

create_cluster = dataproc.DataprocCreateClusterOperator(
    task_id="create_cluster",
    cluster_name=CLUSTER_NAME,
    project_id=PROJECT_ID,
    num_workers=2,
    image_version='1.4',
    master_machine_type='n1-standard-4',
    master_disk_size=200,
    worker_machine_type='n1-standard-4',
    worker_disk_size=200,
    region=dataproc_region,
    dag=dag)

submit_pyspark_job = dataproc.DataprocSubmitPySparkJobOperator(
    task_id="submit_pyspark_job",
    cluster_name=CLUSTER_NAME,
    project_id=PROJECT_ID,
    main="gs://rick_karma_pyspark/data_cleaner.py",
    pyfiles=["gs://rick_karma_pyspark/artifacts.zip"],
    job_name="dataproc-cleanup-job",
    arguments=["--should_prefix_partition=0",
               "--current_timestamp=1606507200",
               "--skip_last_n_hours=3",
               "--input_data_range_in_hours=5",
               "--raw_data_bucket_name=rich_karma_input",
               "--raw_data_bucket_key=py_spark_data",
               "--anonymized_data_bucket_name=rick_karma_pyspark_out",
               "--anonymized_data_bucket_key=anonymized_data",
               "--anonymized_data_column_name=zip"],
    region=dataproc_region,
    dag=dag)


delete_dataproc_cluster = dataproc.DataprocDeleteClusterOperator(
    task_id="delete-dataproc-cluster",
    cluster_name=CLUSTER_NAME,
    project_id=PROJECT_ID,
    region=dataproc_region,
    trigger_rule='all_done',
    dag=dag)


create_cluster >> submit_pyspark_job >> delete_dataproc_cluster

