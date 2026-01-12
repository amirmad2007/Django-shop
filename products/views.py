from django.shortcuts import render , get_object_or_404
from .models import Product
# Create your views here.
def detail(request,slug):
    product = get_object_or_404(Product, slug = slug)
    variants = product.variants.select_related('color', 'size').all()  # بهینه‌سازی
    variants_with_image = [v for v in variants if v.image]
     # لیست یونیک سایزها
    seen_sizes = set()
    unique_sizes = []
    for v in variants:
        if v.size.id not in seen_sizes:
            unique_sizes.append(v)
            seen_sizes.add(v.size.id)

    # لیست یونیک رنگ‌ها
    seen_colors = set()
    unique_colors = []
    for v in variants:
        if v.color.id not in seen_colors:
            unique_colors.append(v)
            seen_colors.add(v.color.id)

    context = {
        'product': product,
        'variants_with_image': variants_with_image,
        'unique_sizes': unique_sizes,
        'unique_colors': unique_colors,
    }
    return render(request, 'detail.html',context= context)
