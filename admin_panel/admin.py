from django.contrib import admin
from .models import Role, Permission, RolePermission, UserRole, Log, AcademicYear, SystemSetting

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']
    search_fields = ['name']


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'code_name', 'description']
    search_fields = ['code_name']


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'role', 'permission']
    list_filter = ['role__name']


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'role', 'assigned_at']
    search_fields = ['user__username', 'role__name']


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'action', 'timestamp', 'ip_address']
    search_fields = ['user__username', 'action']


@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ['id', 'year', 'is_active', 'created_at']


@admin.register(SystemSetting)
class SystemSettingAdmin(admin.ModelAdmin):
    list_display = ['id', 'key']
