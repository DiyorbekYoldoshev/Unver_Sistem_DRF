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
    avatar = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = "__all__"
        ref_name = "CustomUserSerializer"

    def get_avatar(self,obj):
        if obj.avatar and hasattr(obj.avatar, 'url'):
            return obj.avatar.url
        return None


class ProfileSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False)
    password = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name',
            'phone', 'address', 'avatar', 'password'
        ]
        ref_name = "CustomProfileSerializer"

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance

    def validate(self, attrs):
        blocked = ['is_staff','is_superuser','role']
        for filed in blocked:
            if filed in attrs:
                raise serializers.ValidationError({filed: "Bu maydonni o'zgartirish mumkin emas"})
        return attrs

