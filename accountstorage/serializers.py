import base64

from rest_framework import serializers

from accountstorage.encrypt import encrypt_password

from .models import Account, WebAccount, SSHAccount, DatabaseAccount


class WebAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebAccount
        fields = ['link', ]


class SSHAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SSHAccount
        fields = ['link', ]


class DatabaseAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatabaseAccount
        fields = ['host', 'type',]


class AccountSerializer(serializers.ModelSerializer):
    ACCOUNT_TYPE_MODEL_MAP = {
        'web': WebAccount,
        'ssh': SSHAccount,
        'database': DatabaseAccount,
    }

    web = WebAccountSerializer(required=False)
    ssh = SSHAccountSerializer(required=False)
    db = DatabaseAccountSerializer(required=False)

    class Meta:
        model = Account
        fields = [
            'id', 'label', 'username', 'password', 'notes', 'type',
            'created_at', 'updated_at', 'web', 'ssh', 'db',
        ]

    def create(self, validated_data):
        # Extract the specific type account data (e.g. link of a web portal)
        account_type = validated_data['type']
        type_data = validated_data.pop(account_type)

        # Extract the encryption key and encrypt the password
        encryption_key = self.context['request'].META['HTTP_X_ENCRYPTION_KEY']
        plain_text_password = validated_data.pop('password')
        encrypted_password = encrypt_password(plain_text_password, encryption_key)
        validated_data['password'] = encrypted_password

        # Create the base account record
        authenticated_user = self.context['request'].user
        account = Account.objects.create(**validated_data, user=authenticated_user)

        # Create the specific account type record (e.g. web portal record)
        Model = self.ACCOUNT_TYPE_MODEL_MAP[account_type]
        Model.objects.create(**type_data, account=account)

        return account

    def update(self, instance, validated_data):
        # Extract the specific type account data (e.g. link of a web portal)
        account_type = validated_data['type']
        type_data = validated_data.pop(account_type)

        current_instance_type = instance.type
        instance_specific_type = getattr(instance, current_instance_type)
        if not (current_instance_type == account_type):
            # If the type changed, recreate the specific type record
            instance_specific_type.delete()
            Model = self.ACCOUNT_TYPE_MODEL_MAP[account_type]
            Model.objects.create(**type_data, account=instance)
            setattr(instance, current_instance_type, None)
        else:
            # Just update the specific type record
            instance_specific_type.__dict__.update(**type_data)
            instance_specific_type.save()

        # If a new password has been specified, encrypt and save the new password
        new_password = validated_data.pop('password', '')
        if new_password:
            encryption_key = self.context['request'].META['HTTP_X_ENCRYPTION_KEY']
            encrypted_password = encrypt_password(new_password, encryption_key)
            instance.password = encrypted_password

        # Update the other instance properties
        instance.__dict__.update(**validated_data)
        instance.save()

        return instance
