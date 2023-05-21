# Generated by Django 4.2.1 on 2023-05-21 19:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255)),
                ('username', models.CharField(max_length=255)),
                ('notes', models.TextField()),
                ('password', models.CharField(max_length=2048)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='DatabaseAccount',
            fields=[
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='db', serialize=False, to='accountstorage.account')),
                ('host', models.CharField(max_length=2048)),
                ('type', models.CharField(choices=[('mysql', 'MySQL'), ('mariadb', 'MariaDB'), ('postgresql', 'PostgreSQL'), ('oracledb', 'Orable Database'), ('other', 'Other')], max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='SSHAccount',
            fields=[
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='ssh', serialize=False, to='accountstorage.account')),
                ('link', models.CharField(max_length=2048)),
            ],
        ),
        migrations.CreateModel(
            name='WebAccount',
            fields=[
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='web', serialize=False, to='accountstorage.account')),
                ('link', models.URLField()),
            ],
        ),
    ]
