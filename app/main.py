import json
from modules.agent import PresentationAgent
from modules.config import model
from modules.config import get_db_url
from langgraph.checkpoint.postgres import PostgresSaver
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # セキュリティのため本番では特定のドメインに限定する
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health():
    return {"message": "OK"}

@app.post("/presentation")
async def suggest(request: Request):
    with PostgresSaver.from_conn_string(get_db_url()) as checkpointer:
        checkpointer.setup()
        body = await request.json()
        common_background = body["common_background"]
        user_background = body["user_background"]
        state = body["state"]
        print("common_background",common_background)
        print("user_background",user_background)
        print("state",state)
        agent = PresentationAgent(model,common_background,k=3,checkpointer=checkpointer)
        result = agent.run(user_background,state["thread_id"],state["persona_list"])
        print("result finally",result)
        return result