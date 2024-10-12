import asyncio
from fastapi import FastAPI, Request, HTTPException
from feishu_bot import handle_card_event, handle_event, handle_callback
from config import WEBHOOK_URL, APP_ID, APP_SECRET, VERIFICATION_TOKEN, ENCRYPT_KEY, SERVER_HOST, SERVER_PORT
from lark_oapi import Client

app = FastAPI()

# 创建 Lark 客户端
client = Client.builder().app_id(APP_ID).app_secret(APP_SECRET).build()

@app.get("/")
async def root():
    return {"status": "ok", "message": "Server is running"}

@app.post("/webhook/event")
async def handle_webhook_event(request: Request):
    # 获取请求头和请求体
    headers = dict(request.headers)
    body = await request.body()

    # 打印接收到的请求信息（用于调试）
    print(f"Received headers: {headers}")
    print(f"Received body: {body.decode()}")

    # 处理事件回调
    try:
        # 使用 client 来验证和解析事件
        event = await client.event.verify(headers, body)
        print(f"Parsed event: {event}")

        # 根据事件类型处理不同的事件
        if event.header.event_type == "im.message.receive_v1":
            # 处理接收消息事件
            await handle_card_event(event.event)
        else:
            await handle_event(event)

        return {"status": "success"}
    except Exception as e:
        print(f"Error processing event: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/callback")
async def callback_webhook(request: Request):
    body = await request.body()
    headers = dict(request.headers)
    
    try:
        # 使用 client 来验证和解析事件
        event = await client.event.verify(headers, body)
        
        response = await handle_callback(event)
        return response
    except Exception as e:
        print(f"Error processing callback: {e}")
        raise HTTPException(status_code=400, detail="Invalid callback")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=SERVER_HOST, port=SERVER_PORT)
