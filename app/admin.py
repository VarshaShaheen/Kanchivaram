from django.contrib import admin
from .models import Category, Product, CartItem, Order




@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'id','slug']
    search_fields = ['name']
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fields = ['user', 'payment', 'status', 'address', 'display_cart_items','tracking_id']
    list_display = ['user', 'payment', 'status', 'address']
    readonly_fields = ['display_cart_items']  # Making it read-only
    search_fields = ['user__email']

    def display_cart_items(self, obj):
        cart_items = obj.payment.cart_items.all()
        return ", ".join([f"Name: {item.product.name} Code: {item.product.code}" for item in cart_items])

    display_cart_items.short_description = 'Cart Items'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related('payment__cart_items__product')  # Prefetch related products
        return queryset



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'category', 'mrp', 'stock']
    list_filter = ['category', 'color']
    search_fields = ['code', 'name', 'category__name']
    ordering = ['name']
    fields = ['code', 'name', 'description', ('image_pallu', 'image_body', 'image_border', 'image_blouse'), 'color',
              'mrp', 'category', 'weight', 'length', 'fabric', 'stock']


admin.site.register(CartItem)