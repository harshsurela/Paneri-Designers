# Generated by Django 4.0.2 on 2022-03-22 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0022_sales_c_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sales',
            name='d_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sales',
            name='note',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
