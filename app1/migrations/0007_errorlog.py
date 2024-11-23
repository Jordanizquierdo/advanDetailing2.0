# Generated by Django 3.2 on 2024-11-23 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0006_auto_20241113_1532'),
    ]

    operations = [
        migrations.CreateModel(
            name='ErrorLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('error_type', models.CharField(max_length=255)),
                ('error_message', models.TextField()),
                ('stack_trace', models.TextField()),
            ],
        ),
    ]
