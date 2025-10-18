from django.db.models import Avg
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from teacher.models import Teacher, TeacherActivity,TeacherSchedule
from teacher.serializers import TeacherSerializer,TeacherActivitySerializer,TeacherScheduleSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from core.serializers import *
from student.serializers import *
from student.models import *
from employees.models import *
from employees.serializers import *
from accounts.filters import *
from rest_framework.decorators import action
from django.db import models


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


# Student

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]


class StudentRecordViewSet(viewsets.ModelViewSet):
    queryset = StudentRecord.objects.all()
    serializer_class = StudentRecordSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def top_grade_student(self, request):
        """Eng yuqori o‘rtacha bahoga ega 3 ta talabani chiqaradi."""
        top_students = (
            Student.objects
            .annotate(avg_grade=Avg('records__grade'))
            .order_by('-avg_grade')[:3]
        )

        data = []
        for s in top_students:
            profile = getattr(s.user, 'profile', None)
            full_name = (
                f"{profile.first_name} {profile.last_name}"
                if profile else s.user.username
            )
            data.append({
                "student_id": s.student_id,
                "student_name": full_name,
                "group": s.group.name if s.group else None,
                "average_grade": s.avg_grade,
                "status": s.status,
            })

        return Response({"Eng yuqori ball olgan talabalar": data})

    @action(detail=True,methods=['get'])
    def average_rating(self,request,pk=None):
        """Talabaning o‘rtacha bahosini hisoblaydi."""
        student_record = self.get_object()
        student = student_record.student
        records = student.records.all()

        if not records.exists():
            return Response({'average_rating':'Sizda hali baholar yo\'q'})
        avg_rating = records.aggregate(models.Avg('grade'))['grade__avg']

        profile = getattr(student.user,'profile',None)
        full_name = (
            f"{profile.first_name}  {profile.last_name}"
            if profile else student.user.username
        )
        return Response({
            'student_id':student.student_id,
            'student_name':full_name,
            'group':student.group.name if student.group else None,
            'average_rating':avg_rating
        })

class StudentComplaintViewSet(viewsets.ModelViewSet):
    queryset = StudentComplaint.objects.all()
    serializer_class = StudentComplaintSerializer
    permission_classes = [IsAuthenticated]

# Employee


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filterset_class = EmployeeFilter
    search_fields = ['user','position','department']

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filterset_class = TaskFilter
    search_fields = ['employee','title','description','status']

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filterset_class = ReportFilter
    search_fields = ['employee','report_text']
