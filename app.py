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
from fastapi.middleware.cors import CORSMiddleware
import os 

load_dotenv()

origins_env = os.getenv("ORIGINS")
if not origins_env:
    raise ValueError("ORIGINS environment variable is not set. Please set it in your .env file.")

origins = [a.strip() for a in origins_env.split(",")]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/scan")
async def scan_image(company_id:int, file: UploadFile = File(...)):
    try:
        # Read the file content
        contents = await file.read()
        # Process the image
        processed_image, original_format = await resize_image(contents)
        
        # Convert processed image to base64
        base64_image = base64.b64encode(processed_image).decode('utf-8')
        
        # Get inventory analysis
        inventory_data = get_json_inventory(base64_image, original_format, company_id)
        
        
        return JSONResponse(
            content={
                "items": inventory_data["items"],
                "status" : len(inventory_data["items"]) > 0 and 1 or 0,
                "message": len(inventory_data["items"]) > 0 and "Image processed and analyzed successfully" or "No items found in the image",
            },
            status_code=200
        )
    except Exception as e:
        return JSONResponse(
            content={"message": f"Error occurred: {str(e)} {traceback.format_exception(e)}"},
            status_code=500
        )