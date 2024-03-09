import base64

from django.conf import settings

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def generate_fernet_key_from_password(password: str):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=settings.ENCRYPTION_KEY_SALT.encode(),
        iterations=390000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


def encrypt_password(plain_text_password, encryption_key='') -> str:
    f = Fernet(settings.ENCRYPTION_KEY)
    if encryption_key:
        key = generate_fernet_key_from_password(encryption_key)
        f = Fernet(key)

    encrypted_password = f.encrypt(plain_text_password.encode())
    return encrypted_password.decode()


def decrypt_password(encrypted_password, encryption_key='') -> str:
    f = Fernet(settings.ENCRYPTION_KEY)
    if encryption_key:
        key = generate_fernet_key_from_password(encryption_key)
        f = Fernet(key)

    plain_text_password_encoded = f.decrypt(encrypted_password.encode())
    return plain_text_password_encoded.decode()
