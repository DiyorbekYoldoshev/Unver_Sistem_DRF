from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from .models import User

from django.utils.html import format_html

class CustomCreationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username','role','is_active')



class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'role', 'is_staff', 'is_active','avatar')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone', 'role', 'avatar')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )
    def avatar_tag(self,obj):
        if obj.avatar:
            return format_html('<img src="{}" width="40" height="40" style="border-radius:50%;"/>', obj.avatar.url)
        return "-"
    avatar_tag.short_description = 'Avatar'

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username',)
    ordering = ('username',)


admin.site.register(User, CustomUserAdmin)
