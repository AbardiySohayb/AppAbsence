from rest_framework import serializers
from .models import CustomUser, Classroom, Student, Absence, Motivation

# Sérialiseur pour CustomUser
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'date_of_birth']

# Sérialiseur pour Classroom
class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ['id', 'name', 'professors']

# Sérialiseur pour Student
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'classroom']

# Sérialiseur pour Absence
class AbsenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Absence
        fields = ['id', 'student', 'classroom', 'date', 'reason']

# Sérialiseur pour Motivation
class MotivationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motivation
        fields = ['id', 'student', 'classroom', 'date', 'level']
