from django.urls import path

from .views import CreateOrderAPIView, OrderListAPIView,OrderDetialAPIView

urlpatterns = [
    path("create/",CreateOrderAPIView.as_view(),name='create-order'),
    path("", OrderListAPIView.as_view(), name="order-list"),
    path("<int:pk>",OrderDetialAPIView.as_view(),name='order-detail')
    
]