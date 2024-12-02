# Generated by Django 3.1.12 on 2024-11-27 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UsuarioInsta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.CharField(max_length=50, unique=True)),
                ('correo', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
    ]
