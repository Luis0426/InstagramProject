# Generated by Django 3.1.12 on 2024-11-29 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_instagram', '0002_auto_20241126_2154'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuarioinsta',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='usuarioinsta',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='usuarioinsta',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
        migrations.AlterField(
            model_name='usuarioinsta',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
    ]
