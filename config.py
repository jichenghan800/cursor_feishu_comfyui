import os
from dotenv import load_dotenv
import lark_oapi as lark

load_dotenv()  # 加载 .env 文件中的环境变量

# 飞书机器人配置
FEISHU_APP_ID = os.getenv("FEISHU_APP_ID")
FEISHU_APP_SECRET = os.getenv("FEISHU_APP_SECRET")
FEISHU_VERIFICATION_TOKEN = os.getenv("FEISHU_VERIFICATION_TOKEN")
FEISHU_ENCRYPT_KEY = os.getenv("FEISHU_ENCRYPT_KEY")

# 创建飞书 API Client
feishu_client = lark.Client.builder() \
    .app_id(FEISHU_APP_ID) \
    .app_secret(FEISHU_APP_SECRET) \
    .log_level(lark.LogLevel.DEBUG) \
    .build()

# Webhook配置
WEBHOOK_URL = "/webhook/card"

# ComfyUI配置
COMFYUI_API_URL = os.getenv("COMFYUI_API_URL", "http://127.0.0.1:8188")

# 加密策略
ENCRYPT_KEY = os.getenv("ENCRYPT_KEY")
VERIFICATION_TOKEN = os.getenv("VERIFICATION_TOKEN")

# 回调配置
 

# 服务器配置
SERVER_HOST = "0.0.0.0"   
SERVER_PORT = int(os.getenv("SERVER_PORT"))   

# 开发者服务器配置
DEVELOPER_SERVER_URL = os.getenv("DEVELOPER_SERVER_URL")

# 其他配置
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
