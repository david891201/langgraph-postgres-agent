## 專案簡介
本專案目標為建立一個具備長期記憶功能的 LangGraph API ，以 PostgreSQL 作為對話紀錄的後端儲存，透過 LangChain 讀取與整理歷史對話內容，再以 Runnable 機制將「歷史對話」與「當前使用者的查詢」一併餵入 LLM，產出具上下文理解的最終回應。

---

## 核心功能
- 長期記憶對話：自動儲存與提取使用者歷史對話紀錄。
- LangGraph 流程編排：以 node & edges 形式設計對話策略與模型流程。
- PostgreSQL 儲存歷史對話紀錄：穩定存取歷史對話資料。
- Runnable Chain 組合：將使用者的 query 與歷史記錄一起傳遞給 LLM，使模型的回覆具備上下文理解。

---

## 使用技術
- **語言：** Python
- **架構與技術：** langgraph、langchain、postgresql、Azure API

---

## 測試環境
Python 3.10.2

---

## 執行方式

### 事前準備
1. 建立虛擬環境，並根據requirements.txt安裝相對應版本的套件
2. 於 conf/job.conf 填入自己的 Azure 相關參數
3. 本專案為測試 langgraph 流程，簡單增加了幾個 nodes，node的主要功能為利用 RAG 技術查詢台積電或聯發科的歷史股價資訊，並使用 Milvus 作為 RAG 搜索的資料庫，因此在 conf/job.conf 會有 Milvus 的相關參數。該參數可根據自己使用的資料庫做替換（若使用不同的資料庫，節點內和 Milvus 的相關套件也需自己做相對應的替換）

### 建立 Postgresql container 以及儲存歷史對話所需的 database
1. 使用 postgresql 的 dockerfile 於 docker 建立 container(主機 port和容器內部的 port 根據自己的需求決定)
2. 進入 container
```text 
docker exec -it <your_container_name> bash
```
3. 連線 PostgreSQL
```text 
psql -U postgres
```
4. 建立儲存歷史對話所需的 database
```text 
CREATE DATABASE chat_history;
```
5. 將 conf/job.conf 裡面的 postgresql_connection_string 修改成自己的版本
```text 
postgresql://postgres:<your_password>@<your_host>:<your_port>/chat_history
```

### 使用方法
#### 啟動 api 
```text 
bash bin/start_server.sh
```
#### 單純測試記憶功能 
```text
bash bin/run_agent.sh --user_input "請給我台積電的股價資訊" --session_id 001
```
##### 先問過一個問題後，再執行 
```text
bash bin/run_agent.sh --user_input "請問我之前問過什麼問題" --session_id 001
```
#### 將股價資訊儲存至對應的 Milvus 資料庫
```text
python -m bin.ingest_docs --stock_id "2454.TW" --collection_name "mtk_price"
``` 
---

## 專案結構
```text
langgraph-postgres-agent/
├── src/
│   ├── agents/
│   │   ├── state.py # 定義節點間傳遞的 state 結構
│   │   └── graph.py # 將所有 nodes 組成可執行的 graph
│   │   └── nodes/ # 個別節點邏輯（含記憶）
│   │       ├── query_router.py # Query 分類，決定使用哪個 agent
│   │       ├── simple_agent.py # 一般查詢（非股票相關）
│   │       ├── tsmc_agent.py   # 台積電相關查詢
│   │       └── mtk_agent.py    # 聯發科相關查詢
│   ├── api/
│   │   └── server.py
│   ├── models/
│   │   └──model.py # 模型載入邏輯
│   ├── services/
│   │   ├── milvus_service.py # 文件存入 Milvus邏輯
│   │   └── stock_fetcher.py # 爬取個股歷史股價資訊
│   ├── utils/
│       ├── args_parser.py
│       └── utils.py
│   └── main.py # 啟動 agent 的程式進入點
│ 
├── bin/
│   ├── run_agent.sh            # 啟動 agent
│   ├── start_server.sh         # 啟動 API server
│   └── ingest_docs.py          # 一次性將文件塞入 Milvus 的腳本
│
├── logs/
│
├── tests/
│
├── requirements.txt
└── README.md
```
