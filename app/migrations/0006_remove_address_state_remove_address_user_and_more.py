# Generated by Django 5.0.3 on 2024-04-03 10:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_address_country'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='state',
        ),
        migrations.RemoveField(
            model_name='address',
            name='user',
        ),
        migrations.DeleteModel(
            name='Country',
        ),
        migrations.DeleteModel(
            name='State',
        ),
        migrations.DeleteModel(
            name='Address',
        ),
    ]