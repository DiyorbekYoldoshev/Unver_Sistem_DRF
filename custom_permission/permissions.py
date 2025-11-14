from rest_framework.permissions import BasePermission
from accounts.models import User

# =========================
#  ROLE CONSTANTS
# =========================
ADMIN = 'admin'
EMPLOYEE = 'employee'
TEACHER = 'teacher'
STUDENT = 'student'


# =========================
#  SINGLE ROLE CHECKS
# =========================

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == ADMIN
        )


class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == EMPLOYEE
        )


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == TEACHER
        )


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == STUDENT
        )


# =========================
#  MULTI ROLE CHECKS
# =========================

class IsAdminOrEmployee(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role in [ADMIN, EMPLOYEE]
        )


class IsAdminOrTeacher(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role in [ADMIN, TEACHER]
        )


class IsAdminOrStudent(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role in [ADMIN, STUDENT]
        )


class IsAdminOrEmployeeOrTeacher(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role in [ADMIN, EMPLOYEE, TEACHER]
        )


# =========================
#  SELF OR ADMIN
# =========================

class IsSelfOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated and
            (obj == request.user or request.user.role == ADMIN)
        )
