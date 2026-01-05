from django.urls import path, include

app_name = 'catalog'

urlpatterns = [
    path('', include('apps.catalog.urls.catalog_urls')),
]
