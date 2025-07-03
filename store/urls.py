from django.urls import path
from .views import HomeView, UserOrderListView, checkout_success
from . import views

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path('checkout/', views.checkout, name='checkout'),
     path('checkout/success/', checkout_success, name='checkout_success'),
    path('my-orders/', UserOrderListView.as_view(), name='my_orders'),
    path('admin-dashboard/orders/', views.AdminOrderListView.as_view(), name='admin_orders'),
    path('admin-dashboard/orders/<int:pk>/', views.AdminOrderDetailView.as_view(), name='admin_order_detail'),
]
