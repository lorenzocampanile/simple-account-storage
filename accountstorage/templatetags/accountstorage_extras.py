from django import template
from accountstorage.encrypt import decrypt_password

register = template.Library()


@register.filter
def decrypt(encrypted_password):
    """Decrypt the password"""
    return decrypt_password(encrypted_password)
