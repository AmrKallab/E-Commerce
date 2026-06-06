from django.urls import path 
from .views import CartAPIView,AddToCartAPIView,UpdateCartItemAPIView,ClearAPIView

urlpatterns = [

    path("",CartAPIView.as_view(),name='cart'),
    path("add/",AddToCartAPIView.as_view(),name='add-to-cart'),
    path('items/<int:pk>/',UpdateCartItemAPIView.as_view(),name='update-cart-item'),
    path('clear/',ClearAPIView.as_view(),name='clear-cart'),

]