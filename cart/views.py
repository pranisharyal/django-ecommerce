from django.views.generic import FormView
from store.forms import CheckoutForm
from .cart import Cart
from store.models import Order, OrderItem, Product
from django.shortcuts import render, redirect, get_object_or_404


# Create your views here.


def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product)
    return redirect('cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})


class CheckoutView(FormView):
    template_name = 'store/checkout.html'
    form_class = CheckoutForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = Cart(self.request)  # ✅ Adds cart to template context
        return context
    def form_valid(self, form):
        cart = Cart(self.request)
        order = Order.objects.create(
            user=self.request.user,
            name=form.cleaned_data['name'],
            email=form.cleaned_data['email'], 
            address=form.cleaned_data['address'],
            phone=form.cleaned_data['phone'],
            total_price=cart.get_total_price()
        )

        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['price']
            )

        cart.clear()
        return redirect('home')  # or a 'thank you' page
