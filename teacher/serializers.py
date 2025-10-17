from rest_framework import serializers
from .models import Teacher, TeacherActivity, TeacherSchedule


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = "__all__"


class TeacherActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherActivity
        fields = "__all__"


class TeacherScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherSchedule
        fields = "__all__"
