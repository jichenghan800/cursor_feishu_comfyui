# 导入必要的模块
import os
from fastapi import FastAPI, Request, Response
from dotenv import load_dotenv
from lark_oapi.api.im.v1 import *
from feishu_bot import handler
from config import SERVER_HOST, SERVER_PORT
import json
import traceback

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
        print("Calling handler function...")
        resp = handler(headers, body)
        print(f"Handler response: {resp}")
        
        # 如果 resp 是一个元组，说明它包含状态码
        if isinstance(resp, tuple):
            print(f"Returning tuple response: {resp}")
            return Response(content=resp[0], status_code=resp[1])
        else:
            print(f"Returning non-tuple response: {resp}")
            return resp
    except Exception as e:
        print(f"事件处理失败: {str(e)}")
        print(f"Exception type: {type(e)}")
        print(f"Exception traceback: {traceback.format_exc()}")
        return Response(content=json.dumps({"status": "fail", "message": "Event processing failed"}), status_code=400)

# 主程序入口
if __name__ == "__main__":
    import uvicorn
    
    # 使用uvicorn运行FastAPI应用
    uvicorn.run(app, host=SERVER_HOST, port=SERVER_PORT)
