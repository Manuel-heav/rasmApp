# Generated by Django 5.0.7 on 2024-07-19 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rasmApp', '0003_alter_rmbudget_segment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actionplan',
            name='forTheMonth',
            field=models.CharField(blank=True, choices=[('መስከረም', 'መስከረም'), ('ጥቅምት', 'ጥቅምት'), ('ህዳር', 'ህዳር'), ('ታህሳስ', 'ታህሳስ'), ('ጥር', 'ጥር'), ('የካቲት', 'የካቲት'), ('መጋቢት', 'መጋቢት'), ('ሚያዚያ', 'ሚያዚያ'), ('ግንቦት', 'ግንቦት'), ('ሰኔ', 'ሰኔ'), ('ሐምሌ', 'ሐምሌ'), ('ነሐሴ', 'ነሐሴ')], max_length=20, null=True),
        ),
    ]