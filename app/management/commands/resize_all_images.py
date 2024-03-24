from django.core.management.base import BaseCommand
from app.models import Product


class Command(BaseCommand):
    help = 'Resizes and saves all product images in the database'

    def handle(self, *args, **kwargs):
        products = Product.objects.all()

        for product in products:
            product.save()
            self.stdout.write(self.style.SUCCESS(f'Processed {product}'))
