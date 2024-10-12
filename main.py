import asyncio
from fastapi import FastAPI, Request, HTTPException
from feishu_bot import handle_card_event, handle_event, handle_callback
from config import WEBHOOK_URL, APP_ID, APP_SECRET, SERVER_HOST, SERVER_PORT
from lark_oapi import Client

app = FastAPI()

# 创建 Lark 客户端
client = Client.builder().app_id(APP_ID).app_secret(APP_SECRET).build()

@app.get("/")
async def root():
    return {"status": "ok", "message": "Server is running"}

@app.post(WEBHOOK_URL)
async def webhook(request: Request):
    body = await request.body()
    headers = dict(request.headers)
    
    print(f"Received headers: {headers}")
    print(f"Received body: {body.decode()}")
    
    try:
        # 验证请求
        event = client.event.parse(headers, body)
        
        # 处理事件
        if event.header.event_type == "im.message.receive_v1":
            await handle_card_event(event.event)
        else:
            await handle_event(event)
        
        return {"status": "ok"}
    except Exception as e:
        print(f"Error processing event: {e}")
        raise HTTPException(status_code=400, detail="Invalid event")

@app.post("/event")
async def event_webhook(request: Request):
    body = await request.body()
    headers = dict(request.headers)
    
    try:
        # 验证请求
        event = client.event.parse(headers, body)
        
        await handle_event(event)
        return {"status": "ok"}
    except Exception as e:
        print(f"Error processing event: {e}")
        raise HTTPException(status_code=400, detail="Invalid event")

@app.post("/callback")
async def callback_webhook(request: Request):
    body = await request.body()
    headers = dict(request.headers)
    
    try:
        # 验证请求
        event = client.event.parse(headers, body)
        
        response = await handle_callback(event)
        return response
    except Exception as e:
        print(f"Error processing callback: {e}")
        raise HTTPException(status_code=400, detail="Invalid callback")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=SERVER_HOST, port=SERVER_PORT)
