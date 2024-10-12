from lark_oapi import Client
from lark_oapi.api.im.v1 import *
from config import APP_ID, APP_SECRET

client = Client.builder().app_id(APP_ID).app_secret(APP_SECRET).build()

async def upload_image_to_feishu(image_path):
    with open(image_path, 'rb') as f:
        request = CreateImageRequest.builder() \
            .request_body(CreateImageRequestBody.builder()
                .image_type("message")
                .image(f)
                .build()) \
            .build()
        
        response = await client.im.v1.image.create(request)
        return response.image_key
