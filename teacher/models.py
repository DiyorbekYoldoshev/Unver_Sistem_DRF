from django.db import models
from accounts.models import User
from core.models import Department, Subject


class Teacher(models.Model):
    DEGREE_CHOICES = [
        ('bachelor', 'Bakalavr'),
        ('master', 'Magistr'),
        ('phd', 'PhD / Doktor'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)  # Masalan: "Professor", "Dotsent"
    specialization = models.CharField(max_length=150)  # Masalan: "Sun’iy intellekt", "Matematika"
    degree = models.CharField(max_length=20, choices=DEGREE_CHOICES)
    hire_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.position}"


class TeacherSchedule(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    day_of_week = models.CharField(
        max_length=10,
        choices=[
            ('monday', 'Dushanba'),
            ('tuesday', 'Seshanba'),
            ('wednesday', 'Chorshanba'),
            ('thursday', 'Payshanba'),
            ('friday', 'Juma'),
            ('saturday', 'Shanba'),
        ],
    )
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.teacher.user.username} - {self.subject} ({self.day_of_week})"


class TeacherActivity(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.teacher.user.username} - {self.title}"
