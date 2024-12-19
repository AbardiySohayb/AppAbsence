from django.contrib.auth.models import AbstractUser
from django.db import models

# Custom User (Professeur)
class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)  # Date de naissance (facultative)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'custom_user'  # Nom personnalisé pour la table CustomUser

# Classe pour un étudiant
class Student(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    classroom = models.ForeignKey('Classroom', on_delete=models.CASCADE, related_name='students')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = 'student'  # Nom personnalisé pour la table Student

# Classe pour une salle de classe
class Classroom(models.Model):
    name = models.CharField(max_length=255)
    professors = models.ManyToManyField(CustomUser, related_name='classrooms')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'classroom'  # Nom personnalisé pour la table Classroom

# Absence d'un étudiant dans une classe
class Absence(models.Model):
    student = models.ForeignKey(Student, related_name='absences', on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, related_name='absences', on_delete=models.CASCADE)
    date = models.DateField()
    reason = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Absence for {self.student} in {self.classroom} on {self.date}"

    class Meta:
        db_table = 'absence'  # Nom personnalisé pour la table Absence

# Motivation d'un étudiant dans une classe
class Motivation(models.Model):
    student = models.ForeignKey(Student, related_name='motivations', on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, related_name='motivations', on_delete=models.CASCADE)
    date = models.DateField()
    level = models.CharField(max_length=255)

    def __str__(self):
        return f"Motivation level of {self.student} in {self.classroom} on {self.date}"

    class Meta:
        db_table = 'motivation'  # Nom personnalisé pour la table Motivation
