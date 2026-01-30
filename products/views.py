from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import JsonResponse
import random
from .models import Produk, Status
from .forms import ProdukForm

def hint_api(request):
    """
    Simple API endpoint to return a random hint for testing XHR requests.
    """
    hints = [
        "Tip: Use the 'Sellable Only' filter to check stock readiness.",
        "Did you know? Products are synced securely using MD5 hashing.",
        "You can update product prices directly from the Edit page.",
        "Deleting a product requires confirmation to prevent accidents.",
        "Check the Network tab to see this hint being fetched!",
        "The background sync ensures your local DB matches the server."
    ]
    return JsonResponse({
        'status': 'success',
        'hint': random.choice(hints),
        'timestamp': random.randint(100000, 999999)
    })


class ProductListView(ListView):
    model = Produk
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset().select_related('kategori', 'status')
        status_filter = self.request.GET.get('status')
        
        # Default Requirement: Display all, but filter "bisa dijual" is a feature.
        # Implemented as a toggle or link in UI.
        if status_filter == 'bisa_dijual':
            # Assuming the status name logic from API sync usually creates 'bisa dijual'
            # We filter loosely by string
            queryset = queryset.filter(status__nama_status__iexact='bisa dijual')
            
        return queryset.order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_only_sellable'] = self.request.GET.get('status') == 'bisa_dijual'
        return context

class ProductCreateView(CreateView):
    model = Produk
    form_class = ProdukForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('product-list')

class ProductUpdateView(UpdateView):
    model = Produk
    form_class = ProdukForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('product-list')

class ProductDeleteView(DeleteView):
    model = Produk
    success_url = reverse_lazy('product-list')
    
    # We don't generally need a template for delete if we use a modal or post request, 
    # but Django generic view expects one or we can override post.
    # For this test, we can just do a simple confirmation page or handle via JS/POST.
    # The requirement says "Delete action must show a JavaScript confirm() dialog" 
    # which implies the list view will handle the trigger, submitting to this view.
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
