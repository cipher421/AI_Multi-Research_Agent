from langchain_openrouter import ChatOpenRouter

llm = ChatOpenRouter(model = "google/gemma-4-31b-it-20260402:free",temperature=0)
print(llm.model_name)