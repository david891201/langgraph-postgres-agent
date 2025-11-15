from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_milvus import Milvus
from langchain_core.runnables import RunnablePassthrough
from langchain_community.chat_message_histories import PostgresChatMessageHistory

from src.models.model import ModelLoader

class MTKStockSearchAgent:
    def __init__(self, config: dict, session_id: str, model_source: str="Azure"):
        self.config = config
        self.collection_name = "mtk_price"
        self.model_source = model_source
        self.session_id = session_id
        self.llm, self.embedding = ModelLoader(config, self.model_source)()
        self.memory = PostgresChatMessageHistory(
            connection_string=self.config.get('postgresql_connection_string'),
            session_id=self.session_id,
        )
        self.prompt = PromptTemplate.from_template("""
            你是一位股票分析助理，請根據以下資料回答問題。
                                                
            以下是過去的對話紀錄：
            {chat_history}

            以下是相關資料：
            {context}

            問題：{question}

            請根據提供的資料作答，若資料中有符合日期的內容，請直接給出對應的價格，並註明資料來源為Milvus資料庫。
            """
        )
    
    def _format_docs(self, docs):
        return "\n\n".join(f"{doc.page_content}: {str(doc.metadata)}" for doc in docs)
    
    def _debug_docs(self, docs):
        print("====== Retrieved Documents ======")
        for i, doc in enumerate(docs):
            print(f"[{i}] {doc.page_content}")
            print(f"[{i}] metadata: {doc.metadata}")
        return docs
    
    def __call__(self, state: dict) -> dict:
        vectorstore = Milvus(
            embedding_function=self.embedding,
            connection_args={"uri": self.config.get('milvus_url'), "token": "root:Milvus", "db_name": "default"},
            collection_name=self.collection_name,
        )       
        retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 10})
        
        history = ""
        for msg in self.memory.messages:
            role = "使用者" if msg.type == "human" else "助理"
            history += f"{role}：{msg.content}\n"
        
        rag_chain = ( 
            {
                "chat_history": lambda _: history,
                "context": retriever | self._debug_docs | self._format_docs,
                "question": RunnablePassthrough()
            }
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
        response = rag_chain.invoke(state.get("input"))

        self.memory.add_user_message(state.get("input"))
        self.memory.add_ai_message(response)

        return {**state, "response": response, "history": history}