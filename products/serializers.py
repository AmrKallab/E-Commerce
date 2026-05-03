from rest_framework import serializers 
from .models import (Product,Category)

class CategorySerializer(serializers.Serializer) :

    class meta :
        model = Category 
        fields = ["id","name","description"]


class ProductSerializer(serializers.Serializer) :

    class meta : 
        model = Product
        fields = ["id", "name", "stock",'is_active',"description" ,"created_at","category",]
        
