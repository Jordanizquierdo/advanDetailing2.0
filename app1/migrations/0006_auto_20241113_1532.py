# Generated by Django 3.2 on 2024-11-13 18:32

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0005_auto_20241113_1512'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clientes',
            name='vehiculo',
        ),
        migrations.AddField(
            model_name='vehiculo',
            name='cliente',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vehiculos', to='app1.clientes'),
        ),
        migrations.AlterField(
            model_name='clientes',
            name='fecha_registro',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True),
        ),
    ]
