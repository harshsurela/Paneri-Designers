# Generated by Django 3.2.9 on 2022-03-21 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0021_auto_20220320_1805'),
    ]

    operations = [
        migrations.AddField(
            model_name='sales',
            name='c_date',
            field=models.DateField(null=True),
        ),
    ]
