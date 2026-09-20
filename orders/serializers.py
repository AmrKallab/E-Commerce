from rest_framework import serializers
from shipping.serializers import ShippingAddressSerializer
from .models import Order,OrderItem
class OrderItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    class Meta :
        fields = [
            "id",
            "product",
            "product_name",
            "price",
            "quantity",
            "subtotal",
            "payment_method",            
        ]

class OrderSerializer(serializers.ModelSerializer) :
    items = OrderItemSerializer(many=True ,read_only=True)
    shipping_address = ShippingAddressSerializer(read_only=True)
    payment_method = serializers.ChoiceField(choices=Order.PaymentMethod.choices)

    class Meta :
        fields = [
            "id",
            "status",
            "shipping_address",
            "payment_method",
            "payment_status",
            "total_price",
            "items",
            "created_at"]
        
class OrderStatusUpdateSerializer(serializers.Serializer) :
    status = serializers.ChoiceField(choices=Order.Status.choices)

class CreateOrderSerializer(serializers.Serializer):
    shipping_address_id = serializers.IntegerField()
    
    payment_method = serializers.ChoiceField(choices=Order.PaymentMethod.choices)