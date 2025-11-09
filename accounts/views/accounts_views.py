from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from custom_permission.permissions import IsStudent,IsTeacher,IsSuperAdmin,IsEmployee,IsAdminUserOrReadOnly
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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Localized messages
        messages = {
            "UZ": "Siz ro'yhatdan o'tdingiz",
            "RU": "Вы зарегистрированы",
            "EN": "You have registered successfully",
        }
        success_message = messages.get(user.language, "You have registered successfully")
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                'message':success_message,
                'user': {
                    'id':user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'role': user.role,
                    'phone': user.phone,
                    'gender': user.gender,
                    'birth_date': user.birth_date,
                    'address': user.address,
                    'avatar': user.avatar,
                },
                'refresh':str(refresh),
                'access': str(refresh.access_token)
            },status=status.HTTP_201_CREATED
        )


    @action(detail=False, methods=['get', 'put'], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = ProfileSerializer(request.user, data=request.data, partial=True)
        if request.method == 'PUT':
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data)

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


    permission_classes = [IsAdminUserOrReadOnly]
    pagination_class = CustomPagination
    filterset_class = UserFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'email', 'role']
    ordering_fields = ['id', 'username']


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.select_related('user').all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    pagination_class = CustomPagination
    filterset_class = ProfileFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__username', 'first_name', 'last_name', 'phone', 'address']
    ordering_fields = ['id', 'first_name']

