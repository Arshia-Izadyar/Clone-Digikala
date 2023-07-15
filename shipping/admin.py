from django.contrib import admin

from .models import Shipping

@admin.register(Shipping)
class ShippingAdmin(admin.ModelAdmin):
    list_display = ("user", "sending_date", "delivery_method")
    search_fields = ("user",)
