
from fastapi import Request, Response, HTTPException
from dotenv import load_dotenv
import os
from jose import jwt, JWTError
from base64 import b64decode
load_dotenv()
encryption_key = os.getenv("ENCRYPTION_KEY")
print("encryption_key",encryption_key)
ALGORITHM = "HS256"
def verify_jwt_from_cookie(request: Request):
    jwt_options = {
        'verify_signature': True,
        'verify_exp': False,
        'verify_nbf': False,
        'verify_iat': False,
        'verify_aud': False
    }

    decoded_encryption_key = b64decode(encryption_key.encode("utf-8"))
    print("request",request)
    jwt_token = request.cookies.get("jwt")  # 👈 Cookie から取得
    print("jwt_token",jwt_token)
    if not jwt_token:
        raise HTTPException(status_code=401, detail="JWT token not found in cookies")

    try:
        payload = jwt.decode(jwt_token, decoded_encryption_key, options=jwt_options,algorithms=[ALGORITHM])
        return payload  # user情報など
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid JWT token")



#         {
#     "common_background":"AIのベンチャー企業に勤めている",
#     "user_background":"",
#     "state":{
#         "thread_id":"",
#         "request_id": "",
#         "user_request": "AWSの勉強会を開催したい",
#         "persona_list": [],
#         "persona_confirmed": false,
#         "interview_result": [],
#         "iteration": 0,
#         "is_satisfied": false,
#         "presentation": null
#     }
# }