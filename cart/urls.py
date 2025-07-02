from django.urls import path
from . import views
from .views import CheckoutView

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
]
