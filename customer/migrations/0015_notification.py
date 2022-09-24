# Generated by Django 3.2.4 on 2022-03-16 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0014_sales_d_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('not_title', models.CharField(max_length=150)),
                ('not_date', models.DateTimeField(auto_now=True)),
                ('not_read', models.BooleanField(default=False)),
            ],
        ),
    ]