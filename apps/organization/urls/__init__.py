from django.urls import path, include

app_name = 'organization'

urlpatterns = [
    path('', include('apps.organization.urls.organization_urls')),
]
