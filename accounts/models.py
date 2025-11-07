from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager,PermissionsMixin
from django.core.validators import RegexValidator

class UserManager(BaseUserManager):

    def create_user(self,username,password=None,**extra_fields):
        if not username:
            return ValueError("username must have an email")
        user =self.model(username=username,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,username,password,**extra_fields):
        extra_fields.setdefault('role','admin')
        extra_fields.setdefault('is_staff','True')
        extra_fields.setdefault('is_superuser','True')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self.create_superuser(username,password,**extra_fields)


class User(AbstractUser,PermissionsMixin):
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

    USERNAME_FIELDS = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()


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
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    image = models.ImageField(upload_to='profiles/', blank=True, null=True)


    def __str__(self):
        return f"{self.user.username} profili"
