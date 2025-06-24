"""
Photo processing service for BOA API.

This module handles photo watermarking and image processing operations.
"""

import base64
import io
from PIL import Image, ImageDraw, ImageFont
from typing import Optional
from app.utils.exceptions import PhotoProcessingError
from app.utils.config import get_settings

settings = get_settings()


def add_watermark_to_photo(photo_data: str, transaction_id: str) -> str:
    """
    Add visible watermark to photo.
    
    Adds a visible watermark containing the BOA text and transaction ID
    to the bottom-right corner of the photo.
    
    Args:
        photo_data (str): Base64 encoded photo data
        transaction_id (str): Unique transaction ID for the watermark
        
    Returns:
        str: Base64 encoded photo data with watermark
        
    Raises:
        PhotoProcessingError: If photo processing fails
        
    Example:
        >>> watermarked = add_watermark_to_photo(photo_base64, "uuid-1234")
        >>> # Returns base64 string of watermarked photo
    """
    try:
        # Decode base64 photo data
        photo_bytes = base64.b64decode(photo_data)
        image = Image.open(io.BytesIO(photo_bytes))
        
        # Convert to RGBA if necessary (for transparency support)
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        
        # Create transparent overlay for watermark
        overlay = Image.new('RGBA', image.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Prepare watermark text
        watermark_text = f"{settings.watermark_text}\n{transaction_id[:8]}"
        
        # Try to use a built-in font, fallback to default if not available
        try:
            # Try to load a better font
            font_size = max(12, min(image.width // 30, 24))  # Responsive font size
            font = ImageFont.load_default()
        except Exception:
            font = ImageFont.load_default()
        
        # Calculate text size and position
        bbox = draw.textbbox((0, 0), watermark_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Position based on settings (default: bottom-right)
        margin = 10
        if settings.watermark_position == "bottom-right":
            x = image.width - text_width - margin
            y = image.height - text_height - margin
        elif settings.watermark_position == "bottom-left":
            x = margin
            y = image.height - text_height - margin
        elif settings.watermark_position == "top-right":
            x = image.width - text_width - margin
            y = margin
        elif settings.watermark_position == "top-left":
            x = margin
            y = margin
        else:  # Default to bottom-right
            x = image.width - text_width - margin
            y = image.height - text_height - margin
        
        # Draw semi-transparent background for text
        padding = 5
        bg_x1 = x - padding
        bg_y1 = y - padding
        bg_x2 = x + text_width + padding
        bg_y2 = y + text_height + padding
        
        draw.rectangle(
            [bg_x1, bg_y1, bg_x2, bg_y2],
            fill=(0, 0, 0, 128)  # Semi-transparent black background
        )
        
        # Draw watermark text
        draw.multiline_text(
            (x, y),
            watermark_text,
            fill=(255, 255, 255, 255),  # White text
            font=font,
            align="center"
        )
        
        # Composite the overlay onto the original image
        watermarked_image = Image.alpha_composite(image, overlay)
        
        # Convert back to RGB if needed (for JPEG output)
        if watermarked_image.mode == 'RGBA':
            # Create white background
            rgb_image = Image.new('RGB', watermarked_image.size, (255, 255, 255))
            rgb_image.paste(watermarked_image, mask=watermarked_image.split()[-1])
            watermarked_image = rgb_image
        
        # Convert back to base64
        output_buffer = io.BytesIO()
        watermarked_image.save(output_buffer, format='JPEG', quality=95)
        watermarked_base64 = base64.b64encode(output_buffer.getvalue()).decode('utf-8')
        
        return watermarked_base64
        
    except Exception as e:
        raise PhotoProcessingError(
            operation="watermarking",
            reason=f"Failed to add watermark: {str(e)}"
        )


def add_invisible_watermark(photo_data: str, transaction_id: str) -> str:
    """
    Add invisible steganographic watermark to photo.
    
    This function embeds the transaction ID invisibly into the photo
    using basic steganography techniques.
    
    Args:
        photo_data (str): Base64 encoded photo data
        transaction_id (str): Transaction ID to embed
        
    Returns:
        str: Base64 encoded photo data with invisible watermark
        
    Raises:
        PhotoProcessingError: If steganographic processing fails
        
    Note:
        This is a basic implementation. In production, more sophisticated
        steganography techniques should be used.
    """
    try:
        # Decode base64 photo data
        photo_bytes = base64.b64decode(photo_data)
        image = Image.open(io.BytesIO(photo_bytes))
        
        # Convert to RGB mode
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Get image data as a list of pixels
        pixels = list(image.getdata())
        
        # Convert transaction ID to binary
        binary_data = ''.join(format(ord(char), '08b') for char in transaction_id)
        binary_data += '1111111111111110'  # End marker
        
        # Embed data into least significant bits of red channel
        data_index = 0
        modified_pixels = []
        
        for pixel in pixels:
            if data_index < len(binary_data):
                # Modify the least significant bit of the red channel
                r, g, b = pixel
                r = (r & 0xFE) | int(binary_data[data_index])  # Clear LSB and set new bit
                modified_pixels.append((r, g, b))
                data_index += 1
            else:
                modified_pixels.append(pixel)
        
        # Create new image with modified pixels
        stegged_image = Image.new('RGB', image.size)
        stegged_image.putdata(modified_pixels)
        
        # Convert back to base64
        output_buffer = io.BytesIO()
        stegged_image.save(output_buffer, format='JPEG', quality=98)  # High quality to preserve data
        stegged_base64 = base64.b64encode(output_buffer.getvalue()).decode('utf-8')
        
        return stegged_base64
        
    except Exception as e:
        raise PhotoProcessingError(
            operation="invisible watermarking",
            reason=f"Failed to add invisible watermark: {str(e)}"
        )


def extract_invisible_watermark(photo_data: str) -> Optional[str]:
    """
    Extract invisible watermark from photo.
    
    Extracts the transaction ID that was embedded using add_invisible_watermark.
    
    Args:
        photo_data (str): Base64 encoded photo data with invisible watermark
        
    Returns:
        Optional[str]: Extracted transaction ID if found, None otherwise
        
    Raises:
        PhotoProcessingError: If extraction fails
    """
    try:
        # Decode base64 photo data
        photo_bytes = base64.b64decode(photo_data)
        image = Image.open(io.BytesIO(photo_bytes))
        
        # Convert to RGB mode
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Get image data as a list of pixels
        pixels = list(image.getdata())
        
        # Extract bits from least significant bit of red channel
        binary_data = ''
        for pixel in pixels:
            r, g, b = pixel
            binary_data += str(r & 1)  # Get LSB of red channel
        
        # Find end marker
        end_marker = '1111111111111110'
        end_index = binary_data.find(end_marker)
        
        if end_index == -1:
            return None  # No watermark found
        
        # Extract the embedded data
        embedded_binary = binary_data[:end_index]
        
        # Convert binary to string
        if len(embedded_binary) % 8 != 0:
            return None  # Invalid data length
        
        extracted_text = ''
        for i in range(0, len(embedded_binary), 8):
            byte = embedded_binary[i:i+8]
            extracted_text += chr(int(byte, 2))
        
        return extracted_text
        
    except Exception as e:
        raise PhotoProcessingError(
            operation="invisible watermark extraction",
            reason=f"Failed to extract invisible watermark: {str(e)}"
        )


def validate_photo_format(photo_data: str) -> bool:
    """
    Validate that photo data is in a supported format.
    
    Args:
        photo_data (str): Base64 encoded photo data
        
    Returns:
        bool: True if photo format is valid and supported
        
    Raises:
        PhotoProcessingError: If photo format validation fails
    """
    try:
        # Decode base64 photo data
        photo_bytes = base64.b64decode(photo_data)
        image = Image.open(io.BytesIO(photo_bytes))
        
        # Check if format is supported
        supported_formats = ['JPEG', 'JPG', 'PNG', 'BMP']
        if image.format not in supported_formats:
            raise PhotoProcessingError(
                operation="format validation",
                reason=f"Unsupported format: {image.format}. Supported: {supported_formats}"
            )
        
        # Basic integrity check
        image.verify()
        
        return True
        
    except Exception as e:
        raise PhotoProcessingError(
            operation="format validation",
            reason=f"Invalid photo format: {str(e)}"
        )


def get_photo_info(photo_data: str) -> dict:
    """
    Get information about a photo.
    
    Args:
        photo_data (str): Base64 encoded photo data
        
    Returns:
        dict: Photo information including size, format, mode
        
    Raises:
        PhotoProcessingError: If photo analysis fails
    """
    try:
        # Decode base64 photo data
        photo_bytes = base64.b64decode(photo_data)
        image = Image.open(io.BytesIO(photo_bytes))
        
        return {
            "width": image.width,
            "height": image.height,
            "format": image.format,
            "mode": image.mode,
            "size_bytes": len(photo_bytes),
            "size_base64": len(photo_data)
        }
        
    except Exception as e:
        raise PhotoProcessingError(
            operation="photo analysis",
            reason=f"Failed to analyze photo: {str(e)}"
        )
