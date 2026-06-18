from django.shortcuts import render
from rest_framework.views import APIView
from .models import Shipping 
from .serializers import ShippingSerializer
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


class ShippingAddressListCreateAPIView(APIView) :
    permission_classes = [IsAuthenticated]
    def get(self,request) :
        Addresses = Shipping.objects.filter(user = request.user)

        serializer = ShippingSerializer(Addresses,many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request) :
        serializer = ShippingSerializer(data=request.data)

        if serializer.is_valid() :
            serializer.save(user = request.user)

            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class ShippingAddressDetailAPIView(APIView) :
        
    permission_classes = [IsAuthenticated] 

    def get_object(self,request,pk) :
        try :
            return Shipping.objects.get(user=request.user , id = pk)

        except Shipping.DoesNotExist :
            return None
            
    def get(self,request,pk) :
        address = self.get_object(request,pk)

        if address is None :
            return Response({"detail": "Shipping address not found."},status=status.HTTP_400_BAD_REQUEST)
            
        serializer = ShippingSerializer(address) 
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,pk) :
        address = self.get_object(request,pk)
        if address is None :
            return Response({"detail": "Shipping address not found."},status=status.HTTP_404_NOT_FOUND)
            
        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
