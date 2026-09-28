
from urllib import request

from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated , IsAdminUser

from cart.models import Cart
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderStatusUpdateSerializer
from shipping.models import ShippingAddress
from .serializers import CreateOrderSerializer
from products.models import Product , Category 

class CreateOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        shipping_address_id = serializer.validated_data["shipping_address_id"]
        payment_method = serializer.validated_data["payment_method"]

        # 1. Check shipping address
        try:
            shipping_address = ShippingAddress.objects.get(
                id=shipping_address_id,
                user=request.user
            )
        except ShippingAddress.DoesNotExist:
            return Response({"detail": "Shipping address not found."},status=status.HTTP_404_NOT_FOUND)

        # 2. Get user's cart
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response({"detail": "Cart not found."},status=status.HTTP_400_BAD_REQUEST)

        cart_items = cart.items.select_related("product").all()

        if not cart_items.exists():
            return Response({"detail": "Cart is empty."},status=status.HTTP_400_BAD_REQUEST)

        # 3. Start checkout transaction
        with transaction.atomic():

            locked_products = {}

            # 4. Lock and validate ALL products first
            for item in cart_items:

                product = Product.objects.select_for_update().get(pk=item.product_id)

                if item.quantity > product.stock:
                    transaction.set_rollback(True)

                    return Response({"detail":f"Not enough stock for {product.name}."},status=status.HTTP_400_BAD_REQUEST)

                locked_products[item.product_id] = product

            # 5. Only after validation create the order
            order = Order.objects.create(
                user=request.user,
                status=Order.Status.PENDING,
                shipping_address=shipping_address,
                payment_method=payment_method,
                payment_status=Order.PaymentStatus.UNPAID,
                total_price=0
            )

            total_price = 0

            # 6. Create OrderItems and decrease stock
            for item in cart_items:

                product = locked_products[item.product_id]

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    product_name=product.name,
                    quantity=item.quantity,
                    price=product.price
                )

                product.stock -= item.quantity

                product.save(update_fields=["stock"])

                total_price += item.quantity * product.price

            # 7. Save final total
            order.total_price = total_price

            order.save(update_fields=["total_price"])

            # 8. Clear cart
            cart.items.all().delete()

        # Transaction committed here

        serializer = OrderSerializer(order)

        return Response(serializer.data,status=status.HTTP_201_CREATED)

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

#الفكرة أن الـ dictionary يجيب عن سؤال:

#إذا كان الطلب في الحالة الحالية، إلى أي حالات يسمح له بالانتقال؟

ALLOWED_ORDER_TRANSITIONS = {
    Order.Status.PENDING: [
        Order.Status.CONFIRMED,
        Order.Status.CANCELLED,
    ],

    Order.Status.CONFIRMED: [
        Order.Status.PROCESSING,
        Order.Status.CANCELLED,
    ],

    Order.Status.PROCESSING: [
        Order.Status.SHIPPED,
        Order.Status.CANCELLED,
    ],

    Order.Status.SHIPPED: [
        Order.Status.DELIVERED,
    ],

    Order.Status.DELIVERED: [],

    Order.Status.CANCELLED: [],
}

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

        
        new_status = serializer.validated_data["status"]

        allowed_statuses = ALLOWED_ORDER_TRANSITIONS.get(new_status,[])
        if new_status not in allowed_statuses:
            return Response(
            {"detail": (f"Cannot change order status " f"from {order.status} to {new_status}.")},
            status=status.HTTP_400_BAD_REQUEST)
        
        with transaction.atomic() :
            if new_status == Order.Status.CANCELLED:
                for item in order.items.select_related("product"):
                    if item.product:
#select_for_update() داخل transaction.atomic() يقوم بقفل صف المنتج في قاعدة البيانات حتى تنتهي الـ transaction.
                        product = Product.objects.select_for_update().get(pk=item.product_id)
                        item.product.stock += item.quantity
                        item.product.save()
            order.status = new_status 

            if order.status == Order.status.Deliverd and order.payment_method == Order.PaymentMethod.CASH_ON_DELIVERY :
                order.payment_method = Order.status.PAID
            order.save()

        return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)