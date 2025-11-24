from rest_framework import viewsets,status
from rest_framework.exceptions import NotAuthenticated

from .models import (
    Role,Permission,RolePermission,UserRole,Log,AcademicYear,SystemSetting
)
from .serializers import (
    RoleSerializer,PermissionSerializer,RolePermissionSerializer,UserRoleSerializer,
    LogSerializer,AcademicYearSerializer,SystemSettingSerializer
)
from rest_framework.decorators import action,api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from custom_permission.permissions import IsSuperAdmin


class RoleViewSet(viewsets.ModelViewSet):

    queryset = Role.objects.all().order_by('-name')
    serializer_class = RoleSerializer
    permission_classes = [IsSuperAdmin]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.none()
        return self.queryset

class PermissionViewSet(viewsets.ModelViewSet):

    queryset = Permission.objects.all().order_by('-code_name')
    serializer_class = PermissionSerializer
    permission_classes = [IsSuperAdmin]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.none()
        return self.queryset

class RolePermissionViewSet(viewsets.ModelViewSet):

    queryset = RolePermission.objects.select_related('role','permission').all()
    serializer_class = RolePermissionSerializer
    permission_classes = [IsSuperAdmin]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.none()
        return self.queryset

class UserRoleViewSet(viewsets.ModelViewSet):

    queryset = UserRole.objects.select_related('user','role').all()
    serializer_class = UserRoleSerializer
    permission_classes = [IsSuperAdmin]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.none()
        return self.queryset


class LogViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Log.objects.select_related('user').all()
    serializer_class = LogSerializer
    permission_classes = [IsSuperAdmin]
    filterset_fields = ['user__id','action','timestamp']

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.none()
        return self.queryset

class AcademicYearViewSet(viewsets.ModelViewSet):
    
    queryset = AcademicYear.objects.all().order_by('-created_at')
    serializer_class = AcademicYearSerializer
    permission_classes = [IsSuperAdmin]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.none()
        return self.queryset

    @action(detail=True,methods=['post'],permission_classes=[IsSuperAdmin])
    def activate(self,request,pk=None):
        year = self.get_object()
        with transaction.atomic():
            AcademicYear.objects.update(is_active=False)
            year.is_active = True
            year.save()
        return Response(self.get_serializer(year).data)

class SystemSettingViewSet(viewsets.ModelViewSet):

    queryset = SystemSetting.objects.all()
    serializer_class = SystemSettingSerializer
    permission_classes = [IsSuperAdmin]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.none()
        return self.queryset

class DashboardStats(APIView):

    permission_classes = [IsSuperAdmin]

    def get(self,request):
        from core.models import Faculty,Department,Grade
        from student.models import Student
        from teacher.models import Teacher
        from employees.models import Employee

        data = {
            'students_count':Student.objects.count(),
            'teachers_count':Teacher.objects.count(),
            'employees_count':Employee.objects.count(),
            'faculties_count':Faculty.objects.count(),
            'departments_count':Department.objects.count(),
            'roles_count':Role.objects.count()
        }
        return Response(data)