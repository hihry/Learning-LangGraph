import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# 1. Load your API key
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

# 2. Initialize the model
# We point the base_url to OpenRouter and use a ':free' model ID
llm = ChatOpenAI(
    model="google/gemini-2.0-flash-exp:free", # One of the best free models
    openai_api_key=api_key,
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "http://localhost:3000", # Optional: your app URL
        "X-Title": "Local Agent Study",         # Optional: your app name
    }
)

# 3. Test it
response = llm.invoke("What are the benefits of using Poetry for Python?")
print(response.content)