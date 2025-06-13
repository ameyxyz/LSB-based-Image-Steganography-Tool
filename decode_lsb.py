from PIL import Image

def decode_lsb(encoded_image_path):
    """Decodes a message hidden using LSB encoding from an image."""
    img = Image.open(encoded_image_path)
    binary_message = ""
    width, height = img.size

    for y in range(height):
        for x in range(width):
            pixel = list(img.getpixel((x, y)))
            # Extract the least significant bit of the blue channel
            binary_message += str(pixel[2] & 1)

    # Split binary message into bytes and convert to characters
    message = ""
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i + 8]
        if byte == "00000000":  # Stop at null character
            break
        message += chr(int(byte, 2))

    # Extract original message and AES key from decoded_message
    parts = message.rsplit("\n", 2)  
    if len(parts) < 3:
        raise ValueError("Decoded message does not contain a valid ciphertext or key.")

    original_message, ciphertext, stored_key = parts

    return original_message, ciphertext, stored_key