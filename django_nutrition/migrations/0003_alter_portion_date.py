# Generated by Django 5.1 on 2024-09-02 07:26

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("django_nutrition", "0002_alter_portion_quantity"),
    ]

    operations = [
        migrations.AlterField(
            model_name="portion",
            name="date",
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
