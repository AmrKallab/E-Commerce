from urllib import request

from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated , IsAdminUser

from cart.models import Cart
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderStatusUpdateSerializer,CreateOrderSerializer
from shipping.models import Shipping

class CreateOrderAPIView(APIView) :
    permission_classes = [IsAuthenticated]
    def post(self,request):
        serializer = CreateOrderSerializer(data=request.data) 
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        shipping_address_id = serializer.validated_data["shipping_address_id"]
        payment_method = serializer.validated_data["payment_method"] 

        try :
            shipping_address = Shipping.objects.get(id = shipping_address_id) 
        except Shipping.DoesNotExist:
            return Response(
                {"detail": "Shipping address not found."},
                status=status.HTTP_404_NOT_FOUND
            )


        try :
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist :
            return Response(status=status.HTTP_400_BAD_REQUEST)
         

        cart_item = cart.items.select_related("product").all()
        if not cart_item.exists() :
            return Response({"detail" : "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic() :
            order = Order.objects.create(user=request.user,
                                         status=Order.Status.PENDING,
                                         shipping_address=shipping_address,
                                         payment_method=payment_method,
                                         total_price=0,) 

            total_price = 0
            for item in cart_item :
                product = item.product 
                if item.quantity > product.stock :
                    transaction.set_rollback(True)
                    return Response({"detail" : f"Not enough stock for {product.name}"}, status=status.HTTP_400_BAD_REQUEST)
                OrderItem.objects.create(order=order,product=product,
                                         quantity=item.quantity,
                                         price=product.price,
                                         
                                         )
                product.stock -= item.quantity
                product.save()
                total_price += item.quantity * product.price 
                order.total_price = total_price
                order.save()
                cart.items.all().delete()
            serializer = OrderSerializer(order)
            return Response(serializer.data,status =status.HTTP_200_OK)

class OrderListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request) :
        orders = Order.objects.filter(user=request.user).prefetch_related("items").order_by("-created_at")

        serializer = OrderSerializer(orders, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

class OrderDetialAPIView(APIView):
    permission_classes = [IsAuthenticated]
 
    def get(self,request,pk) :
        try :
            orders = Order.objects.get(user=request.user,id=pk)
        except Order.DoesNotExist :
            return Response({"detail": "Order not found."},status=status.HTTP_404_NOT_FOUND)
        
        serializer = OrderSerializer(orders)
        return Response(serializer.data,status=status.HTTP_200_OK)

class AdminOrderListAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        orders = Order.objects.all().prefetch_related("items").order_by("-created_at")
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdminOrderStatusUpdateAPIView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response(
                {"detail": "Order not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = OrderStatusUpdateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        order.status = serializer.validated_data["status"]
        order.save()

        return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)