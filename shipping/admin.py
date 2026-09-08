from django.contrib import admin
from .models import ShippingAddress
# Register your models here.


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin) :
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
        "city",
        "created_at",
    ]

    search_fields = [
        "full_name",
        "phone",
        "city",
        "user__username",
        "user__email",
    ]

    ordering = ["-created_at"]