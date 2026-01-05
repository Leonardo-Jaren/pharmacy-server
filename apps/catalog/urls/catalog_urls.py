from django.urls import path
from apps.catalog.views.catalog_views import ProductViewSet, CategoryViewSet

# Products
product_list = ProductViewSet.as_view({'get': 'list', 'post': 'create'})
product_detail = ProductViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})
product_search = ProductViewSet.as_view({'get': 'search'})

# Categories
category_list = CategoryViewSet.as_view({'get': 'list', 'post': 'create'})
category_detail = CategoryViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})

urlpatterns = [
    path('products/', product_list),
    path('products/<int:pk>/', product_detail),
    path('products/search/', product_search),
    path('categories/', category_list),
    path('categories/<int:pk>/', category_detail),
]
