from django.contrib import admin
from .models import *
# Register your models here.

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1  # چند خط جدید به صورت پیش‌فرض در Admin
    fields = ('color', 'size', 'price', 'quantity', 'image')
    readonly_fields = ()
    show_change_link = True

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_at', 'updated_at',)
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ProductVariantInline]
    search_fields = ('title',)
    list_filter = ('category',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','is_active')
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name',)