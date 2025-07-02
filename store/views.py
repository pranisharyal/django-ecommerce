from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from .models import Order
from django.views import View
from django.shortcuts import render, redirect
from .forms import CheckoutForm
from .models import OrderItem
from cart.cart import Cart
from django.shortcuts import render
from .models import Product, Category
from cart.cart import Cart

# Create your views here.

class HomeView(ListView):
    model = Product
    template_name = "store/home.html"
    context_object_name = "products"

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.GET.get("category")
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["request"] = self.request  # To use in template
        return context
    

@login_required
def checkout(request):
    cart = Cart(request)
    return render(request, 'store/checkout.html', {'cart': cart})


class CheckoutView(View):
    def get(self, request):
        form = CheckoutForm()
        cart = Cart(request)
        return render(request, 'store/checkout.html', {'form': form, 'cart': cart})

    def post(self, request):
        cart = Cart(request)
        form = CheckoutForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    price=item['price']
                )

            cart.clear()
            return redirect('checkout_success')

        return render(request, 'store/checkout.html', {'form': form, 'cart': cart})

def checkout_success(request):
    return render(request, 'store/checkout_success.html')


@method_decorator(login_required, name='dispatch')
class UserOrderListView(ListView):
    model = Order
    template_name = 'store/orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')


@method_decorator(staff_member_required, name='dispatch')
class AdminOrderListView(ListView):
    model = Order
    template_name = 'store/admin_orders.html'
    context_object_name = 'orders'
    ordering = ['-created_at']


@method_decorator(staff_member_required, name='dispatch')
class AdminOrderDetailView(DetailView):
    model = Order
    template_name = 'store/admin_order_detail.html'
    context_object_name = 'order'

