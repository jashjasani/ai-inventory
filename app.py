from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import io
import base64
from chain import get_json_inventory
import json
from dotenv import load_dotenv
from utils import resize_image
import traceback

load_dotenv()


app = FastAPI()



@app.post("/scan")
async def scan_image(file: UploadFile = File(...)):
    try:
        # Read the file content
        contents = await file.read()
        
        # Process the image
        processed_image, original_format = await resize_image(contents)
        
        # Convert processed image to base64
        base64_image = base64.b64encode(processed_image).decode('utf-8')
        
        # Get inventory analysis
        inventory_json = get_json_inventory(base64_image, original_format)
        
        # Parse the inventory string to JSON if it's returned as a string
        if isinstance(inventory_json, str):
            inventory_data = json.loads(inventory_json)
        else:
            inventory_data = inventory_json
        
        # Get the size of the processed image
        img = Image.open(io.BytesIO(processed_image))
        width, height = img.size
        
        return JSONResponse(
            content={
                "data": inventory_data,
                "status" : len(inventory_data["items"]) > 0,
                "message": len(inventory_data["items"]) > 0 and "Image processed and analyzed successfully" or "No items found in the image",
            },
            status_code=200
        )
    except Exception as e:
        return JSONResponse(
            content={"message": f"Error occurred: {str(e)} {traceback.format_exception(e)}"},
            status_code=500
        )