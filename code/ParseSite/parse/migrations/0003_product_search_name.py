# Generated by Django 3.2.9 on 2022-04-26 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parse', '0002_product_is_done'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='search_name',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
