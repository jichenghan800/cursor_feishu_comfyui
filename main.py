from fastapi import FastAPI, Request, Response
from lark_oapi import Client
from lark_oapi.api.event.v1 import *
from config import APP_ID, APP_SECRET, VERIFICATION_TOKEN, ENCRYPT_KEY, SERVER_HOST, SERVER_PORT
import json
 

app = FastAPI()

# 创建 Lark 客户端
client = Client.builder().app_id(APP_ID).app_secret(APP_SECRET).build()

@app.post("/webhook/event")
async def webhook_event(request: Request):
    body = await request.body()
    headers = dict(request.headers)
    
    try:
        # 使用 SDK 提供的方法来验证和解析事件
        event = await client.event.v1.event.verify(headers, body)
        
        
            # 获取发送者的 open_id
        open_id = event.sender.sender_id.open_id
        
        # 创建回复消息
        request = client.im.v1.message.create_req() \
            .receive_id_type("open_id") \
            .receive_id(open_id) \
            .msg_type("text") \
            .content(json.dumps({"text": "已收到"})) \
            .build()
        
        # 发送回复消息
        await client.im.v1.message.create(request)
        
        return Response(content="", status_code=200)
    except Exception as e:
        print(f"Error processing event: {e}")
        return Response(content="Error", status_code=400)

@app.get("/")
async def root():
    return {"status": "ok", "message": "Server is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=SERVER_HOST, port=SERVER_PORT)
