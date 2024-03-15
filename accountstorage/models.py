from django.conf import settings
from django.db import models
from cryptography.fernet import Fernet

from authentication.models import User
from accountstorage.encrypt import encrypt_password, decrypt_password

COMMON_MAX_LENGTH = 255
PASSWORD_MAX_LENGHT = 2048
LINK_MAX_LENGHT = 2048


class Account(models.Model):
    """An account stored in the system."""
    WEB = "web"
    SSH = "ssh"
    DATABASE = "database"
    ACCOUNT_TYPE_CHOICES = [
        (WEB, "Web portal"),
        (SSH, "SSH Server"),
        (DATABASE, "Database"),
    ]

    # The User who owns the account
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # The account informations
    label = models.CharField(max_length=COMMON_MAX_LENGTH)
    username = models.CharField(max_length=COMMON_MAX_LENGTH)
    notes = models.TextField()

    # The encrypted account password
    password = models.CharField(max_length=PASSWORD_MAX_LENGHT)

    # The account type
    type = models.CharField(
        max_length=COMMON_MAX_LENGTH,
        choices=ACCOUNT_TYPE_CHOICES,
    )

    # Generic informations
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_password = self.password

    def __str__(self) -> str:
        return self.label


class WebAccount(models.Model):
    """Additional account informations for web account"""
    account = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='web'
    )
    link = models.URLField()


class SSHAccount(models.Model):
    """Additional informations for a SSH server account"""
    account = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='ssh'
    )
    link = models.CharField(max_length=LINK_MAX_LENGHT)


class DatabaseAccount(models.Model):
    """Additional information for a database account"""
    MYSQL = "mysql"
    MARIADB = "mariadb"
    POSTGRESQL = "postgresql"
    ORACLE = "oracledb"
    OTHER = "other"
    DATABASE_TYPE_CHOICES = [
        (MYSQL, "MySQL"),
        (MARIADB, "MariaDB"),
        (POSTGRESQL, "PostgreSQL"),
        (ORACLE, "Orable Database"),
        (OTHER, "Other"),
    ]

    account = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='db'
    )
    host = models.CharField(max_length=LINK_MAX_LENGHT)
    type = models.CharField(
        max_length=COMMON_MAX_LENGTH,
        choices=DATABASE_TYPE_CHOICES
    )
