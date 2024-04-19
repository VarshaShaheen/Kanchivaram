# Generated by Django 5.0.3 on 2024-04-19 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_order_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='product_details',
        ),
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(related_name='orders', to='app.product'),
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]