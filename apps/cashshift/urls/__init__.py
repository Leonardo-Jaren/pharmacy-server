from django.urls import path, include

app_name = 'cashshift'

urlpatterns = [
    path('', include('apps.cashshift.urls.cashshift_urls')),
]
