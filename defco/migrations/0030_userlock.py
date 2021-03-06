# Generated by Django 4.0.1 on 2022-05-13 19:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('defco', '0029_vehicleapproval_userapproval'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserLock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(default=False, on_delete=django.db.models.deletion.CASCADE, related_name='userlock', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
