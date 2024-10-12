import asyncio
from fastapi import FastAPI, Request, Response
from feishu_bot import handle_card_event, handle_event, handle_callback
from config import WEBHOOK_URL, APP_ID, APP_SECRET, VERIFICATION_TOKEN, ENCRYPT_KEY, SERVER_HOST, SERVER_PORT
from lark_oapi import Client

app = FastAPI()

# 创建 Lark 客户端
client = Client.builder().app_id(APP_ID).app_secret(APP_SECRET).build()

@app.get("/")
async def ping():
    return {"status": "ok", "message": "Server is running"}

@app.post("/webhook/card")
async def webhook_card(request: Request):
    # 立即返回 200 状态码
    asyncio.create_task(handle_webhook_card(request))
    return Response(status_code=200)

async def handle_webhook_card(request: Request):
    try:
        body = await request.body()
        headers = dict(request.headers)
        event = await client.event.verify(headers, body)
        # 处理卡片事件
        await handle_card_event(event)
    except Exception as e:
        print(f"Error handling card event: {e}")

@app.post("/webhook/event")
async def webhook_event(request: Request):
    body = await request.body()
    headers = dict(request.headers)
    
    try:
        event = await client.event.verify(headers, body)
        # 处理事件
        await handle_event(event)
        return {"message": "OK"}
    except Exception as e:
        print(f"Error processing event: {e}")
        return Response(status_code=400, content=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=SERVER_HOST, port=SERVER_PORT)
