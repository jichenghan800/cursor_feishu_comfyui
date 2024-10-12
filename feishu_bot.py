import asyncio
from typing import Dict, Any
import lark_oapi as lark
from lark_oapi.api.im.v1 import *
from config import feishu_client, FEISHU_VERIFICATION_TOKEN, FEISHU_ENCRYPT_KEY
from comfyui_api import generate_image
from utils import upload_image_to_feishu

async def handle_message(event: P2ImMessageReceiveV1) -> None:
    message_content = event.event.message.content
    chat_id = event.event.message.chat_id
    
    # 解析用户输入的prompt
    prompt = message_content.strip()
    
    # 发送等待消息
    await send_message(chat_id, "正在生成图片,请稍候...")
    
    # 调用ComfyUI API生成图片
    image_path = await generate_image(prompt)
    
    # 上传图片到飞书
    image_key = await upload_image_to_feishu(image_path)
    
    # 发送图片消息
    await send_image_message(chat_id, image_key, prompt)

async def send_message(chat_id: str, content: str) -> None:
    request = CreateMessageRequest.builder() \
        .receive_id_type("chat_id") \
        .receive_id(chat_id) \
        .msg_type("text") \
        .content('{"text":"' + content + '"}') \
        .build()
    
    response = await feishu_client.im.v1.message.create(request)
    if not response.success():
        print(f"发送消息失败: {response.msg}")

async def send_image_message(chat_id: str, image_key: str, prompt: str) -> None:
    card_content = {
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
    
    request = CreateMessageRequest.builder() \
        .receive_id_type("chat_id") \
        .receive_id(chat_id) \
        .msg_type("interactive") \
        .content(lark.JSON.marshal(card_content)) \
        .build()
    
    response = await feishu_client.im.v1.message.create(request)
    if not response.success():
        print(f"发送图片消息失败: {response.msg}")

async def handle_card_action(action: Dict[str, Any]) -> None:
    chat_id = action["open_chat_id"]
    prompt = action["value"]["prompt"]
    
    # 重新生成图片
    await handle_message(P2ImMessageReceiveV1(event=lark.P2ImMessageReceiveV1Data(message=lark.P2MessageReceiveV1(chat_id=chat_id, content=prompt))))

# 创建事件处理器
handler = lark.EventDispatcherHandler.builder(FEISHU_ENCRYPT_KEY, FEISHU_VERIFICATION_TOKEN) \
    .register_p2_im_message_receive_v1(handle_message) \
    .build()
