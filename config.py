import os
from dotenv import load_dotenv

load_dotenv()  # 加载 .env 文件中的环境变量

# 飞书应用配置
APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")

# Webhook配置
WEBHOOK_URL = "/webhook/card"

# ComfyUI配置
COMFYUI_API_URL = os.getenv("COMFYUI_API_URL", "http://localhost:8188")

# 加密策略
ENCRYPT_KEY = os.getenv("ENCRYPT_KEY")
VERIFICATION_TOKEN = os.getenv("VERIFICATION_TOKEN")

# 事件配置
EVENT_WEBHOOK_URL = "/event"

# 回调配置
CALLBACK_WEBHOOK_URL = "/callback"

# 服务器配置
SERVER_HOST = "0.0.0.0"  # 监听所有网络接口
SERVER_PORT = int(os.getenv("SERVER_PORT", 9000))

# 开发者服务器配置
DEVELOPER_SERVER_URL = os.getenv("DEVELOPER_SERVER_URL")

# 其他配置...
