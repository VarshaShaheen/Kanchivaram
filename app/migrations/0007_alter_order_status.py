# Generated by Django 5.0.3 on 2024-04-16 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_rename_traking_id_order_tracking_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Order Placed', 'Order Placed'), ('Order Dispatched', 'Order Dispatched'), ('Order Cancelled', 'Order Cancelled')], default='Order Placed', max_length=50),
        ),
    ]
