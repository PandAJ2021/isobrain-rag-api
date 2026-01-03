from django.contrib import admin
from django.db import connection
from django.contrib.auth.admin import UserAdmin
from .models import TenantUser
from django.contrib.auth.models import User, Group

admin.site.unregister(User)
admin.site.unregister(Group)

@admin.register(User)
class GlobalUserAdmin(UserAdmin):
    def has_delete_permission(self, request, obj=None):
        if connection.schema_name != 'public':
            return False
        return super().has_delete_permission(request, obj)

    def has_add_permission(self, request):
        if connection.schema_name != 'public':
            return False
        return super().has_add_permission(request)

    def has_change_permission(self, request, obj=None):
        if connection.schema_name != 'public':
            return False
        return super().has_change_permission(request, obj)


@admin.register(TenantUser)
class TenantUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'tenant', 'role')
    search_fields = ('user__username', 'user__email', 'tenant__name')
    list_filter = ('role', )