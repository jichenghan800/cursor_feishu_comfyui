# 导入必要的模块
import asyncio  # 用于异步编程
from fastapi import FastAPI, Request  # 用于创建Web应用和处理HTTP请求
 
# 修改这一行，确保导入正确的处理函数
from feishu_bot import handler  # 导入自定义的消息处理和卡片操作处理函数
from config import feishu_client, SERVER_HOST, SERVER_PORT  # 从配置文件中导入飞书验证令牌和加密密钥
# 以上导入确保了我们有所有必要的工具来创建一个飞书机器人服务，
# 包括处理异步操作、创建Web服务器、处理飞书事件、以及使用正确的验证和加密方法

# 创建FastAPI应用实例
app = FastAPI()

# 定义处理飞书事件的路由
@app.post("/webhook/event")
async def handle_event(request: Request):
    # 从请求中获取JSON数据
    data = await request.json()
    
    # 修改这一行，使用正确的方法名
    resp = await handler.dispatch(data)
    
    # 返回处理结果
    return resp

# 主程序入口
if __name__ == "__main__":
    # 导入uvicorn服务器
    import uvicorn
    
    # 使用uvicorn运行FastAPI应用
    # 注意：这里的配置是用于开发环境，生产环境应该使用更安全的配置
    uvicorn.run(app, host=SERVER_HOST, port=SERVER_PORT)
