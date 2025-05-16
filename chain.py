import openai
import os 
from prompts import INVENTORY_PROMPT
import config
from utils import get_items_for_company
import json
import time

def get_json_inventory(image_base64 : bytes, original_format: str, company_id:str):

    client = openai.OpenAI(
    base_url = "https://openrouter.ai/api/v1",
    api_key = os.environ["OPENROUTER_API_KEY"],
    )

    items_list, items_dict = get_items_for_company(company_id)
    response = client.chat.completions.create(
        temperature=config.TEMPERATURE,
        response_format={ "type": "json_object" },
        model = "mistralai/mistral-medium-3",   
        messages = [{
            "role": "user",
            "content": [{
            "type": "text",
            "text": INVENTORY_PROMPT.format(items="\n".join(items_list)),
            }, {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/{original_format.lower()};base64,{image_base64}"
            },
            }, ],
        }],
    )
    inventory_json = response.choices[0].message.content

    # Parse the inventory string to JSON if it's returned as a string
    if isinstance(inventory_json, str):
        inventory_data = json.loads(inventory_json.replace("```json", "").replace("```", ""))
    else:
        inventory_data = inventory_json
    
    for item in inventory_data["items"]:
        if item["inDb"]:
            name = item["name"]
            item_in_db : dict = items_dict[name]
            for key, value in item_in_db.items():
                if key not in item:
                    item[key] = value

        else:
            item["weight"]=None
            item["volume"]=None
            item["rooms"]=[]
            item["isCp"]=None
            item["isPbo"]=None
            item["isCarton"]=None

    return inventory_data