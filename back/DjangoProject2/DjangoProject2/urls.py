from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import LoginView, ProfessorClassroomsView, ClassroomStudentsView, StudentAbsencesView, \
    StudentMotivationsView, DashboardView

urlpatterns = [
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/professor/<int:user_id>/classrooms/', ProfessorClassroomsView.as_view(), name='professor-classrooms'),
    path('api/classroom/<int:classroom_id>/students/', ClassroomStudentsView.as_view(), name='classroom-students'),
    path('api/student/<int:student_id>/absences/', StudentAbsencesView.as_view(), name='student-absences'),
    path('api/student/<int:student_id>/motivations/', StudentMotivationsView.as_view(), name='student-motivations'),
    # Endpoint pour obtenir le token
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Endpoint pour rafraîchir le token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('dashboard/<int:user_id>/', DashboardView.as_view(), name='dashboard'),
]
