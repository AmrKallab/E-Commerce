from django.contrib import admin
from django.urls import path ,include
from .views import ShippingAddressAPIView , ShippingAddressDetailAPIView
urlpatterns = [
    path('addresses/',ShippingAddressAPIView.as_view(),name='shipping-address'),
    path('addresses/<int:pk>/',ShippingAddressDetailAPIView.as_view(),name='shipping-address-detail'),
]
