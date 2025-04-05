from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import os
import json, boto3, urllib.parse
load_dotenv()
api_key = os.getenv("OPEN_API_KEY")
# print("api_key",api_key)
model = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=api_key)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small",api_key=api_key)
def get_db_url():
        # ローカルで DATABASE_URL が定義されていれば、それを使う
    local_url = os.getenv("DATABASE_URL")
    if local_url:
        return local_url    
    DB_USERNAME = os.getenv("DB_USERNAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    return (
        f"postgresql://{DB_USERNAME}:{urllib.parse.quote_plus(DB_PASSWORD)}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
