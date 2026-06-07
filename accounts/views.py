from django.shortcuts import render
from rest_framework.views import APIView 
from .serializers import (RegisterSerializer,UserSerializer)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
class RegisterAPIView(APIView) :
    
    def post(self,request) :
        serializer = RegisterSerializer(data=request.data) 
        if serializer.is_valid() :
            user = serializer.save()
            return Response({"user" :{
                         "id" : user.id , 
                         "username": user.username,
                         "email": user.email,}} ,
                status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class MeAPIView(APIView) :
    permission_classes = [IsAuthenticated] 

    def get(self,request) :
        serializer = UserSerializer(request.data) 
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )