from langchain_openrouter import ChatOpenRouter

llm = ChatOpenRouter(model = "openai/gpt-oss-20b:free",temperature=0)
print(llm.model_name)