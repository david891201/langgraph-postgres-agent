from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from src.models.model import ModelLoader

# 要2024-08-01-preview 以後的版本才可以使用 self.llm.with_structured_output(QueryCategory).invoke(state)
# class QueryCategory(BaseModel):
#     category: str = Field(description="Category 'tsmc' or 'mtk'")

class QueryClassifier:
    def __init__(self, config: dict, model_source: str="Azure"):
        self.config = config
        self.model_source = model_source
        self.llm,_ = ModelLoader(config, model_source)()
        self.prompt = PromptTemplate.from_template("""
            你是一位問題分類助理

            問題：{question}
            
            請根據以下規則選擇最符合的分類：

            - 選擇 **tsmc**：如果問題涉及台積電（TSMC）
            - 選擇 **mtk**：如果問題涉及聯發科（MediaTek、MTK）
            - 選擇 **others**：如果問題不屬於以上兩種分類的其中一種

            若問題明確屬於其中之一，請只輸出選項名稱（tsmc 或 mtk 或 others）。
            不要輸出任何多餘文字或解釋。                                                                            
            """
        )
    def __call__(self, state: dict) -> dict:
        chain = ( 
            {"question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
        response = chain.invoke(state.get("input"))
        return {**state, "intent": response}