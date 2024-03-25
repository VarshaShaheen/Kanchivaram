from django.contrib.auth.models import User
from django.db import models


# Create your models here.

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
