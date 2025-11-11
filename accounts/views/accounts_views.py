from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from custom_permission.permissions import (
    IsStudent, IsTeacher, IsEmployee, IsAdminUserOrReadOnly
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
    permission_classes = [IsAdminUserOrReadOnly]
    pagination_class = CustomPagination
    filterset_class = UserFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'email', 'role']
    ordering_fields = ['id', 'username', 'created_at']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Localized success message
        messages = {
            "UZ": "Siz ro'yhatdan o'tdingiz ✅",
            "RU": "Вы успешно зарегистрировались ✅",
            "EN": "You have registered successfully ✅",
        }
        success_message = messages.get(user.language, "You have registered successfully ✅")

        # JWT tokenlar yaratish
        refresh = RefreshToken.for_user(user)

        # Telegram orqali admin yoki log chatga habar yuborish
        try:
            requests.post(
                f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                data={"chat_id": CHAT_ID, "text": f"🆕 Yangi foydalanuvchi ro‘yxatdan o‘tdi: {user.username}"}
            )
        except Exception as e:
            print(f"Telegramga yuborishda xato: {e}")

        return Response(
            {
                'message': success_message,
                'user': {
                    'id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'role': user.role,
                    'phone': user.phone,
                    'gender': user.gender,
                    'birth_date': user.birth_date,
                    'address': user.address,
                    'avatar': getattr(user, 'avatar', None),
                },
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            },
            status=status.HTTP_201_CREATED
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
    queryset = User.objects.select_related('user').all().order_by('-id')
    serializer_class = ProfileSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    pagination_class = CustomPagination
    filterset_class = ProfileFilter
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
