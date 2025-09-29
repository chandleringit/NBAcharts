"""
Sync MySQL to BigQuery Script
用於將 MySQL 資料同步到 BigQuery
"""

from data_ingestion.bigquery import (
    create_dataset_if_not_exists,
    create_table,
    upload_data_to_bigquery,
    drop_table_if_exists
)

from data_ingestion.mysql import query_to_dataframe

from data_ingestion.bigquery import (
    nba_player_salary_bq_schema,
    nba_player_state_bq_schema,
    nba_team_salary_bq_schema,
    nba_team_state_bq_schema,
    nba_team_advance_bq_schema,
    nba_team_table_bq_schema,
    nba_news_headline_bq_schema,
    nba_news_udn_bq_schema,
)

# 同步的表配置
tables_config = [
    {
        'mysql_table': 'nba_player_salary',
        'bq_table': 'nba_player_salary',
        'schema_func': nba_player_salary_bq_schema,
        'partition_key': None  # 不需要分區
    },
    {
        'mysql_table': 'nba_player_state',
        'bq_table': 'nba_player_state',
        'schema_func': nba_player_state_bq_schema,
        'partition_key': None  # 不需要分區
    },
    {
        'mysql_table': 'nba_team_salary',
        'bq_table': 'nba_team_salary',
        'schema_func': nba_team_salary_bq_schema,
        'partition_key': None  # 不需要分區
    },
    {
        'mysql_table': 'nba_team_state',
        'bq_table': 'nba_team_state',
        'schema_func': nba_team_state_bq_schema,
        'partition_key': None  # 不需要分區
    },
    {
        'mysql_table': 'nba_team_advance',
        'bq_table': 'nba_team_advance',
        'schema_func': nba_team_advance_bq_schema,
        'partition_key': None  # 不需要分區
    },
    {
        'mysql_table': 'nba_team_table',
        'bq_table': 'nba_team_table',
        'schema_func': nba_team_table_bq_schema,
        'partition_key': None  # 不需要分區
    },{
        'mysql_table': 'nba_news_headline',
        'bq_table': 'nba_news_headline',
        'schema_func': nba_news_headline_bq_schema,
        'partition_key': None  # 不需要分區
    },
    {
        'mysql_table': 'nba_news_udn',
        'bq_table': 'nba_news_udn',
        'schema_func': nba_news_udn_bq_schema,
        'partition_key': None  # 不需要分區
    }
  
]

def sync_mysql_to_bigquery():
    """
    將 MySQL 資料同步到 BigQuery，使用 pandas
    """
    # 確保 BigQuery Dataset 存在
    create_dataset_if_not_exists()

    for config in tables_config:
        try:
            print(f"🔄 開始同步 {config['mysql_table']} 到 BigQuery...")

            # 刪除 BigQuery 表（如果存在）
            drop_table_if_exists(table_name=config['bq_table'])

            # 建立 BigQuery 表（如果不存在）
            schema = config['schema_func']()
            create_table(table_name=config['bq_table'], schema=schema, partition_key=config['partition_key'])

            # 從 MySQL 讀取資料
            sql = f"SELECT * FROM {config['mysql_table']}"
            df = query_to_dataframe(sql=sql)

            # 上傳到 BigQuery
            upload_data_to_bigquery(table_name=config['bq_table'], df=df, mode="replace")

            print(f"✅ {config['mysql_table']} 同步完成")

        except Exception as e:
            print(f"❌ {config['mysql_table']} 同步失敗: {e}")
            raise


def main():
    """
    主函數，執行 MySQL 到 BigQuery 的同步操作
    """
    print("🚀 開始執行 MySQL 到 BigQuery 的同步...")
    sync_mysql_to_bigquery()
    print("🎉 MySQL 到 BigQuery 的同步完成！")


if __name__ == "__main__":
    main()
