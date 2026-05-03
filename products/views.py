from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from .models import (Product,Category)
from rest_framework.response import Response 
from .serializers import ProductSerializer,CategorySerializer
from rest_framework import status
class CategoryList(APIView) :
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    def get(self,request) :
        queryset = Category.objects.all() 
        serializer = self.serializer_class(queryset,many=True)
        return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
    
class CategoryDetail(APIView) :
    
    def get(self,request,pk) :
        try :
            queryset = Category.objects.get(pk=pk)
            
        except :
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(queryset)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

class ProductList(APIView) :

    def get(self,request) :
        queryset = Product.objects.filter(is_active = True)
        serializer = ProductSerializer(queryset,many = True)
        
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class ProductDetail(APIView) :

    def get(self,request,pk) :
        try :
            queryset = Product.objects.get(pk=pk,is_active= True)
        except :
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProductSerializer(queryset)
        return Response(serializer.data,status=status.HTTP_200_OK)
    


    
        



        