# Generated by Django 3.1.12 on 2024-11-27 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_instagram', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuarioinsta',
            name='usuario',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
