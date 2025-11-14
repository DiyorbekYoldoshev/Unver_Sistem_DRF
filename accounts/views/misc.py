# core/views.py  (yoki loyihangizdagi mos joyga)
from django.db.models import Avg
from rest_framework import viewsets, filters, status
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend


from custom_permission.permissions import (
    IsAdminOrEmployee, IsTeacher, IsStudent, IsEmployee, IsAdmin, IsAdminOrTeacher,IsAdminOrStudent,
    IsAdminOrEmployeeOrTeacher,IsSelfOrAdmin
)
from core.models import (
    Faculty, Department, Group, Subject, Schedule, Grade, Attendance
)
from teacher.models import Teacher, TeacherActivity, TeacherSchedule
from student.models import Student, StudentRecord, StudentComplaint
from employees.models import Employee, Task, Report

from core.serializers import (
    FacultySerializer, DepartmentSerializer, GroupSerializer, SubjectSerializer,
    ScheduleSerializer, GradeSerializer, AttendanceSerializer
)
from teacher.serializers import TeacherSerializer, TeacherActivitySerializer, TeacherScheduleSerializer
from student.serializers import StudentSerializer, StudentRecordSerializer, StudentComplaintSerializer
from employees.serializers import EmployeeSerializer, TaskSerializer, ReportSerializer

# ---------------- Custom Pagination (yoki core/pagination.py faylida saqlang) ---------------
from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# --------------------- BaseViewSet (DRY uchun) ------------------------------------------
class BaseViewSet(viewsets.ModelViewSet):
    """
    DRY: ko'p joyda ishlatiladigan umumiy sozlamalar shu yerda.
    """
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

# --------------------- Teacher ------------------------------------------
class TeacherViewSet(BaseViewSet):
    queryset = Teacher.objects.select_related('user', 'department').all().order_by('hire_date')
    serializer_class = TeacherSerializer
    permission_classes = [IsAdminOrEmployeeOrTeacher]
    search_fields = ['department__name', 'position', 'specialization', 'degree']
    ordering_fields = ['id', 'user__username']

    def get_queryset(self):

        if getattr(self,'swagger_fake_view',False):
            return self.queryset.none()

        user = self.request.user

        if not user or not user.is_authenticated:
            raise NotAuthenticated("Avval tizimga kiring")

        if user.is_superuser or user.is_staff or user.role == 'admin':
            return self.queryset.all()

        return self.queryset.filter(id=user.id)


class TeacherActivityViewSet(BaseViewSet):
    queryset = TeacherActivity.objects.select_related('teacher__user').order_by('-id')
    serializer_class = TeacherActivitySerializer

    def get_queryset(self):

        if getattr(self,'swagger_fake_view',False):
            return self.queryset.none()

        user = self.request.user
        if not user or not user.is_authenticated:
            raise NotAuthenticated("Avval tizimga kiring")

        if user.is_superuser or user.is_staff or user.role == 'admin':
            return self.queryset.all()

        return self.queryset.filter(id=user.id)

    permission_classes = [IsAdminOrEmployeeOrTeacher]
    search_fields = ['teacher__user__username', 'subject__name', 'room']
    ordering_fields = ['id', 'teacher__user__username']

class TeacherScheduleViewSet(BaseViewSet):
    queryset = TeacherSchedule.objects.select_related('teacher__user', 'subject', 'group').all().order_by('-id')
    serializer_class = TeacherScheduleSerializer

    def get_queryset(self):

        if getattr(self,'swagger_fake_view',False):
            return self.queryset.none()

        user = self.request.user

        if not user or not user.is_authenticated:
            raise NotAuthenticated("Avval tizimga kiring")

        if user.is_superuser or user.is_staff or user.role == 'admin':
            return self.queryset.all()

        return self.queryset.filter(id=user.id)


    permission_classes = [IsAdminOrEmployeeOrTeacher]
    search_fields = ['title', 'description', 'day']
    ordering_fields = ['id', 'teacher__user__username']

# --------------------- Core ------------------------------------------
class FacultyViewSet(BaseViewSet):
    queryset = Faculty.objects.all().order_by('name')
    serializer_class = FacultySerializer

    def get_queryset(self):

        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.none()

        user = self.request.user

        if not user or not user.is_authenticated:
            raise NotAuthenticated("Avval tizimga kiring")

        if user.is_superuser or user.is_staff or user.role == 'admin':
            return self.queryset.all()

        return self.queryset.filter(id=user.id)

    permission_classes = [IsAdminOrEmployee]
    search_fields = ['name']
    ordering_fields = ['id', 'name']

class DepartmentViewSet(BaseViewSet):
    queryset = Department.objects.select_related('faculty').all().order_by('name')
    serializer_class = DepartmentSerializer

    def get_queryset(self):

        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.none()

        user = self.request.user

        if not user or not user.is_authenticated:
            raise NotAuthenticated("Avval tizimga kiring")

        if user.is_superuser or user.is_staff or user.role == 'admin':
            return self.queryset.all()

        return self.queryset.filter(id=user.id)

    permission_classes = [IsAdminOrEmployee]
    search_fields = ['name', 'faculty__name']
    ordering_fields = ['id', 'name']

class GroupViewSet(BaseViewSet):
    queryset = Group.objects.select_related('department').all().order_by('name')
    serializer_class = GroupSerializer

    def get_queryset(self):

        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.none()

        user = self.request.user

        if not user or not user.is_authenticated:
            raise NotAuthenticated("Avval tizimga kiring")

        if user.is_superuser or user.is_staff or user.role == 'admin':
            return self.queryset.all()

        return self.queryset.filter(id=user.id)

    permission_classes = [IsAdminOrEmployeeOrTeacher|IsStudent]
    search_fields = ['name', 'department__name']
    ordering_fields = ['id', 'name']

class SubjectViewSet(BaseViewSet):
    queryset = Subject.objects.select_related('department').all().order_by('name')
    serializer_class = SubjectSerializer

    def get_queryset(self):

        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.none()

        user = self.request.user

        if not user or not user.is_authenticated:
            raise NotAuthenticated("Avval tizimga kiring")

        if user.is_superuser or user.is_staff or user.role == 'admin':
            return self.queryset.all()

        return self.queryset.filter(id=user.id)

    permission_classes = [IsTeacher | IsStudent | IsAdminOrEmployee]
    search_fields = ['name', 'department__name']
    ordering_fields = ['id', 'name']

class ScheduleViewSet(BaseViewSet):
    queryset = Schedule.objects.select_related('subject', 'teacher__user', 'group').all().order_by('-id')
    serializer_class = ScheduleSerializer

    def get_queryset(self):

        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.none()

        user = self.request.user

        if not user or not user.is_authenticated:
            raise NotAuthenticated("Avval tizimga kiring")

        if user.is_superuser or user.is_staff or user.role == 'admin':
            return self.queryset.all()

        return self.queryset.filter(id=user.id)

    permission_classes = [IsAdminOrEmployeeOrTeacher|IsStudent]
    search_fields = ['subject__name', 'teacher__user__username', 'group__name', 'day']
    ordering_fields = ['id', 'day']

class GradeViewSet(BaseViewSet):
    queryset = Grade.objects.select_related('student__user', 'subject').all().order_by('-created_at')
    serializer_class = GradeSerializer

    def get_queryset(self):

        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.none()

        user = self.request.user

        if not user or not user.is_authenticated:
            raise NotAuthenticated("Avval tizimga kiring")

        if user.is_superuser or user.is_staff or user.role == 'admin':
            return self.queryset.all()

        return self.queryset.filter(id=user.id)

    permission_classes = [IsTeacher | IsStudent | IsAdminOrEmployee]
    search_fields = ['student__student_id', 'subject__name']
    ordering_fields = ['id', 'created_at']

class AttendanceViewSet(BaseViewSet):
    queryset = Attendance.objects.select_related('student__user', 'subject').all().order_by('-date')
    serializer_class = AttendanceSerializer

    def get_queryset(self):

        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.none()

        user = self.request.user
        if not user or not user.is_authenticated:
            raise NotAuthenticated('Avval tizimga kiring')

        if user.is_superuser or user.is_staff or user.role == 'admin':
            return self.queryset.all()

        return self.queryset.filter(user__id=user.id)



    permission_classes = [IsAdminOrEmployee]
    search_fields = ['student__student_id', 'subject__name']
    ordering_fields = ['id', 'date']

# --------------------- Student ------------------------------------------
class StudentViewSet(BaseViewSet):
    queryset = Student.objects.select_related('user', 'group').all().order_by('-student_id')
    serializer_class = StudentSerializer
    permission_classes = [IsStudent | IsTeacher | IsAdminOrEmployee]
    search_fields = ['student_id', 'user__username', 'group__name']
    ordering_fields = ['id', 'student_id']


    def get_queryset(self):

        user = self.request.user
        if not user or not user.is_authenticated:
            raise NotAuthenticated("Avval tizimga kiring")

        if user.role == 'admin':
            return Student.objects.all()

        elif user.role == 'employee':
            return Student.objects.all()


        elif user.role == 'teacher':

            print("USER TYPE:", type(user))

            return Student.objects.filter(group__teacher__user=user)

        elif user.role == 'student':
            return Student.objects.filter(user=user).select_related('user','group')

        raise PermissionDenied("Sizda ushbu so'rov uchun ruxsat yo'q")


class StudentRecordViewSet(BaseViewSet):
    queryset = StudentRecord.objects.select_related('student__user', 'subject').all().order_by('-id')
    serializer_class = StudentRecordSerializer

    def get_queryset(self):

        if getattr(self,'swagger_fake_view',False):
            return self.queryset.none()

        user = self.request.user
        if not user or not user.is_authenticated:
            raise NotAuthenticated('Avval tizimga kiring')

        if user.is_superuser or user.role == 'admin':
            return self.queryset.all()

        if user.role == 'employee':
            return self.queryset.all()

        if user.role == 'teacher':
            return self.queryset.filter(teacher__user=user)

        if user.role == 'student':
            return self.queryset.filter(student__user=user)

        return self.queryset.none()


    permission_classes = [IsTeacher | IsAdminOrEmployee | IsStudent]
    search_fields = ['student__student_id', 'subject__name']
    ordering_fields = ['id', 'student__student_id']

    @action(detail=False, methods=['get'], permission_classes=[IsAdminOrEmployeeOrTeacher])
    def top_grade_student(self, request):
        top_students = (
            Student.objects
            .annotate(avg_grade=Avg('records__grade'))
            .order_by('-avg_grade')[:3]
        )
        data = [{
            'student_id': s.student_id,
            'full_name': f"{getattr(s.user.profile, 'first_name', '')} {getattr(s.user.profile, 'last_name', '')}".strip(),
            'group': getattr(s.group, 'name', None),
            'average_grade': getattr(s, 'avg_grade', None) or (s.avg_grade if hasattr(s, 'avg_grade') else None)
        } for s in top_students]
        return Response({'results': data})

    @action(detail=True, methods=['get'], permission_classes=[IsStudent | IsAdminOrEmployeeOrTeacher])
    def average_rating(self, request, pk=None):
        student_record = self.get_object()
        student = student_record.student
        avg_rating = student.records.aggregate(avg=Avg('grade'))['avg']
        return Response({
            'student_id': student.student_id,
            'full_name': f"{getattr(student.user.profile, 'first_name', '')} {getattr(student.user.profile, 'last_name', '')}".strip(),
            'group': getattr(student.group, 'name', None),
            'average_rating': avg_rating or 'Hali baholar mavjud emas'
        })

class StudentComplaintViewSet(BaseViewSet):
    queryset = StudentComplaint.objects.select_related('student__user').all().order_by('-id')
    serializer_class = StudentComplaintSerializer

    def get_queryset(self):

        if getattr(self,'swagger_fake_view',False):
            return self.queryset.none()

        user = self.request.user
        if not user or not user.is_authenticated:
            raise NotAuthenticated('Avval tizimga kiring')

        if user.is_superuser or user.role == 'admin':
            return self.queryset.all()

        if user.role == 'employee':
            return self.queryset.all()

        if user.role == 'teacher':
            return self.queryset.filter(teacher__user=user)

        if user.role == 'student':
            return self.queryset.filter(student__user=user)

        return self.queryset.none()

    permission_classes = [IsStudent | IsAdminOrEmployee]

# --------------------- Employee ------------------------------------------
class EmployeeViewSet(BaseViewSet):
    queryset = Employee.objects.select_related('user', 'department').all().order_by('-id')
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        if getattr(self,'swagger_fake_view',False):
            return self.queryset.none()

        user = self.request.user
        if not user or not user.is_authenticated:
            raise NotAuthenticated("Avval tizimga kiring")

        if user.is_superuser and user.role == 'admin':
            return self.queryset.all()

        if user.is_staff and user.role == 'employee':
            return self.queryset.all()

        return self.queryset.none()

    permission_classes = [IsAdminOrEmployee]
    search_fields = ['user__username', 'position', 'department__name']
    ordering_fields = ['id', 'user__username']

class TaskViewSet(BaseViewSet):
    queryset = Task.objects.select_related('employee__user').all().order_by('deadline')
    serializer_class = TaskSerializer

    def get_queryset(self):

        if getattr(self,'swagger_fake_view',False):
            return self.queryset.none()

        user = self.request.user
        if not user or not user.is_authenticated:
            raise NotAuthenticated('Avval tizimga kiring')

        if user.is_superuser or user.role == 'admin':
            return self.queryset.all()

        if user.role == 'employee':
            return self.queryset.all()

        if user.role == 'teacher':
            return self.queryset.filter(teacher__user=user)

        if user.role == 'student':
            return self.queryset.filter(student__user=user)

        return self.queryset.none()

    permission_classes = [IsAdminOrEmployee]
    search_fields = ['employee__user__username', 'title', 'description', 'status']
    ordering_fields = ['id', 'deadline']

class ReportViewSet(BaseViewSet):
    queryset = Report.objects.select_related('employee__user').all().order_by('-created_at')
    serializer_class = ReportSerializer

    def get_queryset(self):

        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.none()

        user = self.request.user
        if not user or not user.is_authenticated:
            raise NotAuthenticated('Avval tizimga kiring')

        if user.is_superuser or user.role == 'admin':
            return self.queryset.all()

        if user.role == 'employee':
            return self.queryset.all()

        return self.queryset.none()

    permission_classes = [IsAdminOrEmployee]
    search_fields = ['employee__user__username', 'report_text']
    ordering_fields = ['id', 'created_at']
