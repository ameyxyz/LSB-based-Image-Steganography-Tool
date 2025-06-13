from PIL import Image

def encode_lsb(image_path, message):
    """Encodes a message into the least significant bits of an image."""
    # Open the image
    img = Image.open(image_path)

    # Convert image to RGB if it's not already in that mode
    if img.mode != 'RGB':
        img = img.convert('RGB')

    encoded_img = img.copy()
    width, height = img.size
    message += chr(0)  # Add a null character to indicate the end of the message
    binary_message = ''.join(format(ord(i), '08b') for i in message)

    data_index = 0
    for y in range(height):
        for x in range(width):
            if data_index < len(binary_message):
                pixel = list(img.getpixel((x, y)))
                # Modify the least significant bit of the blue channel
                pixel[2] = (pixel[2] & ~1) | int(binary_message[data_index])
                encoded_img.putpixel((x, y), tuple(pixel))
                data_index += 1
            else:
                return encoded_img  # Return the encoded image once done

    return encoded_img