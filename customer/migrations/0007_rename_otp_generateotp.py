# Generated by Django 4.0.2 on 2022-02-15 21:05

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customer', '0006_otp_userbase_alter_otp_otp'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='otp',
            new_name='generateotp',
        ),
    ]
