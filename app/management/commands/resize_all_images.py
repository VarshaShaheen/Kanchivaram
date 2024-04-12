from django.core.management.base import BaseCommand
from app.models import Product

class Command(BaseCommand):
    help = 'Resize all images in the Product model'

    def handle(self, *args, **kwargs):
        products = Product.objects.all()

        for product in products:
            if product.image_pallu:
                product.image_pallu = product.create_webp(product.image_pallu)
            if product.image_body:
                product.image_body = product.create_webp(product.image_body)
            if product.image_border:
                product.image_border = product.create_webp(product.image_border)
            if product.image_blouse:
                product.image_blouse = product.create_webp(product.image_blouse)

            product.save()

        self.stdout.write(self.style.SUCCESS('All images resized successfully'))
