from django.db import models
from django.contrib.auth.models import User


# 🏫 Fakultet, Bo‘lim, Guruh
class Faculty(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='departments')

    def __str__(self):
        return f"{self.name} ({self.faculty.name})"


class Group(models.Model):
    name = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='groups')

    def __str__(self):
        return f"{self.name} - {self.department.name}"


# 📘 Fanlar
class Subject(models.Model):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=10, unique=True)
    credit = models.PositiveIntegerField(default=3)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='subjects')

    def __str__(self):
        return f"{self.name} ({self.code})"


# 📆 Dars jadvali
class Schedule(models.Model):
    DAYS_OF_WEEK = [
        ('monday', 'Dushanba'),
        ('tuesday', 'Seshanba'),
        ('wednesday', 'Chorshanba'),
        ('thursday', 'Payshanba'),
        ('friday', 'Juma'),
        ('saturday', 'Shanba'),
    ]
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teacher_schedules')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_schedules')
    day = models.CharField(max_length=15, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.subject.name} ({self.group.name}) - {self.day}"


# 🎓 Baholar
class Grade(models.Model):
    EXAM_TYPES = [
        ('midterm', 'Oraliq imtihon'),
        ('final', 'Yakuniy imtihon'),
        ('project', 'Loyiha'),
    ]
    student = models.ForeignKey('student.Student', on_delete=models.CASCADE, related_name='grades')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    exam_type = models.CharField(max_length=10, choices=EXAM_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.subject.name}: {self.score}"


# 📋 Davomat
class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Kelgan'),
        ('absent', 'Kelmagan'),
        ('late', 'Kechikkan'),
    ]
    student = models.ForeignKey('student.Student', on_delete=models.CASCADE, related_name='attendances')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.student} - {self.date} ({self.status})"
