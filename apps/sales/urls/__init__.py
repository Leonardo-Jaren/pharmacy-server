from django.urls import path, include

app_name = 'sales'

urlpatterns = [
    path('', include('apps.sales.urls.sales_urls')),
]
