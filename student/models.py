from django.db import models
from django.conf import settings
from core.models import Group, Subject


class Student(models.Model):
    STATUS_CHOICES = [
        ('active', 'Faol'),
        ('graduated', 'Bitirgan'),
        ('expelled', 'Haydalgan'),
        ('on_leave', 'Akademik ta’tilda'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='students')
    enrollment_year = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.student_id})"


class StudentRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='records')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.student.student_id} - {self.subject.name} ({self.grade})"


class StudentComplaint(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='complaints')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Complaint by {self.student.student_id}"
