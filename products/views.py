from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from .models import (Product,Category)
from rest_framework.response import Response 
from .serializers import ProductSerializer,CategorySerializer
from rest_framework import status
from django.shortcuts import get_object_or_404



class CategoryList(APIView) :
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    def get(self,request) :
        queryset = Category.objects.all() 
        serializer = self.serializer_class(queryset,many=True)
        return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
    
    def post(self,request) :
        serializer = CategorySerializer(data = request.data) 
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class CategoryDetail(APIView) :
    
    
    def get_object(self,pk) :
        try :
            return Category.objects.get(pk=pk)
        
        except Category.DoesNotExist :
            return None
            
    def get(self,request,pk) :
        queryset = self.get_object(pk)
        if queryset is None :

            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = CategorySerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self,request,pk) :
        category = self.get_object(pk)
        if category is None:
            return Response(
                {"detail": "Category not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = CategorySerializer(category,data=request.data)

        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def patch(self, request, pk):
        category = self.get_object(pk)

        if category is None:
            return Response(
                {"detail": "Category not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CategorySerializer(
            category,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk) :
        category = self.get_object(pk) 
        if category is None:
            return Response(
                {"detail": "Category not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        category.delete()
        return Response( 
            status=status.HTTP_204_NO_CONTENT
        )
    


class ProductList(APIView) :

    def get(self,request) :
        queryset = Product.objects.filter(is_active = True)
        serializer = ProductSerializer(queryset,many = True)
        
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request) :
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid() :
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class ProductDetail(APIView) :

    
    def get_object(self,pk) :
        try :
            return Product.objects.get(pk=pk)
        
        except Product.DoesNotExist :
            return None 

    def get(self,request,pk) :
        queryset = self.get_object(pk) 
        if queryset is None :
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(queryset)

        return Response(serializer.data,status=status.HTTP_200_OK)


    def put(self,request,pk) :
        queryset = self.get_object(pk) 

        if queryset is None :
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProductSerializer(queryset,data = request.data) 

        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self,request,pk) :
        queryset = self.get_object(pk) 

        if queryset is None :
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(queryset,
                                       data = request.data,
                                       partial=True) 
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self,request,pk) :
        queryset = self.get_object(pk) 

        if queryset is None :
            return Response(status=status.HTTP_404_NOT_FOUND)
        
     
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

        