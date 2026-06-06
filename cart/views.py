from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

import cart
from .serializers import (CartItemSerializer,CartSerializer,AddToCartSerializer,UpdateCartItemSerializer) 
from .models import (Cart,CartItem)
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from rest_framework import serializers
from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated
# Create your views here.

class CartAPIView(APIView) :
    permission_classes = [IsAuthenticated]

    def get(self,request) :
        cart,created = Cart.objects.get_or_create(user=request.user) 
        serializer = CartSerializer(cart) 
        if serializer.is_valid() :
            return Response(serializer.data,status = status.HTTP_200_OK)
        
   


class AddToCartAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self,request) :
        serializer = AddToCartSerializer(data=request.data)
        if not serializer.is_valid() :
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

        product_id = serializer.validated_data['product_id'] 
        quantity = serializer.validated_data['quantity']
        try :
            product = Product.objects.get(id=product_id,is_active=True)
            

        except Product.DoesNotExist :
            return Response({'error':'Product not found'},status=status.HTTP_404_NOT_FOUND)
        
        if quantity > Product.stock :
            return Response({'error':'Insufficient stock'},status=status.HTTP_400_BAD_REQUEST)
        
        cart,created = Cart.objects.get_or_create(user=request.user)
        cart_item,created = CartItem.objects.get_or_create(cart=cart,product=product)
        if not created:
            new_quantity = cart_item.quantity + quantity

            if new_quantity > product.stock:
                return Response(
                    {"detail": "Not enough stock."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            cart_item.quantity = new_quantity
            cart_item.save()

        serializer = CartItemSerializer(cart)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

class UpdateCartItemAPIView(APIView) :
    permission_classes = [IsAuthenticated]
    
    def get_object(self,request,pk) :
        try :
            cart_item = CartItem.objects.get(id=pk,cart__user=request.user)
        
        except CartItem.DoesNotExist :
            return None
    
    def patch(self,request,pk) :
        cart_item  = self.get_object(request,pk)
        if cart_item  is None :
            return Response({'error':'Cart item not found'},status=status.HTTP_404_NOT_FOUND)
        
        serializer = UpdateCartItemSerializer(data=request.data)
        if not serializer.is_valid() :
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        quantity = serializer.validated_data['quantity']
        if quantity > cart_item.product.stock:
            return Response(
                {"detail": "Not enough stock."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        cart_item .quantity = quantity
        cart_item .save()

        cart_serializer = CartItemSerializer(cart_item.cart)
        return Response(cart_serializer.data,status=status.HTTP_200_OK)
    
    def delete(self,request,pk) :
        cart_item  = self.get_object(request,pk)
        if cart_item  is None :
            return Response({'error':'Cart item not found'},status=status.HTTP_404_NOT_FOUND)
        cart = cart_item.cart
        cart_item.delete()
        cart_serializer = CartItemSerializer(cart) 
        return Response(cart_serializer.data,status=status.HTTP_200_OK)

class ClearAPIView(APIView): 
    permission_classes = [IsAuthenticated]

    def delete(self,request) :
        cart,created = Cart.objects.get_or_create(user=request.user)
        cart.items.all().delete()
        return Response({'detail':'Cart cleared'},status=status.HTTP_200_OK)

    