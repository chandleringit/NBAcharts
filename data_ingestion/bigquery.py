"""
BigQuery 操作模組
參考 mysql.py 的結構，提供 BigQuery 的資料庫操作功能
"""
import pandas as pd
from google.cloud import bigquery
from google.cloud.bigquery import SchemaField, LoadJobConfig, WriteDisposition
import logging
from typing import List, Dict
from data_ingestion.config import GCP_PROJECT_ID as PROJECT_ID

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# BigQuery 配置
DATASET_ID = "NBA"

def get_bigquery_client():
    """建立 BigQuery 客戶端"""
    return bigquery.Client(project=PROJECT_ID)

def create_dataset_if_not_exists(dataset_id: str = DATASET_ID):
    """建立 BigQuery Dataset（如果不存在）"""
    client = get_bigquery_client()
    dataset_ref = client.dataset(dataset_id)
    
    try:
        client.get_dataset(dataset_ref)
        logger.info(f"Dataset {dataset_id} already exists")
    except Exception:
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = "US"  # 或您偏好的區域
        dataset = client.create_dataset(dataset)
        logger.info(f"Created dataset {dataset_id}")

# ========== Table Schema 定義 ==========

def nba_player_salary_bq_schema():
    """定義 NBA 表的 BigQuery schema"""
    schema = [
        bigquery.SchemaField(name="year", field_type="INTEGER"),
        bigquery.SchemaField(name="player", field_type="STRING"),
        bigquery.SchemaField(name="team", field_type="STRING"),
        bigquery.SchemaField(name="salary", field_type="INTEGER"),
        bigquery.SchemaField(name="uploaded_at", field_type="DATETIME"),
    
    ]
    return schema

def nba_player_state_bq_schema():
    """定義 nba_player_state 表的 BigQuery schema"""
    schema = [
        bigquery.SchemaField(name="year", field_type="INTEGER"),
        bigquery.SchemaField(name="player", field_type="STRING"),
        bigquery.SchemaField(name="team", field_type="STRING"),
        bigquery.SchemaField(name="salary", field_type="INTEGER"),
        bigquery.SchemaField(name="age", field_type="INTEGER"),
        bigquery.SchemaField(name="pos", field_type="STRING"),
        bigquery.SchemaField(name="games", field_type="INTEGER"),
        bigquery.SchemaField(name="games_started", field_type="INTEGER"),
        bigquery.SchemaField(name="minutes_played", field_type="INTEGER"),
        bigquery.SchemaField(name="field_goals", field_type="INTEGER"),
        bigquery.SchemaField(name="field_goals_attempts", field_type="INTEGER"),
        bigquery.SchemaField(name="field_goals_percentage", field_type="FLOAT"),
        bigquery.SchemaField(name="3p_field_goals", field_type="INTEGER"),
        bigquery.SchemaField(name="3p_field_goals_attempts", field_type="INTEGER"),
        bigquery.SchemaField(name="3p_field_goals_percentage", field_type="FLOAT"),
        bigquery.SchemaField(name="2p_field_goals", field_type="INTEGER"),
        bigquery.SchemaField(name="2p_field_goals_attempts", field_type="INTEGER"),
        bigquery.SchemaField(name="2p_field_goals_percentage", field_type="FLOAT"),
        bigquery.SchemaField(name="efg_pct", field_type="FLOAT"),
        bigquery.SchemaField(name="free_throws", field_type="INTEGER"),
        bigquery.SchemaField(name="free_throws_attempts", field_type="INTEGER"),
        bigquery.SchemaField(name="free_throws_percentage", field_type="FLOAT"),
        bigquery.SchemaField(name="offensive_rebounds", field_type="INTEGER"),
        bigquery.SchemaField(name="defensive_rebounds", field_type="INTEGER"),
        bigquery.SchemaField(name="total_rebounds", field_type="INTEGER"),
        bigquery.SchemaField(name="assists", field_type="INTEGER"),
        bigquery.SchemaField(name="steals", field_type="INTEGER"),
        bigquery.SchemaField(name="blocks", field_type="INTEGER"),
        bigquery.SchemaField(name="turnovers", field_type="INTEGER"),
        bigquery.SchemaField(name="personal_fouls", field_type="INTEGER"),
        bigquery.SchemaField(name="points", field_type="INTEGER"),

    ]
    return schema

def nba_team_salary_bq_schema():
    """定義 nba_team_salary 表的 BigQuery schema"""
    schema = [
        bigquery.SchemaField(name="year", field_type="INTEGER"),
        bigquery.SchemaField(name="team", field_type="STRING"),
        bigquery.SchemaField(name="salary", field_type="INTEGER"),
        bigquery.SchemaField(name="uploaded_at", field_type="DATETIME"),
 
    ]
    return schema

def nba_team_state_bq_schema():
    """定義 nba_team_state 表的 BigQuery schema"""
    schema = [
        bigquery.SchemaField(name="year", field_type="INTEGER"),
        bigquery.SchemaField(name="team", field_type="STRING"),
        bigquery.SchemaField(name="games", field_type="INTEGER"),
        bigquery.SchemaField(name="minutes_played", field_type="INTEGER"),
        bigquery.SchemaField(name="field_goals", field_type="INTEGER"),
        bigquery.SchemaField(name="field_goals_attempts", field_type="INTEGER"),
        bigquery.SchemaField(name="field_goals_percentage", field_type="FLOAT"),
        bigquery.SchemaField(name="3p_field_goals", field_type="INTEGER"),
        bigquery.SchemaField(name="3p_field_goals_attempts", field_type="INTEGER"),
        bigquery.SchemaField(name="3p_field_goals_percentage", field_type="FLOAT"),
        bigquery.SchemaField(name="2p_field_goals", field_type="INTEGER"),
        bigquery.SchemaField(name="2p_field_goals_attempts", field_type="INTEGER"),
        bigquery.SchemaField(name="2p_field_goals_percentage", field_type="FLOAT"),
        bigquery.SchemaField(name="free_throws", field_type="INTEGER"),
        bigquery.SchemaField(name="free_throws_attempts", field_type="INTEGER"),
        bigquery.SchemaField(name="free_throws_percentage", field_type="FLOAT"),
        bigquery.SchemaField(name="offensive_rebounds", field_type="INTEGER"),
        bigquery.SchemaField(name="defensive_rebounds", field_type="INTEGER"),
        bigquery.SchemaField(name="total_rebounds", field_type="INTEGER"),
        bigquery.SchemaField(name="assists", field_type="INTEGER"),
        bigquery.SchemaField(name="steals", field_type="INTEGER"),
        bigquery.SchemaField(name="blocks", field_type="INTEGER"),
        bigquery.SchemaField(name="turnovers", field_type="INTEGER"),
        bigquery.SchemaField(name="personal_fouls", field_type="INTEGER"),
        bigquery.SchemaField(name="points", field_type="INTEGER"),
        bigquery.SchemaField(name="uploaded_at", field_type="DATETIME"),

    ]
    return schema

def nba_team_advance_bq_schema():
    """定義 nba_team_advance 表的 BigQuery schema"""
    schema = [
        bigquery.SchemaField(name="year", field_type="INTEGER"),
        bigquery.SchemaField(name="team", field_type="STRING"),
        bigquery.SchemaField(name="average_age", field_type="FLOAT"),
        bigquery.SchemaField(name="wins", field_type="INTEGER"),
        bigquery.SchemaField(name="loses", field_type="INTEGER"),
        bigquery.SchemaField(name="winsP", field_type="FLOAT"),
        bigquery.SchemaField(name="pythagorean_wins", field_type="FLOAT"),
        bigquery.SchemaField(name="pythagorean_lose", field_type="FLOAT"),
        bigquery.SchemaField(name="margin_of_victory", field_type="FLOAT"),
        bigquery.SchemaField(name="strength_of_schedule", field_type="FLOAT"),
        bigquery.SchemaField(name="simple_rating_system", field_type="FLOAT"),
        bigquery.SchemaField(name="offensive_rating", field_type="FLOAT"),
        bigquery.SchemaField(name="defensive_rating", field_type="FLOAT"),
        bigquery.SchemaField(name="net_rating", field_type="FLOAT"),
        bigquery.SchemaField(name="pace_factor", field_type="FLOAT"),
        bigquery.SchemaField(name="free_throw_attempt_rate", field_type="FLOAT"),
        bigquery.SchemaField(name="3p_attempt_rate", field_type="FLOAT"),
        bigquery.SchemaField(name="true_shooting_percentage", field_type="FLOAT"),
        bigquery.SchemaField(name="effective_field_goal_percentage", field_type="FLOAT"),
        bigquery.SchemaField(name="turnover_percentage", field_type="FLOAT"),
        bigquery.SchemaField(name="offensive_rebound_percentage", field_type="FLOAT"),
        bigquery.SchemaField(name="free_throws_per_field_goal_attempt", field_type="FLOAT"),
        bigquery.SchemaField(name="opponent_effective_field_goal_percentage", field_type="FLOAT"),
        bigquery.SchemaField(name="opponent_turnover_percentage", field_type="FLOAT"),
        bigquery.SchemaField(name="defensive_rebound_percentage", field_type="FLOAT"),
        bigquery.SchemaField(name="opponent_free_throws_per_field_goal_attempt", field_type="FLOAT"),
        bigquery.SchemaField(name="arena_name", field_type="STRING"),
        bigquery.SchemaField(name="attendance", field_type="INTEGER"),
        bigquery.SchemaField(name="attendance_per_g", field_type="FLOAT"),
        bigquery.SchemaField(name="uploaded_at", field_type="DATETIME"),
       

    ]
    return schema

def nba_team_table_bq_schema():
    """定義 nba_team_table 表的 BigQuery schema"""
    schema = [
        bigquery.SchemaField(name="year", field_type="INTEGER"),
        bigquery.SchemaField(name="team", field_type="STRING"),
        bigquery.SchemaField(name="salary", field_type="INTEGER"),
        bigquery.SchemaField(name="games", field_type="INTEGER"),
        bigquery.SchemaField(name="minutes_played", field_type="INTEGER"),
        bigquery.SchemaField(name="field_goals", field_type="INTEGER"),
        bigquery.SchemaField(name="field_goals_attempts", field_type="INTEGER"),
        bigquery.SchemaField(name="field_goals_percentage", field_type="FLOAT"),
        bigquery.SchemaField(name="3p_field_goals", field_type="INTEGER"),
        bigquery.SchemaField(name="3p_field_goals_attempts", field_type="INTEGER"),
        bigquery.SchemaField(name="3p_field_goals_percentage", field_type="FLOAT"),
        bigquery.SchemaField(name="2p_field_goals", field_type="INTEGER"),
        bigquery.SchemaField(name="2p_field_goals_attempts", field_type="INTEGER"),
        bigquery.SchemaField(name="2p_field_goals_percentage", field_type="FLOAT"),
        bigquery.SchemaField(name="free_throws", field_type="INTEGER"),
        bigquery.SchemaField(name="free_throws_attempts", field_type="INTEGER"),
        bigquery.SchemaField(name="free_throws_percentage", field_type="FLOAT"),
        bigquery.SchemaField(name="offensive_rebounds", field_type="INTEGER"),
        bigquery.SchemaField(name="defensive_rebounds", field_type="INTEGER"),
        bigquery.SchemaField(name="total_rebounds", field_type="INTEGER"),
        bigquery.SchemaField(name="assists", field_type="INTEGER"),
        bigquery.SchemaField(name="steals", field_type="INTEGER"),
        bigquery.SchemaField(name="blocks", field_type="INTEGER"),
        bigquery.SchemaField(name="turnovers", field_type="INTEGER"),
        bigquery.SchemaField(name="personal_fouls", field_type="INTEGER"),
        bigquery.SchemaField(name="points", field_type="INTEGER"),
        bigquery.SchemaField(name="average_age", field_type="FLOAT"),
        bigquery.SchemaField(name="wins", field_type="INTEGER"),
        bigquery.SchemaField(name="loses", field_type="INTEGER"),
        bigquery.SchemaField(name="winsP", field_type="FLOAT"),
        bigquery.SchemaField(name="pythagorean_wins", field_type="FLOAT"),
        bigquery.SchemaField(name="pythagorean_lose", field_type="FLOAT"),
        bigquery.SchemaField(name="margin_of_victory", field_type="FLOAT"),
        bigquery.SchemaField(name="strength_of_schedule", field_type="FLOAT"),
        bigquery.SchemaField(name="simple_rating_system", field_type="FLOAT"),
        bigquery.SchemaField(name="offensive_rating", field_type="FLOAT"),
        bigquery.SchemaField(name="defensive_rating", field_type="FLOAT"),
        bigquery.SchemaField(name="net_rating", field_type="FLOAT"),
        bigquery.SchemaField(name="pace_factor", field_type="FLOAT"),
        bigquery.SchemaField(name="free_throw_attempt_rate", field_type="FLOAT"),
        bigquery.SchemaField(name="3p_attempt_rate", field_type="FLOAT"),
        bigquery.SchemaField(name="true_shooting_percentage", field_type="FLOAT"),
        bigquery.SchemaField(name="effective_field_goal_percentage", field_type="FLOAT"),
        bigquery.SchemaField(name="turnover_percentage", field_type="FLOAT"),
        bigquery.SchemaField(name="offensive_rebound_percentage", field_type="FLOAT"),
        bigquery.SchemaField(name="free_throws_per_field_goal_attempt", field_type="FLOAT"),
        bigquery.SchemaField(name="opponent_effective_field_goal_percentage", field_type="FLOAT"),
        bigquery.SchemaField(name="opponent_turnover_percentage", field_type="FLOAT"),
        bigquery.SchemaField(name="defensive_rebound_percentage", field_type="FLOAT"),
        bigquery.SchemaField(name="opponent_free_throws_per_field_goal_attempt", field_type="FLOAT"),
        bigquery.SchemaField(name="arena_name", field_type="STRING"),
        bigquery.SchemaField(name="attendance", field_type="INTEGER"),
        bigquery.SchemaField(name="attendance_per_g", field_type="FLOAT"),

    ]
    return schema

def nba_news_headline_bq_schema():
    """定義 nba_news_headline 表的 BigQuery schema"""
    schema = [
        bigquery.SchemaField(name="news_at", field_type="DATE"),
        bigquery.SchemaField(name="title", field_type="STRING"),
        bigquery.SchemaField(name="article_time", field_type="DATETIME"),
        bigquery.SchemaField(name="label", field_type="STRING"),
        bigquery.SchemaField(name="link", field_type="STRING"),
        bigquery.SchemaField(name="uploaded_at", field_type="DATETIME"),
         
    ]
    return schema

def nba_news_udn_bq_schema():
    """定義 nba_news_udn 表的 BigQuery schema"""
    schema = [
        bigquery.SchemaField(name="id", field_type="STRING"),
        bigquery.SchemaField(name="title", field_type="STRING"),
        bigquery.SchemaField(name="url", field_type="STRING"),
        bigquery.SchemaField(name="date", field_type="STRING"),
                 
    ]
    return schema


# ========== 基礎操作函數 ==========

def create_table(table_name: str, schema: List[SchemaField], dataset_id: str = DATASET_ID, partition_key: str = None):
    """
    建立 BigQuery 表格，並可選擇性地指定分區。

    參數：
        table_name: 要建立的表格名稱。
        schema: 表格的結構定義。
        dataset_id: 表格將被建立的資料集 ID。
        partition_key: 用於分區的欄位名稱（可選）。
    """
    client = bigquery.Client()
    table_id = f"{PROJECT_ID}.{dataset_id}.{table_name}"

    table = bigquery.Table(table_id, schema=schema)

    if partition_key:
        table.time_partitioning = bigquery.TimePartitioning(
            type_=bigquery.TimePartitioningType.DAY,
            field=partition_key  # 用於分區的欄位名稱
        )

    try:
        table = client.create_table(table)
        print(f"✅ 表格 {table_id} 建立成功。")
    except Exception as e:
        print(f"❌ 表格 {table_id} 建立失敗: {e}")
        raise

def upload_data_to_bigquery(table_name: str, df: pd.DataFrame, dataset_id: str = DATASET_ID, mode: str = "replace"):
    """
    上傳 DataFrame 到 BigQuery（類似 mysql.py 的 upload_data_to_mysql）
    
    Args:
        table_name: 表名
        df: 要上傳的 DataFrame
        dataset_id: Dataset ID
        mode: 寫入模式 ("replace", "append")
    """
    client = get_bigquery_client()
    table_id = f"{PROJECT_ID}.{dataset_id}.{table_name}"
    
    # 設定寫入模式
    if mode == "replace":
        write_disposition = WriteDisposition.WRITE_TRUNCATE
    elif mode == "append":
        write_disposition = WriteDisposition.WRITE_APPEND
    else:
        write_disposition = WriteDisposition.WRITE_EMPTY
    
    # 配置載入工作
    job_config = LoadJobConfig(
        write_disposition=write_disposition,
        autodetect=True,  # 自動偵測 schema
    )
    
    try:
        # 執行載入
        job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
        job.result()  # 等待完成
        
        print(f"✅ 資料已上傳到 BigQuery 表 '{table_name}'，共 {len(df)} 筆記錄")
        
    except Exception as e:
        print(f"❌ 上傳資料到 BigQuery 表 '{table_name}' 失敗: {e}")
        raise

def upload_data_to_bigquery_insert(table_name: str, data: List[Dict], dataset_id: str = DATASET_ID, batch_size: int = 5000):
    """
    使用 insert_rows_json 上傳資料到 BigQuery，支持分批上傳
    
    Args:
        table_name: 表名
        data: 要插入的資料列表
        dataset_id: Dataset ID
        batch_size: 每批上傳的資料量
    """
    client = get_bigquery_client()
    table_id = f"{PROJECT_ID}.{dataset_id}.{table_name}"
    
    try:
        # 獲取表引用
        table = client.get_table(table_id)
        
        # 分批插入資料
        for i in range(0, len(data), batch_size):
            batch = data[i:i + batch_size]
            errors = client.insert_rows_json(table, batch)
            if errors:
                print(f"❌ 插入資料到 BigQuery 表 '{table_name}' 時發生錯誤: {errors}")
                raise Exception(f"BigQuery 插入失敗: {errors}")
            print(f"✅ 已上傳 {len(batch)} 筆記錄到 {table_name}")
        
    except Exception as e:
        print(f"❌ 插入資料到 BigQuery 表 '{table_name}' 失敗: {e}")
        raise

def create_view(view_name: str, view_sql: str, dataset_id: str = DATASET_ID):
    """
    在 BigQuery 中建立或替換 View（類似 mysql.py 的 create_view）
    
    Args:
        view_name: View 的名稱
        view_sql: 建立 View 的 SQL 語句
        dataset_id: Dataset ID
    """
    client = get_bigquery_client()
    view_id = f"{PROJECT_ID}.{dataset_id}.{view_name}"
    
    # 確保 Dataset 存在
    create_dataset_if_not_exists(dataset_id)
    
    view = bigquery.Table(view_id)
    view.view_query = view_sql
    
    try:
        # 嘗試更新現有 view
        client.update_table(view, ["view_query"])
        print(f"✅ 更新 BigQuery View '{view_name}' 成功")
    except Exception:
        # 如果不存在則建立新的
        try:
            view = client.create_table(view)
            print(f"✅ 建立 BigQuery View '{view_name}' 成功")
        except Exception as e:
            print(f"❌ 建立 BigQuery View '{view_name}' 失敗: {e}")
            raise

def create_table_from_view(view_name: str, table_name: str, dataset_id: str = DATASET_ID):
    """
    從 BigQuery View 建立實體 Table（類似 mysql.py 的 create_table_from_view）
    
    Args:
        view_name: 來源 View 的名稱
        table_name: 目標 Table 的名稱
        dataset_id: Dataset ID
    """
    client = get_bigquery_client()
    
    source_view_id = f"{PROJECT_ID}.{dataset_id}.{view_name}"
    dest_table_id = f"{PROJECT_ID}.{dataset_id}.{table_name}"
    
    try:
        # 完全取代：先刪除舊 Table，再建立新的
        print(f"🗑️  正在刪除舊的 BigQuery Table '{table_name}' (如果存在)...")
        try:
            client.delete_table(dest_table_id)
        except Exception:
            pass  # 表不存在時忽略錯誤
        
        print(f"📝 正在從 View '{view_name}' 建立新的 BigQuery Table '{table_name}'...")
        
        # 建立查詢工作來複製 view 資料到 table
        sql = f"SELECT * FROM `{source_view_id}`"
        
        job_config = bigquery.QueryJobConfig(
            destination=dest_table_id,
            write_disposition=WriteDisposition.WRITE_TRUNCATE
        )
        
        query_job = client.query(sql, job_config=job_config)
        query_job.result()  # 等待完成
        
        # 獲取記錄數量
        count_sql = f"SELECT COUNT(*) as count FROM `{dest_table_id}`"
        count_result = client.query(count_sql).result()
        count = list(count_result)[0].count
        
        print(f"✅ 成功建立 BigQuery Table '{table_name}'，共 {count} 筆記錄")
        
    except Exception as e:
        print(f"❌ 從 View '{view_name}' 建立 BigQuery Table '{table_name}' 失敗: {e}")
        raise

def drop_table_if_exists(table_name: str, dataset_id: str = DATASET_ID):
    """
    刪除 BigQuery 表格（如果存在）

    Args:
        table_name: 要刪除的表格名稱。
        dataset_id: 表格所在的資料集 ID。
    """
    client = get_bigquery_client()
    table_id = f"{PROJECT_ID}.{dataset_id}.{table_name}"

    try:
        client.delete_table(table_id)
        print(f"✅ 表格 {table_id} 已刪除。")
    except Exception as e:
        print(f"❌ 刪除表格 {table_id} 失敗或表格不存在: {e}")





# ========== 輔助函數 ==========

def execute_query(sql: str, dataset_id: str = DATASET_ID) -> List[Dict]:
    """
    執行 BigQuery SQL 查詢並返回結果
    
    Args:
        sql: SQL 查詢語句
        dataset_id: Dataset ID
    
    Returns:
        查詢結果的列表
    """
    client = get_bigquery_client()
    
    query_job = client.query(sql)
    results = query_job.result()
    
    # 直接轉換為字典列表
    return [dict(row) for row in results]

def get_table_info(table_name: str, dataset_id: str = DATASET_ID) -> Dict:
    """
    獲取 BigQuery 表的資訊
    
    Args:
        table_name: 表名
        dataset_id: Dataset ID
    
    Returns:
        表的資訊字典
    """
    client = get_bigquery_client()
    table_id = f"{PROJECT_ID}.{dataset_id}.{table_name}"
    
    try:
        table = client.get_table(table_id)
        return {
            "table_id": table.table_id,
            "num_rows": table.num_rows,
            "num_bytes": table.num_bytes,
            "created": table.created,
            "modified": table.modified,
            "schema": [{"name": field.name, "type": field.field_type} for field in table.schema]
        }
    except Exception as e:
        print(f"❌ 獲取表 '{table_name}' 資訊失敗: {e}")
        raise

