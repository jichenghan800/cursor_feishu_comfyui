import aiohttp
import asyncio
import json
import base64
from config import COMFYUI_API_URL

async def generate_image(prompt: str) -> str:
    workflow = {
        "3": {
            "inputs": {
                "seed": 8566257,
                "steps": 20,
                "cfg": 8,
                "sampler_name": "euler",
                "scheduler": "normal",
                "denoise": 1,
                "model": ["4", 0],
                "positive": ["6", 0],
                "negative": ["7", 0],
                "latent_image": ["5", 0]
            },
            "class_type": "KSampler"
        },
        "4": {
            "inputs": {
                "ckpt_name": "sd_xl_base_1.0.safetensors"
            },
            "class_type": "CheckpointLoaderSimple"
        },
        "5": {
            "inputs": {
                "width": 1024,
                "height": 1024,
                "batch_size": 1
            },
            "class_type": "EmptyLatentImage"
        },
        "6": {
            "inputs": {
                "text": prompt,
                "clip": ["4", 1]
            },
            "class_type": "CLIPTextEncode"
        },
        "7": {
            "inputs": {
                "text": "bad, ugly, blurry",
                "clip": ["4", 1]
            },
            "class_type": "CLIPTextEncode"
        },
        "8": {
            "inputs": {
                "samples": ["3", 0],
                "vae": ["4", 2]
            },
            "class_type": "VAEDecode"
        },
        "9": {
            "inputs": {
                "filename_prefix": "ComfyUI",
                "images": ["8", 0]
            },
            "class_type": "SaveImage"
        }
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{COMFYUI_API_URL}/prompt", json={"prompt": workflow}) as response:
            prompt_id = (await response.json())['prompt_id']
        
        while True:
            async with session.get(f"{COMFYUI_API_URL}/history/{prompt_id}") as response:
                history = await response.json()
                if prompt_id in history:
                    break
            await asyncio.sleep(1)
        
        image_data = history[prompt_id]["outputs"]["9"]["images"][0]
        image_path = f"./outputs/{image_data['filename']}"
        
        return image_path
