from django.urls import path
from apps.sales.views.sales_views import SaleViewSet, SaleDetailViewSet

# Sales
sale_list = SaleViewSet.as_view({'get': 'list', 'post': 'create'})
sale_detail = SaleViewSet.as_view({'get': 'retrieve'})
sale_cancel = SaleViewSet.as_view({'post': 'cancel'})

# Sale Details
detail_list = SaleDetailViewSet.as_view({'get': 'list'})

urlpatterns = [
    path('', sale_list),
    path('<int:pk>/', sale_detail),
    path('<int:pk>/cancel/', sale_cancel),
    path('details/', detail_list),
]
