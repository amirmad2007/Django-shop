from django.db import models
from products.models import Product , Color , Size , ProductVariant
from accounts.models import MyUser as User
# Create your models here.

class Cart(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Cart of {self.user.username}"
    
    @property
    def total_price(self):
        return sum(item.variant.price * item.quantity for item in self.items.all())
    
    def clear(self):
        self.items.all().delete()


class CartItem(models.Model):

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    color = models.ForeignKey(Color, null=True, blank=True, on_delete=models.SET_NULL)
    size = models.ForeignKey(Size, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
         unique_together = ('cart', 'variant', 'color', 'size')