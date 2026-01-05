from django.urls import path, include

app_name = 'facture'

urlpatterns = [
    path('', include('apps.facture.urls.facture_urls')),
]
