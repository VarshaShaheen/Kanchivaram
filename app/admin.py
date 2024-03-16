from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'id']
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'category', 'price', 'stock']
    list_filter = ['category', 'color']
    search_fields = ['code', 'name', 'category__name']
    ordering = ['name']
    fields = ['code', 'name', 'description', ('image_pallu', 'image_body', 'image_border', 'image_blouse'), 'color',
              'price', 'mrp', 'category', 'weight', 'length', 'fabric', 'stock']
