import aiohttp
from lark_oapi import Client
from config import feishu_client

async def upload_image_to_feishu(image_path: str) -> str:
    with open(image_path, "rb") as f:
        image_data = f.read()
    
    response = await feishu_client.im.v1.image.create({
        "image_type": "message",
        "image": image_data
    })
    
    return response.data.image_key

