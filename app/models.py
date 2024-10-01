from django.contrib.auth.models import User
from django.db import models
from payment.models import Payment
from PIL import Image
from django.db.models.signals import post_save
from django.dispatch import receiver
import os
import logging
logger = logging.getLogger(__name__)


class Herovideos(models.Model):
    video = models.FileField(upload_to='hero_videos/')
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.id)


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    category_id = models.DecimalField(max_digits=4, decimal_places=0)
    image = models.ImageField(upload_to='category/', blank=True, null=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


choice = (
    ('Order Placed', 'Order Placed'),
    ('Order Dispatched', 'Order Dispatched'),
    ('Order Cancelled', 'Order Cancelled'),

)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=50, default='Order Placed', choices=choice)
    address = models.ForeignKey('payment.Address', on_delete=models.CASCADE)
    tracking_id = models.CharField(max_length=50, blank=True, null=True)
    product_details = models.TextField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"User {self.user} with Payment ID - {self.payment}"
    
    @property
    def products(self):
        product_ids = self.product_details.split(',')
        products = Product.objects.filter(id__in=product_ids)
        return products


class Product(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='catalogue/')
    image_pallu = models.ImageField(upload_to='catalogue/')
    image_body = models.ImageField(upload_to='catalogue/', blank=True, null=True)
    image_border = models.ImageField(upload_to='catalogue/', blank=True, null=True)
    image_blouse = models.ImageField(upload_to='catalogue/', blank=True, null=True)
    cover_image_small = models.ImageField(upload_to='catalogue/')
    image_pallu_small = models.ImageField(upload_to='catalogue/', blank=True, null=True)
    image_body_small = models.ImageField(upload_to='catalogue/', blank=True, null=True)
    image_border_small = models.ImageField(upload_to='catalogue/', blank=True, null=True)
    image_blouse_small = models.ImageField(upload_to='catalogue/', blank=True, null=True)
    color = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    length = models.DecimalField(max_digits=5, decimal_places=2)
    fabric = models.CharField(max_length=100)
    mrp = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()


@receiver(post_save, sender=Product)
def create_webp(sender, instance, created, **kwargs):
    fields_to_update = []
    for field_name in ['image_pallu', 'image_body', 'image_border', 'image_blouse','cover_image']:
        image_field = getattr(instance, field_name)
        if image_field:
            path = image_field.path
            if not path.endswith('.webp'):
                img = Image.open(path).convert('RGB')
                img.thumbnail((2000, 2000), Image.LANCZOS)

                file_name, ext = os.path.splitext(path)
                webp_file_name = f"{file_name}.webp"
                webp_file_name_small = f"{file_name}_small.webp"

                img.save(webp_file_name, 'WEBP', quality=65)

                img.thumbnail((700, 700), Image.LANCZOS)
                img.save(webp_file_name_small, 'WEBP', quality=65)

                new_webp_rel_path = os.path.relpath(webp_file_name, 'media')
                new_webp_small_rel_path = os.path.relpath(webp_file_name_small, 'media')

                setattr(instance, field_name, new_webp_rel_path)
                setattr(instance, f"{field_name}_small", new_webp_small_rel_path)

                fields_to_update.append(field_name)
                fields_to_update.append(f"{field_name}_small")

                logger.debug(f"Converted {path} to {webp_file_name} and {webp_file_name_small}")

    if fields_to_update:
        instance.save(update_fields=fields_to_update)
        logger.debug(f"Updated fields: {fields_to_update}")


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name}"
