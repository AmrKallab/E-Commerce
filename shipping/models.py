from django.db import models

from django.conf import settings

# Create your models here.
class ShippingAddress(models.Model) :
     user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="shipping_addresses") 
     full_name = models.CharField(max_length=256,blank=False) 
     phone = models.CharField(max_length=256,blank=False) 
     city = models.CharField(max_length=256,blank=False) 
     address = models.CharField(max_length=256,blank=False) 
     street = models.CharField(max_length=256,blank=True) 
     building = models.CharField(max_length=256,blank=True) 
     apartment = models.CharField(max_length=256,blank=True) 
     notes = models.TextField() 
     created_at = models.DateTimeField(auto_now_add=True) 

     class Meta:
         ordering = ["-created_at"]

     def __str__(self):
         return f"{self.full_name} - {self.city}"