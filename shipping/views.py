from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from .models import (ShippingAddress)
from rest_framework.response import Response 
from .serializers import ShippingAddressSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated , IsAdminUser

# Create your views here.

class ShippingAddressAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        shipping_addresses = ShippingAddress.objects.filter(user=request.user)

        serializer = ShippingAddressSerializer(shipping_addresses,many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ShippingAddressSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)

            return Response(serializer.data,status=status.HTTP_201_CREATED)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class ShippingAddressDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self,pk,request) :

        shippingaddress = get_object_or_404(ShippingAddress,pk=pk,user=request.user) 

        return shippingaddress

    def get(self,request,pk) :

        shippingaddress = self.get_object(pk,request) 

        serializer = ShippingAddressSerializer(shippingaddress)

        return Response(serializer.data,status=status.HTTP_200_OK)
# PUT   → تحديث كامل للـ resource
# PATCH → تحديث جزئي
    def put(self,request,pk) :

        shippingaddress = self.get_object(pk,request) 

        serializer = ShippingAddressSerializer(shippingaddress,data=request.data) 
        if serializer.is_valid() :
            serializer.save() 
            return Response(serializer.data,status = status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def patch(self,request,pk) :
        
        shippingaddress = self.get_object(pk,request) 

        serializer = ShippingAddressSerializer(shippingaddress,data=request.data,partial=True) 
        if serializer.is_valid() :
            serializer.save() 
            return Response(serializer.data,status = status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk) :
        shippingaddress = self.get_object(pk,request) 

        shippingaddress.delete()

        return Response(status = status.HTTP_204_NO_CONTENT)

    