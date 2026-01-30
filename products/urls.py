from django.urls import path
from .views import ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView, hint_api

urlpatterns = [
    path('api/hint/', hint_api, name='api-hint'),
    path('', ProductListView.as_view(), name='product-list'),
    path('create/', ProductCreateView.as_view(), name='product-create'),
    path('edit/<int:pk>/', ProductUpdateView.as_view(), name='product-edit'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='product-delete'),
]
