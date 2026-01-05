from django.urls import path
from apps.users.views.user_views import UserViewSet

user_list = UserViewSet.as_view({'get': 'list', 'post': 'create'})
user_detail = UserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})
user_search = UserViewSet.as_view({'get': 'search'})

urlpatterns = [
    path('', user_list),
    path('<int:pk>/', user_detail),
    path('search/', user_search),
]
