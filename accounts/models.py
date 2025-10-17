from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('employee', 'Employee'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    def __str__(self):
        return f"{self.username} ({self.role})"



phone_regex = RegexValidator(
    regex=r'^\+998\d{9}$',
    message="Telefon raqamni shu tartibda kiriting: +998911234567"
)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(validators=[phone_regex], max_length=13, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Erkak'), ('female', 'Ayol')])
    birth_date = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    image = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} profili"
