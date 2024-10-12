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
    print("Handler function called")
    print(f"Headers: {headers}")
    print(f"Body: {body}")

    if not verify_request(headers, body):
        print("Request verification failed")
        return {"status": "fail", "message": "Invalid request"}, 401

    try:
        event = json.loads(body)
    except json.JSONDecodeError:
        print("Failed to parse body as JSON")
        return {"status": "fail", "message": "Invalid JSON"}, 400

    print(f"Parsed event: {event}")

    if event.get("type") == "url_verification":
        print("Handling URL verification")
        return handle_verification(event)
    elif event.get("type") == "event_callback":
        print("Handling event callback")
        return handle_event(event)

    print("Unhandled event type")
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
    print("Handling message event")
    message = event.get("event", {}).get("message", {})
    chat_id = message.get("chat_id")
    content = json.loads(message.get("content", "{}")).get("text", "")

    print(f"Chat ID: {chat_id}")
    print(f"Message content: {content}")

    send_message(chat_id, "正在生成图片，请稍候...")

    try:
        image_path = generate_image(content)
        print(f"Generated image path: {image_path}")
    except Exception as e:
        print(f"Error generating image: {str(e)}")
        send_message(chat_id, "生成图片时出错，请稍后重试。")
        return {"status": "fail", "message": "Image generation failed"}, 500

    try:
        image_key = upload_image_to_feishu(image_path)
        print(f"Uploaded image key: {image_key}")
    except Exception as e:
        print(f"Error uploading image: {str(e)}")
        send_message(chat_id, "上传图片时出错，请稍后重试。")
        return {"status": "fail", "message": "Image upload failed"}, 500

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
