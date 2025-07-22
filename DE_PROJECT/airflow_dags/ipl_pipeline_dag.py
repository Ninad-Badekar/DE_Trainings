from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
import posthog

posthog.api_key = os.getenv("POSTHOG_API_KEY")
posthog.host = os.getenv("POSTHOG_HOST", "https://app.posthog.com")

def track_event(stage, status):
    posthog.capture(
        distinct_id="ipl_etl_pipeline",
        event=f"{stage} - {status}",
        properties={"stage": stage, "status": status, "timestamp": str(datetime.utcnow())}
    )

def track_success(stage, **kwargs):
    track_event(stage, "success")

def track_failure(context):
    task = context['task_instance']
    stage = task.task_id
    track_event(stage, "failure")

default_args = {
    'owner': 'ninad',
    'start_date': datetime(2025, 7, 21),
    'retries': 0,
    'on_failure_callback': track_failure,
}

dag = DAG(
    'ipl_etl_pipeline',
    default_args=default_args,
    description='ETL pipeline for IPL data',
    schedule_interval=None,
    catchup=False,
)

bronze_ingestion = BashOperator(
    task_id='bronze_ingestion',
    bash_command="""
    docker exec spark-master python3 /opt/spark-apps/bronze_ingestion.py \
    jdbc:mysql://mysql_source:3306/ipl_daily_db \
    ipl_user \
    ipl_password \
    deliveries \
    /opt/data_lake/bronze
    """,
    dag=dag,
)

track_bronze = PythonOperator(
    task_id='track_bronze_success',
    python_callable=track_success,
    op_kwargs={'stage': 'bronze_ingestion'},
    dag=dag,
)

silver_processing = BashOperator(
    task_id='silver_processing',
    bash_command="""
    docker exec spark-master python3 /opt/spark-apps/silver_processing.py \
    /opt/data_lake/bronze \
    /opt/data_lake/silver \
    deliveries
    """,
    dag=dag,
)

track_silver = PythonOperator(
    task_id='track_silver_success',
    python_callable=track_success,
    op_kwargs={'stage': 'silver_processing'},
    dag=dag,
)

gold_aggregation = BashOperator(
    task_id='gold_aggregation',
    bash_command="""
    docker exec spark-master python3 /opt/spark-apps/gold_aggregation.py \
    /opt/data_lake/silver \
    /opt/data_lake/gold
    """,
    dag=dag,
)

track_gold = PythonOperator(
    task_id='track_gold_success',
    python_callable=track_success,
    op_kwargs={'stage': 'gold_aggregation'},
    dag=dag,
)

load_to_warehouse = BashOperator(
    task_id='load_to_warehouse',
    bash_command="""
    docker exec spark-master python3 /opt/spark-apps/load_to_warehouse.py \
    /opt/data_lake/gold
    """,
    dag=dag,
)

track_warehouse = PythonOperator(
    task_id='track_warehouse_success',
    python_callable=track_success,
    op_kwargs={'stage': 'load_to_warehouse'},
    dag=dag,
)

bronze_ingestion >> track_bronze >> silver_processing >> track_silver
track_silver >> gold_aggregation >> track_gold >> load_to_warehouse >> track_warehouse
