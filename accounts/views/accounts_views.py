from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action, permission_classes
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from custom_permission.permissions import (
    IsStudent, IsTeacher, IsEmployee, IsAdminOrEmployeeOrTeacher, IsAdmin
)
from rest_framework.throttling import UserRateThrottle
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

    # Asosiy

    # 1 - queryset
    queryset = User.objects.all().order_by('-id')
    # 2 - serializer
    serializer_class = UserSerializer
    # 3 - permission
    permission_classes = [IsAdmin]
    # 4 - pagination
    pagination_class = CustomPagination
    # 5 - parses
    parser_classes = [MultiPartParser,FormParser]

    # Search va Filter

    # 1 - filterset_class
    filterset_class = UserFilter
    # 2 - filter_backend
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # 3 - search_fields
    search_fields = ['username','first_name','last_name','email','role']
    # 4 - ordering_fields
    ordering_fields = ['id','username','role']
    # 5 - throttle_classes
    throttle_classes = [UserRateThrottle]
    # get_permission va get_queryset
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
        if user.role != 'admin':
            raise NotAuthenticated("Sizda bu so'rov uchun ruxsat yo'q")

        if not user or not user.is_authenticated:
            raise NotAuthenticated("Avval tizimga kiring")

        # Admin yoki staff – hammasini ko‘radi
        if user.is_superuser or user.is_staff or user.role == 'admin':
            return self.queryset.all()

        return None

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
        if not user.is_superuser and user.role != 'admin':
            raise NotAuthenticated("Siz admin emassiz")

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



class ProfileViewSet(GenericViewSet):
    # Asosiy
    # 1 - queryset
    queryset = User.objects.all()
    # 2 - serializer_class
    serializer_class = ProfileSerializer
    # 3 - permission_classes
    permission_classes = [IsAuthenticated]
    # 4 - pagination_class
    pagination_class = CustomPagination
    # 5 - parser_classes
    parser_classes = [MultiPartParser, FormParser]

    # Filter va qidiruvlar
    # 6 - filterset_class (filter.py fayldagi)
    filterset_class = ProfileFilter
    # 7 - filter_backends
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # 8 - search_fields
    search_fields = ['first_name', 'last_name', 'email', 'address']
    # 9 - ordering_fields
    ordering_fields = ['id', 'username', 'birth_date']
    # Boshqa
    # 10 - throttle_classes
    throttle_classes = [UserRateThrottle]
    # get_queryset, get_permission
    def get_queryset(self):

        user = self.request.user

        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.none()

        if not user.is_authenticated:
            raise NotAuthenticated("Avval tizimga kiring")

        if user.is_superuser and user.role == 'admin':
            return self.queryset.all()

        if user.role == 'teacher':
            return self.queryset.filter(role='student')

        return self.queryset.filter(id=user.id)

    def get_permissions(self):

        return [IsAuthenticated()]


    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_profile(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['put'], permission_classes=[IsAuthenticated])
    def update_profile(self, request):
        allowed_fields = ['username','first_name','last_name','phone','address','password','avatar']

        data = {field: request.data[field] for field in allowed_fields if field in request.data}

        serializer = ProfileSerializer(request.user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
