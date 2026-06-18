from rest_framework import serializers 
from .models import Shipping

class ShippingSerializer(serializers.ModelSerializer) :

    class Meta :
        model = Shipping 
        fields = [
            "id",
            "phone",
            "city",
            "street",
            "building",
            "apartment",
            "notes",
            "is_default",
            "created_at",
        ]
        read_only_fields  = ["id","created_at"]

    

