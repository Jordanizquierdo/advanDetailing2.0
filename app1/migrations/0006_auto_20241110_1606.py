# Generated by Django 3.2 on 2024-11-10 19:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0005_auto_20241110_1440'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='correo',
            field=models.CharField(max_length=45, null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='fecha_registro',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='encargado',
            name='apellido',
            field=models.CharField(max_length=45, null=True),
        ),
    ]
