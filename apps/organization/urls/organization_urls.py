from django.urls import path
from apps.organization.views.organization_views import (
    OrganizationViewSet,
    BranchViewSet,
    InvoiceSeriesViewSet
)

# Organizations
org_list = OrganizationViewSet.as_view({'get': 'list', 'post': 'create'})
org_detail = OrganizationViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})

# Branches
branch_list = BranchViewSet.as_view({'get': 'list', 'post': 'create'})
branch_detail = BranchViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})

# Invoice Series
series_list = InvoiceSeriesViewSet.as_view({'get': 'list', 'post': 'create'})

urlpatterns = [
    path('organizations/', org_list),
    path('organizations/<int:pk>/', org_detail),
    path('branches/', branch_list),
    path('branches/<int:pk>/', branch_detail),
    path('invoice-series/', series_list),
]
