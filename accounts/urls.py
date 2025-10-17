from rest_framework import routers
from .views import ProfileViewSet,UserViewSet
from django.urls import path,include


router = routers.DefaultRouter()
router.register(r'user',UserViewSet)
router.register(r'profile',ProfileViewSet)

urlpatterns = [
    path('',include(router.urls))
]
