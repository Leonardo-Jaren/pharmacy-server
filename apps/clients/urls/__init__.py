from django.urls import path, include

app_name = 'clients'

urlpatterns = [
    path('', include('apps.clients.urls.client_urls')),
]
