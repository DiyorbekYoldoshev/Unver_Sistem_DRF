from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.exceptions import NotAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from custom_permission.permissions import (
    IsStudent, IsTeacher, IsEmployee, IsAdminOrEmployeeOrTeacher, IsAdminOrEmployee, IsAdmin
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
class ProfileViewSet(viewsets.ModelViewSet):
    from rest_framework.parsers import MultiPartParser,FormParser
    queryset = User.objects.select_related('user').all().order_by('-id')
    serializer_class = ProfileSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.none()

        user = self.request.user
        if not user or not user.is_authenticated:
            raise NotAuthenticated("Avval tizimga kiring")

        if user.is_superuser or user.is_staff or user.role == 'admin':
            return self.queryset.all()

        # Faqat o‘z profilini ko‘radi
        return self.queryset.filter(user=user)

    permission_classes = [IsAdminOrEmployeeOrTeacher|IsStudent]
    pagination_class = CustomPagination
    filterset_class = ProfileFilter
    parser_classes = [MultiPartParser,FormParser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__username', 'first_name', 'last_name', 'phone', 'address']
    ordering_fields = ['id', 'first_name', 'last_name']

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_profile(self, request):
        """Foydalanuvchining profile ma'lumotlarini olish"""
        profile = User.objects.filter(user=request.user).first()
        if not profile:
            return Response({'error': 'Profil topilmadi'}, status=404)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)
