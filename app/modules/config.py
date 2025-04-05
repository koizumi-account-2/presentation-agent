from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import os
import json, boto3
load_dotenv()
api_key = os.getenv("OPEN_API_KEY")
# print("api_key",api_key)
model = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=api_key)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small",api_key=api_key)

def get_db_url():
    secret_name = os.getenv("DB_SECRET_ARN")
    client = boto3.client("secretsmanager")
    response = client.get_secret_value(SecretId=secret_name)
    secret = json.loads(response["SecretString"])
    return (
        f"postgresql://{secret['username']}:{secret['password']}"
        f"@{secret['host']}:{secret['port']}/{secret['dbname']}"
    )
