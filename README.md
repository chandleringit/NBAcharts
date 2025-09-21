NBAcharts 🏀📊🐳
這個專案是一個基於 Python 的 NBA 數據工程解決方案，旨在實現數據擷取、任務編排、處理、儲存與視覺化的完整流程。所有服務都在 Docker 容器中運行，讓你能夠透過 Docker Compose 一鍵部署與管理。

專案特性 ✨
🏀 NBA 主題數據： 涵蓋球隊與球員的狀態、進階數據、薪資與最新新聞。
📨 任務佇列： 使用 RabbitMQ 作為訊息代理，搭配 Celery Workers 實現非同步任務處理。
🗓️ 自動化工作流： Airflow DAGs 實現數據擷取任務的自動排程與監控。
🗄️ 數據儲存： 採用 MySQL 資料庫來儲存所有擷取的數據。📊 數據視覺化： 透過 Metabase 建立互動式儀表板，輕鬆分析數據。
🐳 容器化部署： 每個服務都獨立成一個 Docker 容器，並透過共用網路實現互聯。

架構概覽 🧩

以下是專案的架構圖，展示了各個容器如何協同工作，以及數據流動的方向。flowchart LR

  %% Sources
  subgraph 資料來源
    S1[NBA 公開數據來源]
  end

  %% Containers
  subgraph Docker 容器
    direction LR
    P[Python 擷取]
    Q[RabbitMQ 代理]
    W[Celery Workers]
    DB[MySQL]
    AF[Airflow 排程/網頁伺服器]
    MB[Metabase]
  end

  %% Docker network
  subgraph Docker 網路
    NET[my_network]
  end

  %% Data flow
  S1 --> P --> Q --> W --> DB --> MB
  AF --> P
  AF --> W
  AF --> DB

  %% Network connections (all containers join the same docker network)
  P --- NET
  Q --- NET
  W --- NET
  DB --- NET
  AF --- NET
  MB --- NET

  %% Common exposed ports (host:container)
  Qp[埠號 15672, 5672, 5555]
  DBp[埠號 3306]
  AFp[埠號 8080]
  MBp[埠號 3000]

  Q --- Qp
  DB --- DBp
  AF --- AFp
  MB --- MBp

  %% Styles
  classDef docker fill:#e3f2fd,stroke:#1e88e5,stroke-width:1px,color:#0d47a1
  classDef network fill:#e8f5e9,stroke:#2e7d32,stroke-width:1px,color:#1b5e20
  classDef port fill:#fff3e0,stroke:#f57c00,stroke-width:1px,color:#e65100

  class P,Q,W,DB,AF,MB docker
  class NET network
  class Qp,DBp,AFp,MBp port

快速啟動指南 🚀
前置作業
確保已安裝 Docker 與 Docker Compose。
建議先建立 Docker 網路：
docker network create my_network

一鍵啟動所有服務
依照以下順序啟動各個服務：
# 1. 啟動訊息代理 (RabbitMQ/Flower)
docker compose -f docker-compose-broker.yml up -d

# 2. 啟動資料庫 (MySQL)
docker compose -f docker-compose-mysql.yml up -d

# 3. 啟動 Airflow (Scheduler/Webserver)
docker compose -f airflow/docker-compose-airflow.yml up -d

# 4. 啟動任務 Workers (Celery)
docker compose -f docker-compose-worker.yml up -d

# 5. 啟動數據擷取 Producers
docker compose -f docker-compose-producer.yml up -d

# 6. 啟動儀表板 (Metabase)
docker compose -f metabase/docker-compose-metabase.yml up -d

服務入口
RabbitMQ 管理介面： http://localhost:15672
Airflow Web UI： http://localhost:8080 （預設帳密：airflow/airflow）
Metabase 儀表板： http://localhost:3000

關閉全部服務 ⛔
若要停止並移除所有容器，請依相反順序執行 down 命令：

docker compose -f metabase/docker-compose-metabase.yml down
docker compose -f airflow/docker-compose-airflow.yml down
docker compose -f docker-compose-producer.yml down
docker compose -f docker-compose-worker.yml down
docker compose -f docker-compose-mysql.yml down
docker compose -f docker-compose-broker.yml down

開發者與貢獻者 👩‍💻我們歡迎任何形式的貢獻！若您有任何想法或發現問題，請隨時提交 PR 或 Issue。在提交 PR 前，請簡述您的修改動機與測試步驟。

授權 📜請參閱 LICENSE 檔案。