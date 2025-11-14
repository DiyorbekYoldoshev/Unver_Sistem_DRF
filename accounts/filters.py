from .models import *
from django_filters import rest_framework as django_filters
from employees.models import *


class UserFilter(django_filters.FilterSet):
    role = django_filters.CharFilter(field_name='role',lookup_expr='icontains')
    username = django_filters.CharFilter(field_name='username',lookup_expr='icontains')

    class Meta:
        model = User
        fields = ['role','username']

class ProfileFilter(django_filters.FilterSet):

    user = django_filters.CharFilter(field_name='user__username', lookup_expr='icontains')
    first_name = django_filters.CharFilter(field_name='first_name', lookup_expr='icontains')
    last_name = django_filters.CharFilter(field_name='last_name', lookup_expr='icontains')
    phone = django_filters.CharFilter(field_name='phone', lookup_expr='icontains')
    gender = django_filters.CharFilter(field_name='gender', lookup_expr='icontains')
    address = django_filters.CharFilter(field_name='address', lookup_expr='icontains')

    class Meta:
        model = User
        fields = ['user', 'first_name', 'last_name', 'phone', 'gender', 'address']


# Employees Filter

class EmployeeFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(field_name='user__username', lookup_expr='icontains')
    position = django_filters.CharFilter(field_name='position', lookup_expr='icontains')
    department = django_filters.CharFilter(field_name='department__title', lookup_expr='icontains')

    class Meta:
        model = Employee
        fields = ['user', 'position', 'department']


class TaskFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(field_name='user__username', lookup_expr='icontains')
    employee = django_filters.CharFilter(field_name='employee__user__username', lookup_expr='icontains')
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    description = django_filters.CharFilter(field_name='description', lookup_expr='icontains')
    status = django_filters.ChoiceFilter(choices=Task._meta.get_field('status').choices)
    class Meta:
        model = Task
        fields = ['user', 'employee', 'title', 'description', 'status']


class ReportFilter(django_filters.FilterSet):
    employee = django_filters.CharFilter(field_name='employee__user__username', lookup_expr='icontains')
    report_text = django_filters.CharFilter(field_name='report_text', lookup_expr='icontains')

    class Meta:
        model = Report
        fields = ['report_text', 'employee']