from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    image_pallu = models.ImageField(upload_to='products/')
    image_body = models.ImageField(upload_to='products/')
    image_border = models.ImageField(upload_to='products/')
    image_blouse = models.ImageField(upload_to='products/')
    color = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    length = models.DecimalField(max_digits=5, decimal_places=2)
    fabric = models.CharField(max_length=100)
    mrp = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.code})"
