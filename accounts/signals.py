from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import User


@receiver(post_save, sender=User)
def assign_role_and_permissions(sender, instance, created, **kwargs):
    """
    Yangi user yaratilganda, role ga qarab avtomatik group va permission beriladi
    """
    if not created:
        return

    # Groupni yarat (agar mavjud bo'lmasa)
    group, created = Group.objects.get_or_create(name=instance.role)

    # Role bo‘yicha permission belgilash
    if instance.role == 'admin':
        # Admin barcha ruxsatlarni oladi
        instance.is_staff = True
        instance.is_superuser = True
        instance.save()
        return

    elif instance.role == 'teacher':
        # Teacher uchun ma’lum model ruxsatlari
        perms = Permission.objects.filter(
            content_type__app_label__in=['teacher', 'core'],
            codename__in=['view_teacher', 'change_teacher', 'view_schedule']
        )
        group.permissions.set(perms)

    elif instance.role == 'student':
        perms = Permission.objects.filter(
            content_type__app_label__in=['student', 'core'],
            codename__in=['view_student', 'view_schedule']
        )
        group.permissions.set(perms)

    elif instance.role == 'employee':
        perms = Permission.objects.filter(
            content_type__app_label__in=['employees'],
            codename__in=['view_employee', 'change_employee']
        )
        group.permissions.set(perms)

    # Groupni userga biriktirish
    instance.groups.add(group)
