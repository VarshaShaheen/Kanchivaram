from django.contrib import admin
from .models import Category, Product, CartItem, Order




@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'id','slug']
    search_fields = ['name']
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fields = ['user', 'payment', 'status', 'address', 'product_details','tracking_id']
    list_display = ['user', 'payment', 'status', 'address']
    search_fields = ['user__email']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'category', 'mrp', 'stock']
    list_filter = ['category', 'color']
    search_fields = ['code', 'name', 'category__name']
    ordering = ['name']
    fields = ['code', 'name', 'description', ('image_pallu', 'image_body', 'image_border', 'image_blouse'), 'color',
              'mrp', 'category', 'weight', 'length', 'fabric', 'stock']


admin.site.register(CartItem)