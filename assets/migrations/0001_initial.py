# Generated by Django 4.2 on 2024-11-12 10:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AssetMaster',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('asset_based_id', models.CharField(max_length=10, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='DepartmentMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='RoleMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='UserMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('employee_id', models.IntegerField(unique=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.departmentmaster')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.rolemaster')),
            ],
        ),
        migrations.CreateModel(
            name='AssetCategoryDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.IntegerField()),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.assetmaster')),
            ],
        ),
    ]