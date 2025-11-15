import pandas as pd
from langchain_milvus import Milvus
from langchain_community.document_loaders import DataFrameLoader
from pymilvus import connections, list_collections

from src.models.model import ModelLoader 

class MilvusHandler:
    def __init__(self, collection_name: str, config: dict, model_source: str = 'Azure'):
        self.collection_name = collection_name
        self.config = config
        self.llm, self.embedding = ModelLoader(config, model_source)()
        self.model_source = model_source
        self.milvus_url = config.get('milvus_url')
    def insert(self, df: pd.DataFrame, page_content_column: str):
        documents = DataFrameLoader(df, page_content_column=page_content_column).load()
        vectorstore = Milvus.from_documents(
            documents=documents,
            embedding=self.embedding,
            connection_args={"uri": self.milvus_url, "token": "root:Milvus", "db_name": "default"},
            collection_name=self.collection_name,
            drop_old=True
        )
        print(f"文件已成功儲存至 {self.collection_name} 資料庫")
    def list_collection(self, milvus_host: str, milvus_port: str):
        connections.connect(alias="default", host=milvus_host, port=milvus_port)
        collections = list_collections()
        print("目前的 collections 有：", collections)