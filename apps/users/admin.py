from django.contrib import admin
from apps.users.models import User, Role


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'role', 'branch', 'is_active', 'created_at')
    list_filter = ('role', 'is_active', 'branch')
    search_fields = ('username', 'email', 'first_name', 'last_name')
