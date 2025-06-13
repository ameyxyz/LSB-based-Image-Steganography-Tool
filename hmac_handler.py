# hmac_handler.py
import hmac
import hashlib

def generate_hmac(key, message):
    """Generates an HMAC-SHA256 hash of the message using the given key."""
    key_bytes = key.encode('utf-8')
    message_bytes = message.encode('utf-8')
    hmac_obj = hmac.new(key_bytes, message_bytes, hashlib.sha256)
    return hmac_obj.hexdigest()

def verify_hmac(key, message, hmac_value):
    """Verifies the HMAC-SHA256 hash of the message against the given HMAC value."""
    generated_hmac = generate_hmac(key, message)
    return hmac.compare_digest(generated_hmac, hmac_value)  # Secure comparison
