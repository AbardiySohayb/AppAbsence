from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser, Classroom, Student, Absence, Motivation
from .serializers import CustomUserSerializer, ClassroomSerializer, StudentSerializer, AbsenceSerializer, MotivationSerializer
from django.contrib.auth import get_user_model

# Vue pour le login
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Authentification
        user = authenticate(username=username, password=password)

        if user:
            return Response({
                "message": "Login successful",
                "username": user.username,
                "user_id": user.id  # Ajout de l'ID utilisateur
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)

# Vue pour récupérer les classes du professeur (professeur connecté)
class ProfessorClassroomsView(APIView):
    def get(self, request, user_id):  # Ajout explicite du paramètre user_id
        if not user_id:
            return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_id = int(user_id)
        except ValueError:
            return Response({"error": "Invalid user_id"}, status=status.HTTP_400_BAD_REQUEST)

        # Vérifier si l'utilisateur existe
        try:
            professor = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "Professor not found"}, status=status.HTTP_404_NOT_FOUND)

        classrooms = Classroom.objects.filter(professors__id=user_id)  # Récupérer les classes par l'ID du professeur
        data = []

        for classroom in classrooms:
            # Compter le nombre d'étudiants pour chaque salle de classe
            student_count = Student.objects.filter(classroom_id=classroom.id).count()
            classroom_data = ClassroomSerializer(classroom).data
            classroom_data['student_count'] = student_count
            data.append(classroom_data)

        return Response(data, status=status.HTTP_200_OK)

# Vue pour récupérer les étudiants dans une classe
class ClassroomStudentsView(APIView):
    def get(self, request, classroom_id):
        classroom = Classroom.objects.get(id=classroom_id)  # Récupérer la classe
        students = classroom.students.all()  # Récupérer les étudiants dans cette classe
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Vue pour récupérer les absences d'un étudiant
class StudentAbsencesView(APIView):
    def get(self, request, student_id):
        student = Student.objects.get(id=student_id)
        absences = Absence.objects.filter(student=student)
        serializer = AbsenceSerializer(absences, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Vue pour récupérer les motivations d'un étudiant
class StudentMotivationsView(APIView):
    def get(self, request, student_id):
        student = Student.objects.get(id=student_id)
        motivations = Motivation.objects.filter(student=student)
        serializer = MotivationSerializer(motivations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DashboardView(APIView):
    def get(self, request, user_id):
        if not user_id:
            return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_id = int(user_id)
        except ValueError:
            return Response({"error": "Invalid user_id"}, status=status.HTTP_400_BAD_REQUEST)

        # Récupérer le nombre de classes associées au professeur
        classes_count = Classroom.objects.filter(professors__id=user_id).count()

        # Récupérer le nombre d'étudiants par classe
        students_count = 0
        classrooms = Classroom.objects.filter(professors__id=user_id)
        for classroom in classrooms:
            students_count += Student.objects.filter(classroom=classroom).count()

        # Structure de la réponse
        data = {
            "classes_count": classes_count,
            "students_count": students_count,
        }

        return Response(data, status=status.HTTP_200_OK)
