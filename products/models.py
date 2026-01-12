from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.core.exceptions import ValidationError
# Create your models here.
class Category(models.Model):

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    image = models.ImageField(upload_to="product_categories", blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        pass
        # return reverse("product_category", kwargs={"slug": self.slug})
    def save(self, *args, **kwargs):
        
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


    class Meta:
        verbose_name_plural = "Categories"

class Color(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(*args, **kwargs)

class Size(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super().save(*args, **kwargs)

class Product(models.Model):

    title = models.CharField( max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField( auto_now_add=True)
    updated_at  = models.DateTimeField( auto_now=True)
    category = models.ManyToManyField(Category, related_name='products')
    slug = models.SlugField(unique=True,blank=True)
    
    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})
    
    def save(self, *args, **kwargs):
        self.title = self.title.title()
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    def __str__(self):
        return self.title

class ProductManager(models.Manager):
    def available_products(self):
        return self.filter(is_active=True)

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=3)
    image = models.ImageField(upload_to='product_image', blank= True , null= True)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, blank=True, null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    def clean(self):
        if self.color and self.size:
            exists = ProductVariant.objects.filter(
                product=self.product,
                color=self.color,
                size=self.size
            ).exclude(pk=self.pk).exists()
            if exists:
                raise ValidationError("این ترکیب محصول، رنگ و سایز قبلا وجود دارد.")

    def save(self, *args, **kwargs):
        self.full_clean()  # اعتبارسنجی قبل از ذخیره
        if self.quantity < 0:
            self.is_active = False
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.title} - {self.color or 'No Color'} - {self.size or 'No Size'}"
