from langchain_openrouter import ChatOpenRouter

llm = ChatOpenRouter(model = "qwen/qwen3.6-plus:free",temperature=0)
print(llm.model_name)