from django.urls import path
from apps.clients.views.client_views import ClientViewSet

client_list = ClientViewSet.as_view({'get': 'list', 'post': 'create'})
client_detail = ClientViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})
client_search = ClientViewSet.as_view({'get': 'search'})

urlpatterns = [
    path('', client_list),
    path('<int:pk>/', client_detail),
    path('search/', client_search),
]
