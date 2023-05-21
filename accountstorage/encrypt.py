from django.conf import settings
from cryptography.fernet import Fernet


def encrypt_password(plain_text_password) -> str:
    f = Fernet(settings.ENCRYPTION_KEY)
    encrypted_password = f.encrypt(plain_text_password.encode())
    return encrypted_password.decode()


def decrypt_password(encrypted_password) -> str:
    f = Fernet(settings.ENCRYPTION_KEY)
    plain_text_password_encoded = f.decrypt(encrypted_password.encode())
    return plain_text_password_encoded.decode()
