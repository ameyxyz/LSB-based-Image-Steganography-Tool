import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random

# Constants
BLOCK_SIZE = 16

# Padding function for AES
def pad(s):
    return s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)

# Unpadding function for AES
def unpad(s):
    return s[:-ord(s[len(s) - 1:])]

# Function to generate a private key from a password
def get_private_key(password):
    # Use SHA-256 to hash the password to create a 32-byte key
    return hashlib.sha256(password.encode("utf-8")).digest()

# Function to encrypt data using AES
def encrypt(raw, password):
    private_key = get_private_key(password)
    raw = pad(raw)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    encrypted = iv + cipher.encrypt(raw.encode('utf-8'))
    return base64.b64encode(encrypted)

# Function to decrypt data using AES
def decrypt(enc, password):
    private_key = get_private_key(password)
    enc = base64.b64decode(enc)
    
    if len(enc) < 16:
        raise ValueError("Invalid encrypted message.")
    
    iv = enc[:16]
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    
    try:
        decrypted = unpad(cipher.decrypt(enc[16:])).decode('utf-8')
        return decrypted
    except Exception as e:
        raise ValueError("Decryption failed: Invalid key or corrupted ciphertext.")