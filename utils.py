from PIL import Image
import io 
import imghdr


def get_image_format(image_data: bytes) -> str:
    """
    Detect the image format from the binary data
    """
    format_type = imghdr.what(None, image_data)
    if format_type is None:
        raise ValueError("Unrecognized image format")
    return format_type.upper()

def convert_to_supported_format(img: Image.Image, original_format: str) -> bytes:
    """
    Convert image to a format supported by the vision model while preserving quality
    """
    img_byte_arr = io.BytesIO()
    
    # If original format is PNG with transparency
    if original_format == 'PNG' and img.mode == 'RGBA':
        # Create a white background
        background = Image.new('RGB', img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3])  # 3 is the alpha channel
        img = background
    
    # Convert to RGB mode if necessary
    if img.mode not in ('RGB', 'L'):
        img = img.convert('RGB')
    
    # Save in original format if it's supported, otherwise default to JPEG
    try:
        if original_format in ('PNG', 'JPEG', 'JPG'):
            if original_format == 'PNG':
                img.save(img_byte_arr, format='PNG', optimize=True)
            else:
                img.save(img_byte_arr, format='JPEG', quality=95, optimize=True)
        else:
            img.save(img_byte_arr, format='JPEG', quality=95, optimize=True)
    except Exception as e:
        # Fallback to JPEG if there's any error
        img.save(img_byte_arr, format='JPEG', quality=95, optimize=True)
    
    return img_byte_arr.getvalue()

async def resize_image(image_data: bytes) -> tuple[bytes, str]:
    """
    Resize image if either dimension exceeds 1024 pixels while maintaining aspect ratio.
    Returns the processed image as bytes and the format.
    """
    try:
        # Detect original format
        original_format = get_image_format(image_data)
        
        # Open image from bytes
        img = Image.open(io.BytesIO(image_data))
        
        # Get original dimensions
        width, height = img.size
        
        # Check if resizing is needed
        if width > 1024 or height > 1024:
            # Calculate aspect ratio
            aspect_ratio = width / height
            
            if width > height:
                new_width = 1024
                new_height = int(1024 / aspect_ratio)
            else:
                new_height = 1024
                new_width = int(1024 * aspect_ratio)
                
            # Resize image
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Convert and return processed image
        processed_image = convert_to_supported_format(img, original_format)
        return processed_image, original_format
    
    except Exception as e:
        raise ValueError(f"Error processing image: {str(e)}")
