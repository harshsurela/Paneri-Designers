# Generated by Django 3.2.9 on 2022-03-18 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0018_rename_purachsedetails_purchasedetails'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesreturndetails',
            name='salRet_date',
            field=models.DateField(auto_now=True),
        ),
    ]