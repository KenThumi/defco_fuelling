# Generated by Django 4.0.1 on 2022-02-26 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('defco', '0008_alter_fuelreplenish_options_transaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
