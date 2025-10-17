from django.db import models
from django.conf import settings
from core.models import Department

"""
🧰 Employees (Universitet xodimlari)
"""

class Employee(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    hire_date = models.DateTimeField(auto_now_add=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Task(models.Model):
    STATUS_CHOICES = [
        ('new', 'Yangi'),
        ('in_progress', 'Bajarilmoqda'),
        ('done', 'Bajarilgan'),
    ]
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    deadline = models.DateTimeField()

    def __str__(self):
        return f"{self.title} — {self.employee.user.username}"


class Report(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='reports')
    report_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report by {self.employee.user.username}"
