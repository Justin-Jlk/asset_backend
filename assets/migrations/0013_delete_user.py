# Generated by Django 4.2 on 2024-11-13 09:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0012_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]