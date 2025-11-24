from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'employee'


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'teacher'


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'student'


class IsAdminOrEmployeeOrTeacher(BasePermission):
    def has_permission(self, request, view):
        u = request.user
        return u.is_authenticated and (u.role in ['admin', 'employee', 'teacher'])


class IsSuperAdmin(BasePermission):
    message = "Faqat superadmin boshqarishi mumkin"

    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.is_superuser and user.role == 'admin'
