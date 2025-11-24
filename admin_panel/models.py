from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()



class Role(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False,unique=True)
    description = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.name

class Permission(models.Model):

    code_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.code_name

class RolePermission(models.Model):
    role = models.ForeignKey(Role,on_delete=models.CASCADE,related_name='permissions')
    permission = models.ForeignKey(Permission,on_delete=models.CASCADE,related_name='roles')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['role','permission'],
                name='unique_role_permission'
            )
        ]

    def __str__(self):
        return f"{self.role.name} - {self.permission.code_name}"


class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='users')
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user','role'],
                name='unique_user_role'
            )
        ]

    def __str__(self):
        return f"{self.user.username} → {self.role.name}"


class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    meta = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        user_repr = self.user.username if self.user else "Anon"
        return f"{user_repr} - {self.action} ({self.timestamp.isoformat()})"


class AcademicYear(models.Model):
    year = models.CharField(max_length=20, null=True,blank=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.year

class SystemSetting(models.Model):
    key = models.CharField(max_length=150,unique=True)
    value = models.JSONField()
    description = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.key
