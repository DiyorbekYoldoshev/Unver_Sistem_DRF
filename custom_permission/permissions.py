from rest_framework.permissions import BasePermission, SAFE_METHODS


# 1. Faqat admin (superuser yoki staff)
class IsAdminUserOrReadOnly(BasePermission):

    """Admin yozishi mumkin boshqalar o'qiy oladi"""

    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

# 2. Faqat super admin (superuser=True)

class IsSuperAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_superuser


# 3. Faqat Employee uchun
class IsEmployee(BasePermission):
    """Employee role tekshiradi"""
    def has_permission(self, request, view):
        return hasattr(request.user,'role') and request.user.role == 'employee'

# 4. Faqat Teacher uchun
class IsTeacher(BasePermission):
    """Teacher rolini tekshirdi"""

    def has_permission(self, request, view):
        return hasattr(request.user,'role') and request.user.role == 'teacher'

# 5. Faqat Student uchun
class IsStudent(BasePermission):
    """Student rolini tekshiradi"""

    def has_permission(self, request, view):
        return hasattr(request.user,'role') and request.user.role == 'student'


# 6.