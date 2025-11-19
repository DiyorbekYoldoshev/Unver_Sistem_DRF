# 1 - Importlar
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.base_user import BaseUserManager

# 2 - Custom Managers (modelga qarab bazi hollarda yoziladi
class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The username must be set")
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        user = self.model(username=username, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('role','admin')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(username, password, **extra_fields)


phone_regex = RegexValidator(
    regex=r'^\+998\d{9}$',
    message="Telefon raqamni shu tartibda kiriting: +998911234567"
)

# 3 - Model Class (Fields,Relations)
class User(AbstractBaseUser, PermissionsMixin):
    # 4 - Global constants / Choices (fielsga qarab)
    ADMIN = 'admin'
    EMPLOYEE = 'employee'
    TEACHER = 'teacher'
    STUDENT = 'student'

    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (EMPLOYEE, 'Employee'),
        (TEACHER, 'Teacher'),
        (STUDENT, 'Student'),
    ]
    # 5 - Fieldlar
    username = models.CharField(max_length=150, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(validators=[phone_regex], max_length=13, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Erkak'), ('female', 'Ayol')], blank=True)
    birth_date = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    # 6 - Managers biriktirish (objects = ...)
    objects = UserManager()


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    # 7 - str()
    def __str__(self):
        return f"{self.username} ({self.role})"

# Shartga qarab
# Custom model methods
# save() override (agar bo‘lsa)
# signals bo‘lsa — models.py ichida emas, alohida signals.py da bo‘ladi