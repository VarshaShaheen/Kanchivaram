import os
from PIL import Image

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Compress all images from static folder to WebP'

    def handle(self, *args, **kwargs):
        static_dir = settings.STATIC_ROOT  # Assuming your static files are stored in STATIC_ROOT

        for root, dirs, files in os.walk(static_dir):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    image_path = os.path.join(root, file)

                    try:
                        with Image.open(image_path) as img:
                            output_path = image_path.split('.')[0] + '.webp'
                            img.save(output_path, 'webp', quality=80)
                            os.remove(image_path)  # Remove the original image file
                            os.rename(output_path, image_path)  # Rename the WebP file to original name
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Error processing {image_path}: {e}"))
                    else:
                        self.stdout.write(self.style.SUCCESS(f"Successfully converted {image_path} to WebP"))

        self.stdout.write(self.style.SUCCESS('All images compressed successfully'))
