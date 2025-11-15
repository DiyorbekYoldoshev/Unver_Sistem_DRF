from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from custom_permission.permissions import (
    IsStudent, IsTeacher, IsEmployee, IsAdminOrEmployeeOrTeacher, IsAdmin
)
from core.middleware import CHAT_ID, TOKEN
from ..filters import ProfileFilter, UserFilter
from ..models import User
from ..serializers import UserSerializer, ProfileSerializer
import requests


# ================================
# 📄 PAGINATION
# ================================
class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


# ================================
# 👤 USER VIEWSET
# ================================
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-id')
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['create']:
            return [IsAdmin()]

        if self.action in ['list', 'destroy', 'update', 'partial_update']:
            return [IsAdmin()]

        if self.action in ['retrieve']:
            return [IsTeacher(),IsEmployee]

        return [IsAuthenticated()]

    def get_queryset(self):
        # Swagger fake view uchun
        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.none()

        user = self.request.user
        if not user or not user.is_authenticated:
            raise NotAuthenticated("Avval tizimga kiring")

        # Admin yoki staff – hammasini ko‘radi
        if user.is_superuser or user.is_staff or user.role == 'admin':
            return self.queryset.all()

        if user.role == 'teacher':
            return User.objects.filter(role='student')

        # Oddiy foydalanuvchi – faqat o‘zini ko‘radi
        return self.queryset.filter(id=user.id)


    permission_classes = [IsAdmin]
    pagination_class = CustomPagination
    filterset_class = UserFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'email', 'role']
    ordering_fields = ['id', 'username', 'created_at']

    def create(self, request, *args, **kwargs):

        data = request.data.copy()

        if not request.user.is_authenticated or request.user.is_superuser:
            data['is_superuser'] = False
            data['is_staff'] = False
            data['role'] = 'student'


        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                'message': "You have registered successfully ✅",
                'user': UserSerializer(user,context={'request':request}).data,
                'refresh':str(refresh),
                'access':str(refresh.access_token)
            },status=status.HTTP_201_CREATED
        )


    @action(detail=False, methods=['get', 'put'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Foydalanuvchining shaxsiy profilini ko‘rish yoki tahrirlash"""
        user = request.user
        if request.method == 'PUT':
            serializer = self.get_serializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
            serializer = self.get_serializer(user)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        """GET /api/v1/user/ uchun Telegram log"""
        try:
            requests.post(
                f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                data={"chat_id": CHAT_ID, "text": f"👀 User ro‘yxati so‘raldi\nBy: {request.user.username}"}
            )
        except Exception:
            pass
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """GET /api/v1/user/<id>/ uchun Telegram log"""
        instance = self.get_object()
        try:
            requests.post(
                f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                data={"chat_id": CHAT_ID, "text": f"📄 User profili so‘raldi: {instance.username}"}
            )
        except Exception:
            pass
        return super().retrieve(request, *args, **kwargs)


# ================================
# 👥 PROFILE VIEWSET
# ================================


# class ProfileViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all().order_by('-id')
#     serializer_class = ProfileSerializer
#
#     # Faqat o'qish va taxrirlash
#     http_method_names = ["get", "put", "patch"]
#
#     parser_classes = [MultiPartParser, FormParser]
#     permission_classes = [IsAdminOrEmployeeOrTeacher | IsStudent]
#
#     pagination_class = CustomPagination
#     filterset_class = ProfileFilter
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
#
#     search_fields = ['username', 'first_name', 'last_name', 'email']
#     ordering_fields = ['id', 'first_name', 'last_name']
#
#     def get_queryset(self):
#         user = self.request.user
#
#         if not user.is_authenticated:
#             raise NotAuthenticated("Avval tizimga kiring")
#
#         if user.is_superuser:
#             return User.objects.select_related("teacher", "student", "employee")
#
#         return User.objects.filter(id=user.id)
#
#     # CREATE NI BLOKLASH
#     def create(self, request, *args, **kwargs):
#         return Response(
#             {"detail": "Profil yaratib bo‘lmaydi"},
#             status=status.HTTP_405_METHOD_NOT_ALLOWED
#         )
#
#     # DELETE NI BLOKLASH
#     def destroy(self, request, *args, **kwargs):
#         return Response(
#             {"detail": "Profil o‘chirib bo‘lmaydi"},
#             status=status.HTTP_405_METHOD_NOT_ALLOWED
#         )
#
#     @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
#     def my_profile(self, request):
#         serializer = UserSerializer(request.user)
#         return Response(serializer.data)
#
#     @action(detail=False, methods=['put', 'patch'], permission_classes=[IsAuthenticated])
#     def update_profile(self, request):
#         serializer = ProfileSerializer(
#             request.user,
#             data=request.data,
#             partial=True
#         )
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#

class ProfileViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    pagination_class = CustomPagination

    filterset_class = ProfileFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    parser_classes = [MultiPartParser, FormParser]

    search_fields = ['username', 'first_name', 'last_name', 'email']
    ordering_fields = ['id', 'first_name', 'last_name']

    def get_permissions(self):
        """
        Admin → create/update/delete mumkin
        Boshqa userlar → faqat o‘z profiliga update
        """
        # Admin uchun cheksiz huquq
        if self.request.user.is_superuser:
            return [IsAdmin()]

        # create/delete → faqat admin; boshqalar uchun taqiqlanadi
        if self.action in ['create', 'destroy']:
            return [IsAdmin()]

        # oddiy user → faqat authenticated
        return [IsAuthenticated()]

    def get_queryset(self):
        """
        Admin → Barcha userlar
        Oddiy user → faqat o‘z profilini ko‘radi
        """
        user = self.request.user

        if not user or not user.is_authenticated:
            raise NotAuthenticated("Avval tizimga kiring")

        if user.is_superuser:
            return User.objects.select_related('employee', 'teacher', 'student').all()

        return User.objects.filter(id=user.id)

    def perform_destroy(self, instance):
        """
        O'chirish -> faqat admin
        """
        user = self.request.user
        if not user.is_superuser:
            raise PermissionDenied("Faqat admin o‘chira oladi")
        instance.delete()

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_profile(self, request):
        """
        Foydalanuvchining shaxsiy profilini olish
        """
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
