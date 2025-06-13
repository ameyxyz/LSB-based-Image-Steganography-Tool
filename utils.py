import os
from PIL import Image

def load_image(image_path):
    """Load an image from the specified file path."""
    try:
        return Image.open(image_path)
    except Exception as e:
        raise ValueError(f"Error loading image: {e}")

def calculate_image_properties(image):
    """Calculate and return properties of the image."""
    width, height = image.size
    size = os.path.getsize(image.filename) / 1024  # Size in KB
    resolution = f"{width} x {height}"
    num_pixels = width * height
    return {
        "size": size,
        "resolution": resolution,
        "num_pixels": num_pixels
    }

def can_message_fit(image, message):
    """Check if the message can fit in the image based on its pixel count."""
    width, height = image.size
    num_pixels = width * height
    # Each pixel can hold 3 bits (one for each RGB channel)
    max_message_length = num_pixels * 3 // 8  # Convert bits to bytes
    return len(message) <= max_message_length

def get_image_extension(image_path):
    """Return the file extension of the image."""
    return os.path.splitext(image_path)[1].lower()