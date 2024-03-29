from django.contrib import admin

from payment.models import Payment


# Register your models here.

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    fields = ['id', 'amount', 'currency', 'user', 'status','cart_items',]
    list_display = ['id', 'amount', 'currency', 'user', 'status', ]
    list_filter = ['status',]
    search_fields = ['id', 'user__email', 'user__full_name', ]
    readonly_fields = ['id']

