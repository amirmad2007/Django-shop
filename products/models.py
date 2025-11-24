from django.db import models
from django.utils.text import slugify
from django.urls import reverse
# Create your models here.
class Category(models.Model):

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True)
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
