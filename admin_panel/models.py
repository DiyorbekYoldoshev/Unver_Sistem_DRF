from django.contrib.auth.models import AbstractUser
from django.db import models


# admin_panel (boshqaruv va ruxsat tizimi)
# Model	Maydonlar	Aloqalar

class Role(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.name

class Permission(models.Model):

    code_name = models.CharField(max_length=100)
    description = models.CharField(max_length=250, null=True, blank=True)

class RolePermission(models.Model):

    pass