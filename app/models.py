from django.contrib.auth.models import User
from django.db import models
from payment.models import Payment
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

country_charges = {
    "AFGHANISTAN (FED)": {"charge_1kg": 4000, "charge_additional_500g": 700},
    "ARGENTINA (FED)": {"charge_1kg": 4100, "charge_additional_500g": 600},
    "AUSTRALIA (DTDC)": {"charge_1kg": 2600, "charge_additional_500g": 500},
    "AUSTRIA (FED)": {"charge_1kg": 3800, "charge_additional_500g": 600},
    "ARMENIA (FED)": {"charge_1kg": 3800, "charge_additional_500g": 600},
    "AZERBAIJAN (FED)": {"charge_1kg": 4000, "charge_additional_500g": 700},
    "BAHRAIN (DTDC)": {"charge_1kg": 2700, "charge_additional_500g": 500},
    "BELGIUM (FED)": {"charge_1kg": 3800, "charge_additional_500g": 600},
    "BANGLADESH (DTDC)": {"charge_1kg": 2300, "charge_additional_500g": 500},
    "BRAZIL (FED)": {"charge_1kg": 4000, "charge_additional_500g": 700},
    "CAMBODIA (FED)": {"charge_1kg": 3900, "charge_additional_500g": 700},
    "CAMEROON (FED)": {"charge_1kg": 4100, "charge_additional_500g": 800},
    "CANADA (FED)": {"charge_1kg": 3800, "charge_additional_500g": 600},
    "CHILE (FED)": {"charge_1kg": 4100, "charge_additional_500g": 600},
    "CHINA (FED)": {"charge_1kg": 3800, "charge_additional_500g": 600},
    "COLOMBIA (FED)": {"charge_1kg": 3900, "charge_additional_500g": 700},
    "COSTA RICA (FED)": {"charge_1kg": 3900, "charge_additional_500g": 600},
    "CROATIA (FED)": {"charge_1kg": 3800, "charge_additional_500g": 700},
    "CZECH REP (FED)": {"charge_1kg": 3800, "charge_additional_500g": 700},
    "DENMARK (FED)": {"charge_1kg": 3800, "charge_additional_500g": 600},
    "EGYPT (FED)": {"charge_1kg": 3700, "charge_additional_500g": 500},
    "ETHOPIA (FED)": {"charge_1kg": 3900, "charge_additional_500g": 700},
    "FINLAND (FED)": {"charge_1kg": 3800, "charge_additional_500g": 700},
    "FRANCE (FED)": {"charge_1kg": 3800, "charge_additional_500g": 700},
    "GEORGIA (FED)": {"charge_1kg": 4000, "charge_additional_500g": 700},
    "GERMANY (FED)": {"charge_1kg": 4000, "charge_additional_500g": 600},
    "GHANA (FED)": {"charge_1kg": 4100, "charge_additional_500g": 600},
    "GREECE (FED)": {"charge_1kg": 3800, "charge_additional_500g": 600},
    "HONG KONG (FED)": {"charge_1kg": 3700, "charge_additional_500g": 700},
    "HUNGARY (FED)": {"charge_1kg": 3800, "charge_additional_500g": 600},
    "ICELAND (FED)": {"charge_1kg": 4000, "charge_additional_500g": 700},
    "INDONESIA (FED)": {"charge_1kg": 4000, "charge_additional_500g": 700},
    "IRAN (FED)": {"charge_1kg": 3900, "charge_additional_500g": 600},
    "IRAQ (FED)": {"charge_1kg": 3800, "charge_additional_500g": 600},
    "IRELAND (FED)": {"charge_1kg": 3800, "charge_additional_500g": 600},
    "ISRAEL (FED)": {"charge_1kg": 4000, "charge_additional_500g": 700},
    "ITALY (FED)": {"charge_1kg": 3800, "charge_additional_500g": 600},
    "JAMAICA (FED)": {"charge_1kg": 4000, "charge_additional_500g": 700},
    "JAPAN (FED)": {"charge_1kg": 3800, "charge_additional_500g": 600},
    "JORDAN (FED)": {"charge_1kg": 3700, "charge_additional_500g": 600},
    "KAZAKHSTAN (FED)": {"charge_1kg": 3800, "charge_additional_500g": 600},
    "KENYA (FED)": {"charge_1kg": 4100, "charge_additional_500g": 700},
    "KUWAIT (DTDC)": {"charge_1kg": 2700, "charge_additional_500g": 500},
    "LATVIA (FED)": {"charge_1kg": 4000, "charge_additional_500g": 600},
    "LEBANON (FED)": {"charge_1kg": 3800, "charge_additional_500g": 600},
    "LIBIYA (FED)": {"charge_1kg": 3900, "charge_additional_500g": 700},
    "LUXEMBOURG (FED)": {"charge_1kg": 3800, "charge_additional_500g": 600},
    "MALAYSIA (DTDC)": {"charge_1kg": 2100, "charge_additional_500g": 500},
    "MALDIVES (DTDC)": {"charge_1kg": 2200, "charge_additional_500g": 600},
    "MALTA (FED)": {"charge_1kg": 3900, "charge_additional_500g": 600},
    "MEXICO (FED)": {"charge_1kg": 3900, "charge_additional_500g": 700},
    "MOROCCO (FED)": {"charge_1kg": 4100, "charge_additional_500g": 700},
    "MYANMAR (FED)": {"charge_1kg": 3900, "charge_additional_500g": 600},
    "NEPAL (DTDC)": {"charge_1kg": 2000, "charge_additional_500g": 600},
    "NETHERLANDS (FED)": {"charge_1kg": 3800, "charge_additional_500g": 700},
    "NEW ZEALAND (FED)": {"charge_1kg": 4000, "charge_additional_500g": 600},
    "NIGERIA (FED)": {"charge_1kg": 4100, "charge_additional_500g": 800},
    "NORWAY (FED)": {"charge_1kg": 3800, "charge_additional_500g": 700},
    "OMAN (DTDC)": {"charge_1kg": 2700, "charge_additional_500g": 500},
    "PANAMA (FED)": {"charge_1kg": 3900, "charge_additional_500g": 800},
    "PERU (FED)": {"charge_1kg": 3900, "charge_additional_500g": 700},
    "PHILIPPINES (FED)": {"charge_1kg": 3800, "charge_additional_500g": 600},
    "POLAND (FED)": {"charge_1kg": 3900, "charge_additional_500g": 600},
    "PORTUGAL (FED)": {"charge_1kg": 3900, "charge_additional_500g": 600},
    "QATAR (DTDC)": {"charge_1kg": 2700, "charge_additional_500g": 600},
    "SAUDI (DTDC)": {"charge_1kg": 2200, "charge_additional_500g": 500},
    "SERBIA (FED)": {"charge_1kg": 3900, "charge_additional_500g": 700},
    "SINGAPORE (DTDC)": {"charge_1kg": 2000, "charge_additional_500g": 500},
    "SLOVAKIA (FED)": {"charge_1kg": 3900, "charge_additional_500g": 700},
    "SOUTH AFRICA (FED)": {"charge_1kg": 4000, "charge_additional_500g": 700},
    "SPAIN (FED)": {"charge_1kg": 3800, "charge_additional_500g": 600},
    "SRILANKA (DTDC)": {"charge_1kg": 2500, "charge_additional_500g": 500},
    "SWEDAN (FED)": {"charge_1kg": 3800, "charge_additional_500g": 600},
    "SWITZERLAND (FED)": {"charge_1kg": 3900, "charge_additional_500g": 700},
    "TAIWAN (FED)": {"charge_1kg": 3800, "charge_additional_500g": 600},
    "THAILAND (DTDC)": {"charge_1kg": 2300, "charge_additional_500g": 600},
    "TURKEY (FED)": {"charge_1kg": 3700, "charge_additional_500g": 700},
    "UAE (DTDC)": {"charge_1kg": 2200, "charge_additional_500g": 500},
    "UK (FED)": {"charge_1kg": 3800, "charge_additional_500g": 600},
    "USA (DTDC)": {"charge_1kg": 3200, "charge_additional_500g": 600},
    "URUGUAY (FED)": {"charge_1kg": 3800, "charge_additional_500g": 600},
    "YEMEN (FED)": {"charge_1kg": 3900, "charge_additional_500g": 700},
    "ZIMBAWE (FED)": {"charge_1kg": 4100, "charge_additional_500g": 800},
}

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
    country = models.CharField(max_length=100)  # Store country name as CharField

    def calculate_delivery_charge(self, weight):
        country_charge = country_charges.get(self.country)
        if country_charge:
            charge_1kg = country_charge["charge_1kg"]
            charge_additional_500g = country_charge["charge_additional_500g"]
            total_charge = charge_1kg + ((weight - 1) // 0.5) * charge_additional_500g
            return total_charge
        else:
            return None

    def __str__(self):
        return f"{self.address_line_1}, {self.address_line_2}, {self.country}"
