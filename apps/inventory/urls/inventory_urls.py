from django.urls import path
from apps.inventory.views.inventory_views import BatchViewSet, StockMovementViewSet

# Batches
batch_list = BatchViewSet.as_view({'get': 'list', 'post': 'create'})
batch_detail = BatchViewSet.as_view({'get': 'retrieve', 'put': 'update'})
batch_adjust = BatchViewSet.as_view({'post': 'adjust_stock'})
batch_expiring = BatchViewSet.as_view({'get': 'expiring'})

# Stock Movements
movement_list = StockMovementViewSet.as_view({'get': 'list'})

urlpatterns = [
    path('batches/', batch_list),
    path('batches/<int:pk>/', batch_detail),
    path('batches/<int:pk>/adjust/', batch_adjust),
    path('batches/expiring/', batch_expiring),
    path('movements/', movement_list),
]
