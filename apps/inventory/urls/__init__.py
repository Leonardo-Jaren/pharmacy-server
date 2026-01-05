from django.urls import path, include

app_name = 'inventory'

urlpatterns = [
    path('', include('apps.inventory.urls.inventory_urls')),
]
