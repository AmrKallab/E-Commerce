from django.db import models
from django.conf import settings
from products.models import Product

# Create your models here.
class Order(models.Model) :
    class Status(models.TextChoices) :
        PENDING = "pending", "Pending"
        PAID = "paid", "Paid"
        SHIPPED = "shipped", "Shipped"
        DELIVERED = "delivered", "Delivered"
        CANCELLED = "cancelled", "Cancelled"

    class PaymentMethod(models.TextChoices):
        CASH_ON_DELIVERY = "cash_on_delivery", "Cash on Delivery"
        STRIPE = "stripe", "Stripe"
        
    status = models.CharField(max_length = 20 , choices = Status.choices , default=Status.PENDING)
    user = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete = models.CASCADE,related_name="orders") 
    created_at = models.DateTimeField(auto_now_add = True)
    total_price = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    payment_method = models.CharField(max_length=30,choices=PaymentMethod.choices,default=PaymentMethod.CASH_ON_DELIVERY)


    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

class OrderItem(models.Model) :
    order = models.ForeignKey(Order , on_delete = models.CASCADE,related_name="items")
    product = models.ForeignKey(Product , on_delete = models.CASCADE)
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order #{self.order.id}"
    
    @property
    def total_price(self) :
        return self.quantity * self.price 
    
