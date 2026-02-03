from django.shortcuts import render , get_object_or_404
from .models import Product , Color , Size , ProductVariant
from django.http import JsonResponse
# Create your views here.
def detail(request,slug):

    product = get_object_or_404(Product, slug = slug)
    variants = product.variants.select_related('color', 'size').all()  # بهینه‌سازی
    variants_with_image = [v for v in variants if v.image]
    colors = Color.objects.filter(productvariant__product=product).distinct()
    sizes = Size.objects.filter(productvariant__product=product).distinct()

    return render(request, 'detail.html',context= {'product' : product , 'variants_with_image' : variants_with_image , 'sizes' : sizes , 'colors' : colors })




def get_variant(request):

    product_id = request.GET.get('product_id')
    size_id = request.GET.get('size_id')
    color_id = request.GET.get('color_id')

    try:

        variant = ProductVariant.objects.get(
            product_id=product_id,
            size_id=size_id,
            color_id=color_id,
            is_active=True,
            quantity__gt=0 
        )

        return JsonResponse({
            'price': variant.price,
            'quantity': variant.quantity,
            'image': variant.image.url if variant.image else '',
        })
    
    except ProductVariant.DoesNotExist:
        return JsonResponse({
            'error': 'Variant not available', 
            'price': '-', 
            'quantity': 0
        })