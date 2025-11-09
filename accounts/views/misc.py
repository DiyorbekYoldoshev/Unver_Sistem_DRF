from django.db.models import Avg
from rest_framework import viewsets,filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend


from student.serializers import *
from teacher.serializers import *
from employees.serializers import *
from core.serializers import *

from custom_permission.permissions import *


class CustomPagination(PageNumberPagination):
    page_size = 10

# =====================================================================================
# 🧑‍🏫 TEACHER VIEWS
# =====================================================================================

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all().order_by('hire_date')
    pagination_class = CustomPagination
    serializer_class = TeacherSerializer
    permission_classes = [IsTeacher|IsAdminUserOrReadOnly]
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['department','position','specialization','degree']
    ordering_fields = ['id','user__username']

    def get_queryset(self):
        user = self.request.user
        if hasattr(user,'role') and user.role == 'teacher':
            return Teacher.objects.filter(user=user)
        return super().get_queryset()

class TeacherActivityViewSet(viewsets.ModelViewSet):
    queryset = TeacherActivity.objects.all().order_by('-id')
    serializer_class = TeacherActivitySerializer
    pagination_class = CustomPagination
    permission_classes = [IsTeacher|IsAdminUserOrReadOnly]
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['teacher__user__username','subject__name','room']
    ordering_fields = ['id','teacher__user__username']


class TeacherScheduleViewSet(viewsets.ModelViewSet):
    queryset = TeacherSchedule.objects.all().order_by('-id')
    serializer_class = TeacherScheduleSerializer
    pagination_class = CustomPagination
    permission_classes = [IsTeacher|IsAdminUserOrReadOnly]
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter,filters.SearchFilter]
    search_fields = ['title','description','day']
    ordering_fields = ['id','teacher__user__username']


# =====================================================================================
# 🧱 CORE VIEWS
# =====================================================================================

class FacultyViewSet(viewsets.ModelViewSet):
    queryset = Faculty.objects.all().order_by('name')
    serializer_class = FacultySerializer
    pagination_class = CustomPagination
    permission_classes = [IsAdminUserOrReadOnly]

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all().order_by('name')
    serializer_class = DepartmentSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAdminUserOrReadOnly]

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    pagination_class = CustomPagination
    permission_classes = [IsTeacher|IsStudent|IsAdminUserOrReadOnly]

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all().order_by('name')
    serializer_class = SubjectSerializer
    permission_classes = [IsTeacher | IsStudent | IsAdminUserOrReadOnly]

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all().order_by('-id')
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]


class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all().order_by("-created_at")
    serializer_class = GradeSerializer
    permission_classes = [IsTeacher | IsStudent | IsAdminUserOrReadOnly]


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all().order_by("-date")
    serializer_class = AttendanceSerializer
    permission_classes = [IsTeacher | IsStudent | IsAdminUserOrReadOnly]


# =====================================================================================
# 🎓 STUDENT VIEWS
# =====================================================================================


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().order_by('-student_id')
    serializer_class = StudentRecordSerializer
    permission_classes = [IsStudent|IsTeacher|IsAdminUserOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user,'role') and user.role == 'student':
            return Student.objects.filter(user=user)
        return super().get_queryset()

class StudentRecordViewSet(viewsets.ModelViewSet):
    queryset = StudentRecord.objects.all().order_by('-id')
    serializer_class = StudentRecordSerializer
    permission_classes = [IsTeacher|IsAdminUserOrReadOnly]
    pagination_class = CustomPagination

    @action(detail=False,methods=['get'])
    def top_grade_student(self,request):
        top_student = (
            Student.objects
            .annotate(avg_grade=Avg('average_rating'))
            .order_by('-id')[:3]
        )
        data = [
            {
                'student_id':s.student_id,
                'full_name':f"{getattr(s.user.profile,'first_name','')} {getattr(s.user.profile,'last_name','')}".strip(),
                'group':getattr(s.group,'name',None),
                'average_rating':s.avg_grade,
                'status':s.status

            }
            for s in top_student
        ]
        return Response({'result':data})

    @action(detail=True,methods=['get'])
    def average_rating(self,request,pk=None):
        student_record = self.get_object()
        student = student_record.student
        avg_rating = student.records.aggregate(Avg('grade'))['grade_avg']
        return Response(
            {
                'student_id':student.student_id,
                'full_name':f"{getattr(student.user.profile,'first_name','')}  {getattr(student.user.profile,'last_name','')}".strip(),
                'group':getattr(student.group,'name',None),
                'average_rating':avg_rating or 'Hali baholar mavjud emas'
            }
        )

class StudentComplaintViewSet(viewsets.ModelViewSet):
    queryset = StudentComplaint.objects.all().order_by('-id')
    serializer_class = StudentComplaintSerializer
    permission_classes = [IsStudent | IsAdminUserOrReadOnly]


# =====================================================================================
# 👨‍💼 EMPLOYEE VIEWS
# =====================================================================================

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all().order_by('-id')
    serializer_class = EmployeeSerializer
    permission_classes = [IsEmployee | IsAdminUserOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["user__username", "position", "department__name"]
    ordering_fields = ["id", "user__username"]


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('deadline')
    serializer_class = TaskSerializer
    permission_classes = [IsEmployee | IsAdminUserOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["employee__user__username", "title", "description", "status"]
    ordering_fields = ["id", "employee__user__username"]


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all().order_by('-created_at')
    serializer_class = ReportSerializer
    permission_classes = [IsEmployee | IsAdminUserOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["employee__user__username", "report_text"]
    ordering_fields = ["id", "employee__user__username"]