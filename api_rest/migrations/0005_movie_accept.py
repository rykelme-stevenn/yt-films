# Generated by Django 5.0.6 on 2024-05-30 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_rest', '0004_alter_rating_user_delete_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='accept',
            field=models.BooleanField(null=True),
        ),
    ]
