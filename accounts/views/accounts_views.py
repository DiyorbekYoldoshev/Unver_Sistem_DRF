from django_filters import rest_framework as django_filters
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters

from core.middleware import CHAT_ID,TOKEN
from ..filters import ProfileFilter, UserFilter
from ..models import *
from ..serializers import UserSerializer, ProfileSerializer
import requests



class CustomPagination(PageNumberPagination):
    page_size = 10


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


    def list(self, request, *args, **kwargs):
        # GET /api/v1/user/ ga so‘rov keldi
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": f"👀 User ro‘yxati so‘raldi\nBy: {request.user}"}
        )
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        # GET /api/v1/user/<id>/ uchun
        instance = self.get_object()
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": f"📄 User profili so‘raldi: {instance.username}"}
        )
        return super().retrieve(request, *args, **kwargs)


    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filterset_class = UserFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'email', 'role']
    ordering_fields = ['id', 'username']


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filterset_class = ProfileFilter

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__username', 'first_name', 'last_name', 'phone', 'address']
    ordering_fields = ['id', 'first_name']

