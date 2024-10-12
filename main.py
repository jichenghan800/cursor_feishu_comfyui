# 导入必要的模块
import os
from fastapi import FastAPI, Request
from dotenv import load_dotenv
from lark_oapi.api.im.v1 import *
from feishu_bot import handler
from config import SERVER_HOST, SERVER_PORT

# 加载环境变量
load_dotenv()

# 创建FastAPI应用实例
app = FastAPI()

# 定义处理飞书事件的路由
@app.post("/webhook/event")
async def handle_event(request: Request):
    # 获取请求头和请求体
    headers = dict(request.headers)
    body = await request.body()

    # 打印接收到的请求信息
    print(f"Received headers: {headers}")
    print(f"Received body: {body.decode()}")

    try:
        # 使用 handler 处理事件
        resp = handler(headers, body)
        return resp
    except Exception as e:
        # 如果事件处理失败，打印错误信息并返回 400 状态码
        print(f"事件处理失败: {str(e)}")
        return {"status": "fail", "message": "Event processing failed"}, 400

# 主程序入口
if __name__ == "__main__":
    import uvicorn
    
    # 使用uvicorn运行FastAPI应用
    uvicorn.run(app, host=SERVER_HOST, port=SERVER_PORT)
