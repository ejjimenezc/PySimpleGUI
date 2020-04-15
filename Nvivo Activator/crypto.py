import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

password = "nvivo12".encode()
salt = "securesalt".encode()
#salt = os.urandom(16)
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=default_backend()
)

key = base64.urlsafe_b64encode(kdf.derive(password))
f = Fernet(key)
token = f.encrypt("".encode())
#token = f.encrypt("aaaaa-bbbbb-ccccc-ddddd-eeeee".encode())

with open('nvivo.key','w+') as file:
        file.write(key.decode())
with open('nvivo.lic','w+') as file:
        file.write(token.decode())