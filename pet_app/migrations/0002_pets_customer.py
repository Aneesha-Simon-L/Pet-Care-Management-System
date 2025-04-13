# Generated by Django 5.2 on 2025-04-10 11:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
        ('pet_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pets',
            name='customer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='customer.customer'),
            preserve_default=False,
        ),
    ]
