# Generated by Django 5.0.1 on 2024-03-02 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_tdown', '0003_partida_divisoepartida_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='partida',
            name='nomePartida',
            field=models.CharField(default='', max_length=300),
            preserve_default=False,
        ),
    ]
