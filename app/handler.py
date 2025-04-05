import json
from modules.agent import PresentationAgent
from modules.config import model
from modules.config import get_db_url
from langgraph.checkpoint.postgres import PostgresSaver

def lambda_handler(event, context):
    with PostgresSaver.from_conn_string(get_db_url()) as checkpointer:
        checkpointer.setup()
        body = json.loads(event["body"])
        common_background = body["common_background"]
        user_background = body["user_background"]
        state = body["state"]
        agent = PresentationAgent(model,common_background,k=3,checkpointer=checkpointer)
        result = agent.run(user_background,state["thread_id"],state["persona_list"])
        print("result finally",result)

        # result の中身に Purpose インスタンスなどがあるため、手動で全部辞書化する
        # serialized = {
        #     "suggestions": [s.model_dump() for s in result["suggestions"]],
        #     "judge_reason": result["judge_reason"],
        #     "purpose": result["purpose"].model_dump() if "purpose" in result else None
        # }
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "OPTIONS,POST",
            },
            "body": json.dumps(result, ensure_ascii=False)
        }