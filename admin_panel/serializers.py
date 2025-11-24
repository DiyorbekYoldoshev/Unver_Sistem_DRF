from rest_framework.decorators import permission_classes
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import (
    Role,Permission,RolePermission,UserRole,Log,AcademicYear,SystemSetting
)
from django.contrib.auth import get_user_model
User = get_user_model()


class RoleSerializer(ModelSerializer):

    class Meta:
        model = Role
        fields = ['id','name','description']
        read_only_fields = ['name','description']


class PermissionSerializer(ModelSerializer):

    class Meta:
        model = Permission
        fields = ['id','code_name','description']
        ref_name = "UserPermission"

class RolePermissionSerializer(ModelSerializer):

    role = RoleSerializer(read_only=True)
    permission = PermissionSerializer(read_only=True)
    role_id = serializers.IntegerField(write_only=True, required=True)
    permission_id = serializers.IntegerField(write_only=True,required=True)

    class Meta:
        model = RolePermission
        fields = ['id','role','permission','role_id','permission_id']
        read_only_fields = ['role','permission']

    def create(self, validated_data):
        role = Role.objects.get(pk=validated_data.pop('role_id'))
        permission = Permission.objects.get(pk=validated_data.pop('permission_id'))
        obj, created = RolePermission.objects.get_or_create(role=role, permission=permission)

        return obj

class UserRoleSerializer(ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    role = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = UserRole
        fields = ['id','user','role','assigned_at']
        read_only_fields = ['assigned_at']



class LogSerializer(ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Log
        fields = ['id','user','action','timestamp','ip_address','meta']

class AcademicYearSerializer(ModelSerializer):

    class Meta:
        model = AcademicYear
        fields = ['id','year','is_active','created_at']

class SystemSettingSerializer(ModelSerializer):

    class Meta:
        model = SystemSetting
        fields = ['key','value','description']