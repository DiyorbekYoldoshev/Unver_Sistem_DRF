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
        unique_together = ('role','permission')

    def __str__(self):
        return f"{self.role.name} - {self.permission.code_name}"


class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='users')
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'role')

    def __str__(self):
        return f"{self.user.username} → {self.role.name}"


class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.action} ({self.timestamp})"
