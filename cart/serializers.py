from rest_framework import serializers 
from .models import(Cart,CartItem)

class CartSerializer(serializers.ModelSerializer) :
    product_name = serializers.CharField(
        source="product.name",
        read_only=True
    )

    product_price = serializers.DecimalField(
        source="product.price",
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    subtotal = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    
    class Meta :
        model = Cart 
        fields = ['id','product_name','proudct_price','quantity','total_price']


    


class CartItemSerializer(serializers.ModelSerializer) :
    item = CartSerializer(read_only=True,many=True)
    total_price = serializers.DecimalField(source='get_total_price',max_digits=10,decimal_places=2,read_only=True)
    class Meta : 
        model = CartItem 
        fields = ['id','user','item','total_price','created_at']
        read_fields = ['user','created_at']

    
class AddToCartSerializer(serializers.Serializer) :
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

class UpdateCartItemSerializer(serializers.Serializer) :
    quantity = serializers.IntegerField(min_value=1)
    
