from rest_framework import viewsets
from student.serializers import *
from teacher.serializers import *
from rest_framework.permissions import IsAuthenticated



class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    # permission_classes = [IsAuthenticated]
    serializer_class = StudentSerializer



class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    # permission_classes = [IsAuthenticated]
    serializer_class = TeacherSerializer



