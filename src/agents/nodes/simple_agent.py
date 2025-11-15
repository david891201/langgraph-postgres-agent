from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.chat_message_histories import PostgresChatMessageHistory

from src.models.model import ModelLoader

class SimpleAgent:
    def __init__(self, config: dict, session_id: str, model_source: str="Azure"):
        self.config = config
        self.model_source = model_source
        self.session_id = session_id
        self.llm, self.embedding = ModelLoader(config, self.model_source)()
        self.memory = PostgresChatMessageHistory(
            connection_string=self.config.get('postgresql_connection_string'),
            session_id=self.session_id,
        )
        self.prompt = PromptTemplate.from_template("""
            請根據以下資料回答問題。
                                                
            以下是過去的對話紀錄：
            {chat_history}

            問題：{question}

            請根據提供的資料作答。
            """
        )
    
    def __call__(self, state: dict) -> dict:
        history = ""
        for msg in self.memory.messages:
            role = "使用者" if msg.type == "human" else "助理"
            history += f"{role}：{msg.content}\n"
        
        chain = ( 
            {
                "chat_history": lambda _: history,
                "question": RunnablePassthrough()
            }
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
        response = chain.invoke(state.get("input"))

        self.memory.add_user_message(state.get("input"))
        self.memory.add_ai_message(response)

        return {**state, "response": response, "history": history}