# Generated by Django 4.2 on 2024-11-12 11:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0008_alter_assetcategorydetails_asset_number'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='assetcategorydetails',
            unique_together={('employee_id', 'asset_number')},
        ),
    ]
