from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import JSONResponse
from PIL import Image
import io
import base64
from chain import get_json_inventory
import json
from dotenv import load_dotenv
from utils import resize_image, initialize_mongo_client, close_mongo_client
import traceback
from fastapi.middleware.cors import CORSMiddleware
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get and validate origins for CORS
origins_env = os.getenv("ORIGINS")
if not origins_env:
    raise ValueError("ORIGINS environment variable is not set. Please set it in your .env file.")
origins = [a.strip() for a in origins_env.split(",")]

# Initialize the application
app = FastAPI(
    title="Inventory Scanner API",
    description="API for scanning and analyzing inventory images",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/scan")
async def scan_image(company_id: int, file: UploadFile = File(...)):
    try:
        logger.info(f"Processing image for company ID: {company_id}")
        
        # Read the file content
        contents = await file.read()
        
        # Process the image
        processed_image, original_format = await resize_image(contents)
        
        # Convert processed image to base64
        base64_image = base64.b64encode(processed_image).decode('utf-8')
        
        # Get inventory analysis
        logger.info("Getting inventory analysis from image")
        inventory_data = get_json_inventory(base64_image, original_format, company_id)
        
        item_count = len(inventory_data["items"])
        logger.info(f"Analysis complete. Found {item_count} items.")
        
        return JSONResponse(
            content={
                "items": inventory_data["items"],
                "room_name" : inventory_data["room_name"],
                "status": 1 if item_count > 0 else 0,
                "message": "Image processed and analyzed successfully" if item_count > 0 else "No items found in the image",
            },
            status_code=200
        )
    except Exception as e:
        error_details = traceback.format_exc()
        logger.error(f"Error in scan_image: {str(e)}\n{error_details}")
        return JSONResponse(
            content={"message": f"Error occurred: {str(e)}", "status": 0},
            status_code=500
        )

# Health check endpoint
@app.get("/health")
async def health():
    return {"status": "healthy"}