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
    secret_name = "AuroraAuroraSecretF26D12ED-oLCM3z1Q5Oxo"
    print("secret_name",secret_name)
    client = boto3.client("secretsmanager")
    response = client.get_secret_value(SecretId=secret_name)
    secret = json.loads(response["SecretString"])
    print("secret",secret)
    return (
        f"postgresql://{secret['username']}:{urllib.parse.quote_plus(secret['password'])}"
        f"@{secret['host']}:{secret['port']}/{secret['dbname']}"
    )
