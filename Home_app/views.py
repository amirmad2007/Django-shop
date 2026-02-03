from django.shortcuts import render
from django.views.generic import TemplateView , FormView , ListView
from .forms import *
from django.urls import reverse_lazy
from products.models import *
# Create your views here.
class HomeView(TemplateView):
    template_name = 'index.html'

class CartView(TemplateView):
    template_name = 'cart.html'

class CheckoutView(TemplateView):
    template_name = 'checkout.html'

class DetailView(TemplateView):
    template_name = 'detail.html'

class ShopView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'shop.html'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['colors'] = Color.objects.all()
        context['sizes'] = Size.objects.all()
        return context
    
  
class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactUsForm
    success_url = reverse_lazy("contact")
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

