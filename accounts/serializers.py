from rest_framework import serializers 
from django.contrib.auth.models import User 

class RegisterSerializer(serializers.ModelSerializer) :
    password = serializers.CharField(write_only=True,min_length = 8)
    password_confirm = serializers.CharField(write_only=True,min_length = 8)

    class Meta :
        model = User 
        fields = ["id","username","email","password","password_confirm"] 

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"] :
            raise serializers.ValidationError({'password':'password dont match'})
        
        return attrs
    
    def create(self,validate_data) : 
        validate_data.pop("password_confirm")
        user = User.objects.create_user(
            username=validate_data["username"] , 
            email=validate_data.get("email"),
            password=validate_data["password"]
        )
        return user
    
class UserSerializer(serializers.ModelSerializer) :
    class Meta :
        model = User 
        fields = ["id","username","email"]