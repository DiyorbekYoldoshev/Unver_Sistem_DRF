from rest_framework import serializers
from .models import *
from django.contrib.auth.models import Group, Permission

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'codename', 'name']


class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)
    user_permissions = PermissionSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = "__all__"
        ref_name = "CustomUserSerializer"

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = "__all__"
        ref_name = "CustomProfileSerializer"
