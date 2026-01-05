from django.urls import path, include

app_name = 'users'

urlpatterns = [
    path('', include('apps.users.urls.user_urls')),
]
