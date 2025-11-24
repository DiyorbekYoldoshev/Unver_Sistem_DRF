from django.urls import path,include
from rest_framework.routers import DefaultRouter

from .views import (
    RoleViewSet, PermissionViewSet, RolePermissionViewSet, UserRoleViewSet,
    LogViewSet, AcademicYearViewSet, SystemSettingViewSet, DashboardStats
)

router = DefaultRouter()

router.register('role',RoleViewSet,basename='admin-roles')
router.register('permission',PermissionViewSet,basename='admin-permissions')
router.register('role-permission',RolePermissionViewSet,basename='admin-role-permissions')
router.register('user-roles',UserRoleViewSet,basename='admin-user-roles')
router.register('logs',LogViewSet,basename='admin-logs')
router.register('academic-year',AcademicYearViewSet,basename='admin-academic-years')
router.register('system-settings',SystemSettingViewSet,basename='admin-system-settings')

urlpatterns = [
    path('',include(router.urls)),
    path('dashboard/',DashboardStats.as_view(),name='admin-dashboard')

]