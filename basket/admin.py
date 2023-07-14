from django.contrib import admin
from .models import BasketLine, Basket


# Register your models here.
@admin.register(BasketLine)
class BasketAdmin(admin.ModelAdmin):
    list_display = ("basket", "product", "quantity")


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ("user", "created_time")