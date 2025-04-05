import json
from modules.agent import PresentationAgent
from modules.config import model
from modules.config import get_db_url
from langgraph.checkpoint.postgres import PostgresSaver
from fastapi import FastAPI, Request
app = FastAPI()




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
        agent = PresentationAgent(model,common_background,k=3,checkpointer=checkpointer)
        result = agent.run(user_background,state["thread_id"],state["persona_list"])
        print("result finally",result)
        return result