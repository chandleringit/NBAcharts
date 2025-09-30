"""
NBA BigQuery ETL DAG
從 MySQL 同步資料到 BigQuery 並進行 ETL 處理
"""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator


from data_ingestion.nba_sync_mysql_to_bigquery import sync_mysql_to_bigquery


# 預設參數
default_args = {
    'owner': 'data-team',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,  # 失敗時重試 1 次
    'retry_delay': timedelta(minutes=1),  # 重試間隔 1 分鐘
    'execution_timeout': timedelta(hours=1),  # 執行超時時間 1 小時
}


# 建立 DAG
with DAG(
    dag_id='NBA_bigquery_dag',
    default_args=default_args,
    description='NBA BigQuery DAG - 從 MySQL 同步資料到 BigQuery 並進行分析',
    schedule_interval='0 10 * * *',  # 每天 10 點執行一次（確保爬蟲任務完成後）
    catchup=False,  # 不執行歷史任務
    max_active_runs=1,  # 同時只允許一個 DAG 實例運行
    tags=['NBA', 'crawler', 'player', 'team'],
) as dag:

    # 開始任務
    start_task = BashOperator(
        task_id='start_bigquery_etl',
        bash_command='echo "開始執行 NBA BigQuery ETL 任務..."',
    )

    # MySQL 到 BigQuery 同步任務
    sync_to_bigquery_task = PythonOperator(
        task_id='sync_mysql_to_bigquery',
        python_callable=sync_mysql_to_bigquery,
    )

        
    # 結束任務
    end_task = BashOperator(
        task_id='end_bigquery_etl',
        bash_command='echo "Hahow BigQuery ETL 任務執行完成！"',
        trigger_rule='all_success',  # 只有當所有前置任務成功時才執行
    )

    # 設定任務依賴關係
    # BigQuery ETL 流程：開始 -> 同步資料 -> 建立銷售日統計 -> 進階分析 -> 每日匯總 -> 結束
    start_task >> sync_to_bigquery_task >> end_task
