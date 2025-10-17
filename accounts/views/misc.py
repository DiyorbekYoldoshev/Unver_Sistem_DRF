from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from teacher.models import Teacher, TeacherActivity,TeacherSchedule
from teacher.serializers import TeacherSerializer,TeacherActivitySerializer,TeacherScheduleSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from core.serializers import *

class CustomPagination(PageNumberPagination):
    page_size = 10


# Teacher
class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['department','position','specialization','degree']
    ordering_fields = ['id','user']

class TeacherActivityViewSet(viewsets.ModelViewSet):
    queryset = TeacherActivity.objects.all()
    serializer_class = TeacherActivitySerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['teacher','subject','room']
    ordering_fields = ['id','teacher']

class TeacherScheduleViewSet(viewsets.ModelViewSet):
    queryset = TeacherSchedule.objects.all()
    serializer_class = TeacherScheduleSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['title','description']


# CORE
class FacultyViewSet(viewsets.ModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    permission_classes = [IsAuthenticated]


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]



class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]



class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]


class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated]


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]


