from fastapi import FastAPI, Request, Response
from lark_oapi import Client
from lark_oapi.api.event.v1 import *
from feishu_bot import handle_message, handle_card_action
from config import APP_ID, APP_SECRET, VERIFICATION_TOKEN, ENCRYPT_KEY, SERVER_HOST, SERVER_PORT

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
        
        if isinstance(event, ImMessageReceiveV1):
            await handle_message(client, event)
        elif isinstance(event, ImMessageActionV1):
            await handle_card_action(client, event)
        
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
