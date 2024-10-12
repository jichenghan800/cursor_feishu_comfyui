import asyncio
from lark_oapi import Client
from lark_oapi.api.im.v1 import *
from comfyui_api import generate_image
from utils import upload_image_to_feishu
from config import APP_ID, APP_SECRET
import json

# 创建客户端
client = Client.builder().app_id(APP_ID).app_secret(APP_SECRET).build()

async def handle_card_event(event):
    try:
        action = event.get("action")
        if action.get("tag") == "button":
            open_id = event["open_id"]
            prompt = action["value"].get("prompt", "")
            
            # 生成图片
            image_path = await generate_image(prompt)
            
            # 上传图片到飞书
            image_key = await upload_image_to_feishu(image_path)
            
            # 更新消息卡片
            await update_card_message(event["open_message_id"], image_key, prompt)
    except Exception as e:
        print(f"Error handling event: {e}")

async def update_card_message(message_id, image_key, prompt):
    card = {
        "config": {
            "wide_screen_mode": True
        },
        "elements": [
            {
                "tag": "img",
                "img_key": image_key,
                "alt": {
                    "tag": "plain_text",
                    "content": prompt
                }
            },
            {
                "tag": "action",
                "actions": [
                    {
                        "tag": "button",
                        "text": {
                            "tag": "plain_text",
                            "content": "重新生成"
                        },
                        "type": "primary",
                        "value": {
                            "prompt": prompt
                        }
                    }
                ]
            }
        ]
    }
    
    request = PatchMessageRequest.builder() \
        .message_id(message_id) \
        .request_body(PatchMessageRequestBody.builder()
            .content(json.dumps(card))
            .build()) \
        .build()
    
    await client.im.v1.message.patch(request)

async def handle_event(event):
    print(f"Received event: {event}")
    # 根据事件类型执行相应的操作

async def handle_callback(event):
    print(f"Received callback: {event}")
    # 根据回调类型执行相应的操作
    return {"status": "ok"}
