# Generated by Django 5.0.3 on 2024-04-13 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image_blouse_small',
            field=models.ImageField(blank=True, null=True, upload_to='catalogue/'),
        ),
        migrations.AddField(
            model_name='product',
            name='image_body_small',
            field=models.ImageField(blank=True, null=True, upload_to='catalogue/'),
        ),
        migrations.AddField(
            model_name='product',
            name='image_border_small',
            field=models.ImageField(blank=True, null=True, upload_to='catalogue/'),
        ),
        migrations.AddField(
            model_name='product',
            name='image_pallu_small',
            field=models.ImageField(blank=True, null=True, upload_to='catalogue/'),
        ),
    ]
