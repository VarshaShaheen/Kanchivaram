from django.contrib.auth.models import User
from django.db import models
from payment.models import Payment
from PIL import Image
from django.db.models.signals import post_save
from django.dispatch import receiver
import os


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    category_id = models.DecimalField(max_digits=4, decimal_places=0)
    image = models.ImageField(upload_to='category/', blank=True, null=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    image_pallu = models.ImageField(upload_to='catalogue/', blank=True, null=True)
    image_body = models.ImageField(upload_to='catalogue/', blank=True, null=True)
    image_border = models.ImageField(upload_to='catalogue/', blank=True, null=True)
    image_blouse = models.ImageField(upload_to='catalogue/', blank=True, null=True)
    color = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    length = models.DecimalField(max_digits=5, decimal_places=2)
    fabric = models.CharField(max_length=100)
    mrp = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.code})"


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name}"


choice = (
    ('Placed', 'Placed'),
    ('Cancelled', 'Cancelled'),
    ('Completed', 'Completed'),

)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=50, default='Placed', choices=choice)

    def __str__(self) -> str:
        return f"User {self.user} with Payment ID - {self.payment}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


@receiver(post_save, sender=Product)
def create_webp(sender, instance, created, **kwargs):
    if created:
        for field_name in ['image_pallu', 'image_body', 'image_border', 'image_blouse']:
            image_field = getattr(instance, field_name)
            if not image_field:
                continue

            path = image_field.path
            if path.endswith('.webp'):
                continue

            # Open the image and resize it to 2000x2000 pixels
            img = Image.open(path).convert('RGB')
            img.thumbnail((2000, 2000), Image.LANCZOS)

            # Convert the resized image to WebP format
            file_name, _ = os.path.splitext(path)
            webp_file_name = f"{file_name}.webp"
            img.save(webp_file_name, 'WEBP', quality=65)

            # Update the image field with the path to the WebP file
            setattr(instance, field_name, os.path.relpath(webp_file_name, 'media'))

        instance.save()