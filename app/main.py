import json
from modules.agent import PresentationAgent
from modules.config import model
from modules.config import get_db_url
from langgraph.checkpoint.postgres import PostgresSaver
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from modules.verify import verify_jwt_from_cookie
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # セキュリティのため本番では特定のドメインに限定する
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/")
async def root():
    return {"message": "Hello World"}

@app.get("/api/health")
async def health():
    return {"message": "OK"}

@app.post("/api/presentation")
async def suggest(request: Request):
    with PostgresSaver.from_conn_string(get_db_url()) as checkpointer:
        checkpointer.setup()
        body = await request.json()
        # common_background = body["common_background"]
        user_background = body["user_background"]
        state = body["state"]
        print("state",state)
        agent = PresentationAgent(model,k=3,checkpointer=checkpointer)
        result = agent.run(user_background,state["thread_id"],state["persona_list"],common_background=state["common_background"])
        fake_result ={
            "thread_id": "b315d660-ee1d-4f6f-bd41-6648fe8bb9e1",
            "common_background": "ITベンチャー企業に勤めています",
            "user_request": "",
            "persona_list": [
                {
                    "name": "佐藤健太AAAA",
                    "background": "30歳男性。AI開発部門で働くエンジニア。大学でコンピュータサイエンスを専攻し、5年間の経験を持つ。新しい技術に対する好奇心が強く、特に機械学習に興味を持っている。"
                },
                {
                    "name": "山田美咲BBBB",
                    "background": "25歳女性。マーケティング部門で働くデジタルマーケティングスペシャリスト。AIの活用によるデータ分析に関心があり、SNSを通じたプロモーション戦略を担当している。最近、AIツールを使ったキャンペーンの効果測定に取り組んでいる。"
                },
                {
                    "name": "鈴木一郎CCCC",
                    "background": "45歳男性。経営戦略部門のマネージャー。AIのビジネス活用に関する豊富な知識を持ち、企業の成長戦略を策定する役割を担っている。技術的なバックグラウンドはないが、AIのトレンドに敏感で、業界の動向を常に追っている。"
                }
            ],
            "persona_confirmed": False,
            "interview_result": [],
            "iteration": 1,
            "is_satisfied": False
        }
        print("result finally",result)
        return result
