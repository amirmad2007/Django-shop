from django.shortcuts import render , redirect , get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from products.models import ProductVariant
from .models import Cart , CartItem
# Create your views here.
@login_required 
def cart_detail(request):
    
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('variant__product', 'variant__color', 'variant__size').all()

    total_price = cart.total_price
    context = {
        'cart': cart,
        'items': items,
        'total_price': total_price,

    }
    return render(request, 'cart.html', context)


def add_to_cart(request):
    
    if request.method == "POST":
        color_id = request.POST.get('color')
        size_id = request.POST.get('size')
        product_id = request.POST.get('product')

        variant = get_object_or_404(
            ProductVariant,
            product_id=product_id,
            color_id=color_id,
            size_id=size_id
        )

        cart, created = Cart.objects.get_or_create(user=request.user)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            variant=variant,
            defaults={'quantity': 1}
        )

        if not created:
            cart_item.quantity += 1
            cart_item.save()

    return redirect('cart')

def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('cart')  # یا نام view صفحه cart

