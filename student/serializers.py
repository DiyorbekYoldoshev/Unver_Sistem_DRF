from rest_framework import serializers
from .models import Student,StudentRecord,StudentComplaint

class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = "__all__"


class StudentRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentRecord
        fields = "__all__"


class StudentComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentComplaint
        fields = "__all__"


