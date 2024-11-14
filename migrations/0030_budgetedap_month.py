# Generated by Django 5.0.7 on 2024-08-10 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rasmApp', '0029_accomplishment_budgetedap'),
    ]

    operations = [
        migrations.AddField(
            model_name='budgetedap',
            name='month',
            field=models.CharField(choices=[('1', 'ሐምሌ'), ('2', 'ነሃሴ'), ('3', 'መስከረም'), ('4', 'ጥቅምት'), ('5', 'ህዳር'), ('6', 'ታህሳስ'), ('7', 'ጥር'), ('8', 'የካቲት'), ('9', 'መጋቢት'), ('10', 'ሚያዚያ'), ('11', 'ግንቦት'), ('12', 'ሰኔ')], default='1', max_length=2),
        ),
    ]