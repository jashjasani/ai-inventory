import openai
import os 
from prompts import INVENTORY_PROMPT
import config

def get_json_inventory(image_base64 : bytes, original_format: str):

    client = openai.OpenAI(
    
    base_url = "https://api.fireworks.ai/inference/v1",
    api_key = os.environ["FIREWORKS_API_KEY"],
    )
    response = client.chat.completions.create(
    temperature=config.TEMPERATURE,
    response_format={ "type": "json_object" },
    model = "accounts/fireworks/models/qwen2-vl-72b-instruct",
    messages = [{
        "role": "user",
        "content": [{
        "type": "text",
        "text": INVENTORY_PROMPT,
        }, {
        "type": "image_url",
        "image_url": {
            "url": f"data:image/{original_format};base64,{image_base64}"
        },
        }, ],
    }],
    )
    return response.choices[0].message.content
