from django.contrib import admin
from .models import Shipping 
# Register your models here.

@admin.register(Shipping)
class ShippingAdmin(admin.ModelAdmin) :
    list_display = [
        "id",
        "user",
        "full_name",
        "phone",
        "city",
        "is_default",
        "created_at",
    ]
    list_filter = [
        "city" ,
        "created_at",
        "is_default",
    ]
    search_fields = [
        "full_name",
        "phone",
        "city",
        "user__username",
        "user__email",
    ]

    ordering = [
        "-created_at",
    ]
