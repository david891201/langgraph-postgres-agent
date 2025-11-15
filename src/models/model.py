from langchain_openai import AzureChatOpenAI, OpenAIEmbeddings, AzureOpenAIEmbeddings

class ModelLoader:
    def __init__(self, config: dict, model_source: str = 'Azure'):
        self.config = config
        self.model_source = model_source
    
    def __call__(self):
        llm = AzureChatOpenAI(
            api_key=self.config.get('azure_openai_api_key'),
            azure_endpoint=self.config.get('azure_openai_endpoint'),
            azure_deployment=self.config.get('azure_openai_deployment'),
            api_version=self.config.get('azure_openai_api_version'),
            model=self.config.get('azure_openai_model')
        )
        embeddings = AzureOpenAIEmbeddings(
            api_key=self.config.get('azure_openai_api_key'),
            azure_endpoint=self.config.get('azure_openai_endpoint'),
            azure_deployment=self.config.get('azure_openai_embedding_deployment'),
            api_version=self.config.get('azure_openai_embedding_api_version'),
            chunk_size=100  
        )
        return llm, embeddings