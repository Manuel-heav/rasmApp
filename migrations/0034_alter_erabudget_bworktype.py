# Generated by Django 5.0.7 on 2024-08-16 06:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rasmApp', '0033_alter_erabudget_bproject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='erabudget',
            name='bworktype',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='rasmApp.maintenancetype'),
        ),
    ]
