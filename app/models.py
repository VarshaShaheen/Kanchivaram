from django.contrib.auth.models import User
from django.db import models
from payment.models import Payment
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile


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
    image_pallu = models.ImageField(upload_to='catalogue/')
    image_body = models.ImageField(upload_to='catalogue/')
    image_border = models.ImageField(upload_to='catalogue/')
    image_blouse = models.ImageField(upload_to='catalogue/')
    color = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    length = models.DecimalField(max_digits=5, decimal_places=2)
    fabric = models.CharField(max_length=100)
    mrp = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    def resize_image(self, image_field):
        img = Image.open(image_field)
        img.convert('RGB')
        img.thumbnail((2000, 2000), Image.LANCZOS)

        # Convert image to WebP format
        img_io_webp = BytesIO()
        img.save(img_io_webp, format='WEBP', quality=85)
        img_io_webp.seek(0)
        new_image_webp = ContentFile(img_io_webp.read(), name=image_field.name)

        return new_image_webp

    def save(self, *args, **kwargs):
        # Resize images if present
        if self.image_pallu:
            self.image_pallu = self.resize_image(self.image_pallu)
        if self.image_body:
            self.image_body = self.resize_image(self.image_body)
        if self.image_border:
            self.image_border = self.resize_image(self.image_border)
        if self.image_blouse:
            self.image_blouse = self.resize_image(self.image_blouse)

        super(Product, self).save(*args, **kwargs)

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
