# Generated by Django 5.0.5 on 2024-05-08 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_rest', '0004_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='rating',
            field=models.FloatField(default=0),
        ),
    ]
