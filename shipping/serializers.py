from rest_framework import serializers 
from .models import(ShippingAddress)

class ShippingAddressSerializer(serializers.ModelSerializer) :
    class Meta :
        model = ShippingAddress 
        fields = [  'id', 
                    'full_name',
                    'phone', 
                    'city', 
                    'address', 
                    'street', 
                    'building', 
                    'apartment', 
                    'notes', 
                    'is_default', 
                    'created_at']

        read_only_fields = ['id', 'created_at']