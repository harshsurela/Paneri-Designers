# Generated by Django 4.0.2 on 2022-02-12 19:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='userbase',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.userbase'),
        ),
    ]
