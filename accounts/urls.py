from rest_framework import routers
from .views import *
from django.urls import path,include


router = routers.DefaultRouter()
router.register(r'user',UserViewSet)
router.register(r'profile',ProfileViewSet)
router.register(r'teacher',TeacherViewSet)
router.register(r'teacher-activity',TeacherActivityViewSet)
router.register(r'teacher-schedule',TeacherScheduleViewSet)
router.register(r'faculty',FacultyViewSet)
router.register(r'department',DepartmentViewSet)
router.register(r'group',GroupViewSet)
router.register(r'subject',SubjectViewSet)
router.register(r'schedule',ScheduleViewSet)
router.register(r'grade',GradeViewSet)
router.register(r'attendance',AttendanceViewSet)

urlpatterns = [
    path('',include(router.urls))
]
