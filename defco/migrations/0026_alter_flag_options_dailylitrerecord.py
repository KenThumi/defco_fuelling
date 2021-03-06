# Generated by Django 4.0.1 on 2022-04-30 09:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('defco', '0025_flag'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='flag',
            options={'ordering': ['-pk']},
        ),
        migrations.CreateModel(
            name='DailyLitreRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opening', models.IntegerField()),
                ('closing', models.IntegerField()),
                ('dipstick', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='daily_records', to='defco.station')),
            ],
            options={
                'ordering': ['-pk'],
            },
        ),
    ]
