from django.urls import path
from apps.cashshift.views.cashshift_views import CashShiftViewSet, CashOperationViewSet

# Cash Shifts
shift_list = CashShiftViewSet.as_view({'get': 'list', 'post': 'create'})
shift_detail = CashShiftViewSet.as_view({'get': 'retrieve'})
shift_close = CashShiftViewSet.as_view({'post': 'close'})
shift_current = CashShiftViewSet.as_view({'get': 'current'})

# Cash Operations
operation_list = CashOperationViewSet.as_view({'get': 'list', 'post': 'create'})

urlpatterns = [
    path('shifts/', shift_list),
    path('shifts/<int:pk>/', shift_detail),
    path('shifts/<int:pk>/close/', shift_close),
    path('shifts/current/', shift_current),
    path('operations/', operation_list),
]
