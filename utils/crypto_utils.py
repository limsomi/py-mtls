from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

KEY = b'secretkey1234567'  # 16-byte key
IV = b'initialvector123'   # 16-byte IV

def encrypt(data: bytes) -> bytes:
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    encrypted = cipher.encrypt(pad(data, AES.block_size))
    return base64.b64encode(encrypted)

def decrypt(data: bytes) -> bytes:
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    decoded = base64.b64decode(data)
    return unpad(cipher.decrypt(decoded), AES.block_size)
