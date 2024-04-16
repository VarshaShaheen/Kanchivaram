from django.contrib.auth.models import User
from django.db import models
import smtplib
import ssl
from dotenv import load_dotenv
import os

dotenv_path = '.env'
load_dotenv(dotenv_path)


def generate_id():
    import uuid
    key = uuid.uuid4().hex[:10]
    while True:
        if Payment.objects.filter(id=key).exists():
            key = uuid.uuid4().hex[:10]
        else:
            break
    return key


class Payment(models.Model):
    id = models.CharField(max_length=10, primary_key=True, unique=True, default=generate_id)
    amount = models.CharField(max_length=10)
    currency = models.CharField(max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, default="pending", choices=(("pending", "pending"), ("success", "success"),
                                                                         ("failed", "failed")))
    cart_items = models.ManyToManyField("app.CartItem")

    def __str__(self):
        return self.id


class State(models.Model):
    name = models.CharField(max_length=400)
    delivery_charge = models.DecimalField(max_digits=15, decimal_places=4)


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address_line_1 = models.CharField(max_length=1500)
    address_line_2 = models.CharField(max_length=1500)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.address_line_1}, {self.address_line_2}, {self.country}"


def send_email(message, receiver, subject):
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = os.getenv("EMAIL_HOST_USER")
    receiver_email = receiver
    password = os.getenv("EMAIL_HOST_PASSWORD")
    text = message
    message = f'Subject: {subject}\n\n{text}'

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()
        server.starttls(context=context)
        message = message.encode('utf-8')
        server.ehlo()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
