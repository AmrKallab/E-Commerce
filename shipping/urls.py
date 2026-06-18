from django.urls import path
from .views import ShippingAddressListCreateAPIView , ShippingAddressDetailAPIView


urlpatterns = [
    path('addresses',ShippingAddressListCreateAPIView.as_view(),name="shipping-address-list-create"),
    path('addresses<int:pk>',ShippingAddressDetailAPIView.as_view(),name="shipping-address-detail"),

]