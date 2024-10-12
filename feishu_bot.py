import json
import lark_oapi as lark
from lark_oapi.api.im.v1 import *
from config import FEISHU_APP_ID, FEISHU_APP_SECRET, FEISHU_VERIFICATION_TOKEN, FEISHU_ENCRYPT_KEY
from comfyui_api import generate_image
from utils import upload_image_to_feishu

# 创建 lark_oapi_client 实例
client = lark.Client.builder() \
    .app_id(FEISHU_APP_ID) \
    .app_secret(FEISHU_APP_SECRET) \
    .build()

def handler(headers, body):
    # 验证请求
    if not verify_request(headers, body):
        return {"status": "fail", "message": "Invalid request"}, 401

    # 解析事件
    event = json.loads(body)

    # 处理事件
    if event.get("type") == "url_verification":
        return handle_verification(event)
    elif event.get("type") == "event_callback":
        return handle_event(event)

    return {"status": "success"}, 200

def verify_request(headers, body):
    # 这里应该实现请求验证逻辑
    # 使用 FEISHU_VERIFICATION_TOKEN 和 FEISHU_ENCRYPT_KEY
    # 返回 True 如果验证通过，否则返回 False
    return True  # 临时返回 True，实际应该实现验证逻辑

def handle_verification(event):
    return {"challenge": event.get("challenge")}

def handle_event(event):
    event_type = event.get("event", {}).get("type")
    if event_type == "message":
        return handle_message(event)
    # 可以添加其他事件类型的处理
    return {"status": "success"}, 200

def handle_message(event):
    message = event.get("event", {}).get("message", {})
    chat_id = message.get("chat_id")
    content = json.loads(message.get("content", "{}")).get("text", "")

    # 发送等待消息
    send_message(chat_id, "正在生成图片，请稍候...")

    # 调用 ComfyUI API 生成图片
    image_path = generate_image(content)

    # 上传图片到飞书
    image_key = upload_image_to_feishu(image_path)

    # 发送图片消息
    send_image_message(chat_id, image_key, content)

    return {"status": "success"}, 200

def send_message(chat_id, content):
    req = CreateMessageRequest.builder() \
        .receive_id_type("chat_id") \
        .receive_id(chat_id) \
        .msg_type("text") \
        .content(json.dumps({"text": content})) \
        .build()
    
    resp = client.im.v1.message.create(req)
    if not resp.success():
        print(f"发送消息失败: {resp.msg}")

def send_image_message(chat_id, image_key, prompt):
    card_content = {
        "config": {"wide_screen_mode": True},
        "elements": [
            {
                "tag": "img",
                "img_key": image_key,
                "alt": {"tag": "plain_text", "content": prompt}
            },
            {
                "tag": "action",
                "actions": [
                    {
                        "tag": "button",
                        "text": {"tag": "plain_text", "content": "重新生成"},
                        "type": "primary",
                        "value": {"prompt": prompt}
                    }
                ]
            }
        ]
    }

    req = CreateMessageRequest.builder() \
        .receive_id_type("chat_id") \
        .receive_id(chat_id) \
        .msg_type("interactive") \
        .content(json.dumps(card_content)) \
        .build()
    
    resp = client.im.v1.message.create(req)
    if not resp.success():
        print(f"发送图片消息失败: {resp.msg}")
