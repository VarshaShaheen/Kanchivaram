from django.contrib import admin

from payment.models import Payment, Address
from app.models import Order

# Register your models here.
admin.site.register(Order)
admin.site.register(Address)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    fields = ['id', 'amount', 'currency', 'user', 'status', 'cart_items', ]
    list_display = ['id', 'amount', 'currency', 'user', 'status', ]
    list_filter = ['status', ]
    search_fields = ['id', 'user__email', 'amount']
    readonly_fields = ['id']
