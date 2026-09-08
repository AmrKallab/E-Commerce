from django.db import models
from django.conf import settings
# Create your models here.
class ShippingAddress(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="shipping_addresses"
    )

    full_name = models.CharField(max_length=256)
    phone = models.CharField(max_length=30)
    city = models.CharField(max_length=256)
    address = models.CharField(max_length=256)
    street = models.CharField(max_length=256)
    building = models.CharField(max_length=256, blank=True)
    apartment = models.CharField(max_length=256, blank=True)
    notes = models.TextField(blank=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} - {self.city}"