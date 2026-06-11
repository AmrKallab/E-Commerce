from django.urls import path

from .views import (CreateOrderAPIView,
                    OrderListAPIView,
                    OrderDetialAPIView,
                    AdminOrderListAPIView,
                    AdminOrderStatusUpdateAPIView)

urlpatterns = [
    path("create/",CreateOrderAPIView.as_view(),name='create-order'),
    path("", OrderListAPIView.as_view(), name="order-list"),
    path("<int:pk>",OrderDetialAPIView.as_view(),name='order-detail'),
    path("admin/", AdminOrderListAPIView.as_view(), name="admin-order-list"),
    path("admin/<int:pk>/status/", AdminOrderStatusUpdateAPIView.as_view(), name="admin-order-status-update"),
]