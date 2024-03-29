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
        # Open the image using Pillow
        img = Image.open(image_field)
        img.convert('RGB')

        # Resize the image
        img.thumbnail((2000, 2000), Image.Resampling.LANCZOS)
        img_io = BytesIO()
        img.save(img_io, format='JPEG', quality=85)
        img_io.seek(0)
        new_image = ContentFile(img_io.read(), name=image_field.name)

        # Return new image
        return new_image

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


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, blank=True, null=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class State(models.Model):
    name = models.CharField(max_length=400)
    delivery_charge = models.DecimalField(max_digits=15, decimal_places=4)


class Country(models.Model):
    name = models.CharField(max_length=400)
    delivery_charge = models.DecimalField(max_digits=15, decimal_places=3)


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address_line_1 = models.CharField(max_length=1500)
    address_line_2 = models.CharField(max_length=1500)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True, blank=True)
    pincode = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def calculate_delivery_charge(self):
        if self.country.name == 'India':
            return self.state.delivery_charge
