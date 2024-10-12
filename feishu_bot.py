import json
import logging
from lark_oapi import Client
from lark_oapi.api.im.v1 import *
from config import FEISHU_APP_ID, FEISHU_APP_SECRET, FEISHU_VERIFICATION_TOKEN, FEISHU_ENCRYPT_KEY
from comfyui_api import generate_image
from utils import upload_image_to_feishu

# 设置日志级别
logging.basicConfig(level=logging.DEBUG)

# 创建 lark_oapi_client 实例
client = Client.builder() \
    .app_id(FEISHU_APP_ID) \
    .app_secret(FEISHU_APP_SECRET) \
    .build()

def handler(headers, body):
    logging.debug("Handler function called")
    logging.debug(f"Headers: {headers}")
    logging.debug(f"Body: {body}")

    # 解析事件
    event = json.loads(body)

    # 处理事件
    if event.get("type") == "url_verification":
        return handle_verification(event)
    elif event.get("type") == "event_callback":
        return handle_event(event)

    return {"status": "success"}, 200

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

    logging.info(f"Chat ID: {chat_id}")
    logging.info(f"Message content: {content}")
    
    # 打印客户端输入的内容
    print(f"Client input: {content}")

    send_message(chat_id, "正在生成图片，请稍候...")

    try:
        image_path = generate_image(content)
        logging.info(f"Generated image path: {image_path}")
    except Exception as e:
        logging.error(f"Error generating image: {str(e)}")
        send_message(chat_id, "生成图片时出错，请稍后重试。")
        return {"status": "fail", "message": "Image generation failed"}, 500

    try:
        image_key = upload_image_to_feishu(image_path)
        logging.info(f"Uploaded image key: {image_key}")
    except Exception as e:
        logging.error(f"Error uploading image: {str(e)}")
        send_message(chat_id, "上传图片时出错，请稍后重试。")
        return {"status": "fail", "message": "Image upload failed"}, 500

    send_image_message(chat_id, image_key, content)

    return {"status": "success"}, 200

def send_message(chat_id, content):
    req = CreateMessageRequest.builder() \
        .receive_id_type("chat_id") \
        .receive_id(chat_id) \
        .msg_type("text") \
        .content('{"text":"' + content + '"}') \
        .build()
    
    resp = client.im.v1.message.create(req)
    if not resp.success():
        logging.error(f"发送消息失败: {resp.msg}")

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
        logging.error(f"发送图片消息失败: {resp.msg}")
