# Generated by Django 4.0.2 on 2022-02-19 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0008_alter_producthasoffer_unique_together_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='app_desc',
            field=models.CharField(default='nothing', max_length=30),
            preserve_default=False,
        ),
    ]
