# Generated by Django 3.2.4 on 2021-06-25 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shelfapi', '0009_alter_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image_path',
            field=models.URLField(null=True),
        ),
    ]
