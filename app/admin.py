from django.contrib import admin
from .models import Category, Product, CartItem, Order, Herovideos, Gallery


admin.site.site_header = "Kanchivaram"
admin.site.site_title = "Kanchivaram Admin Portal"
admin.site.index_title = "Welcome to Kanchivaram"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'id', 'slug']
    search_fields = ['name']
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fields = ['user', 'payment', 'status', 'address', 'tracking_id', 'products']
    list_display = ['order_id', 'user', 'payment', 'status', 'address']
    readonly_fields = ['products']
    search_fields = ['user__email']

    def order_id(self, obj):
        return obj.id
    order_id.short_description = 'Order ID'
    order_id.admin_order_field = 'id'
    
    def products(self, obj):
        return "".join([str(f'Code: {product.code} Name: {product.name} \n ')  for product in obj.products])


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'category', 'mrp', 'stock']
    list_filter = ['category', 'color']
    search_fields = ['code', 'name', 'category__name']
    ordering = ['name']
    fields = ['code', 'name', 'description',
              ('cover_image', 'image_pallu', 'image_body', 'image_border', 'image_blouse'), 'color',
              'mrp', 'category', 'weight', 'length', 'fabric', 'stock']


admin.site.register(CartItem)
admin.site.register(Herovideos)
admin.site.register(Gallery)