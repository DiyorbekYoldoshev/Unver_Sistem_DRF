from rest_framework.permissions import BasePermission,SAFE_METHODS


class IsAdminOrEmployee(BasePermission):

    def has_permission(self, request, view):
        if not request.user or request.user.is_authenticated:
            return False

        if request.method == 'DELETE':
            return request.user.role == 'admin'
        return request.user.role in ['admin','employee']

class AdminReadOnly(BasePermission):

    """Allow authenticated users read-only access"""

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 'admin'
            and request.methodin in SAFE_METHODS
        )

class EmployeeReadOnly(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 'employee'
            and request.method in SAFE_METHODS
        )