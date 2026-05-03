from django.db import models

class Category(models.Model) :
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    class meta :
        ordering = ['name']

    def __str__(self):
        return self.name


# Create your models here.
class Product(models.Model) :
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products')

    name = models.CharField(max_length=256,blank=True,null=False)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


    class meta :
        ordering = ['-created_at']

    def __str__(self):
        return self.name