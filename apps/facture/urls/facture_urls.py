from django.urls import path
from apps.facture.views.facture_views import ElectronicDocumentViewSet

doc_list = ElectronicDocumentViewSet.as_view({'get': 'list', 'post': 'create'})
doc_detail = ElectronicDocumentViewSet.as_view({'get': 'retrieve', 'put': 'update'})

urlpatterns = [
    path('', doc_list),
    path('<int:pk>/', doc_detail),
]
