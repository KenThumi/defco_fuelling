# Generated by Django 4.0.1 on 2022-02-07 06:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('defco', '0005_station_fuelreplenish'),
    ]

    operations = [
        migrations.AddField(
            model_name='station',
            name='admin',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='station', to=settings.AUTH_USER_MODEL),
        ),
    ]