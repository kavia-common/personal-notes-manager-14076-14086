from django.urls import path
from .views import (
    health,
    NoteListCreateView,
    NoteRetrieveUpdateDestroyView,
    RegisterView,
    LoginView,
    LogoutView,
    UserView,
)

urlpatterns = [
    path('health/', health, name='Health'),
    # Authentication
    path('auth/register/', RegisterView.as_view(), name='auth-register'),
    path('auth/login/', LoginView.as_view(), name='auth-login'),
    path('auth/logout/', LogoutView.as_view(), name='auth-logout'),
    path('auth/user/', UserView.as_view(), name='auth-user'),
    # Notes
    path('notes/', NoteListCreateView.as_view(), name='note-list-create'),
    path('notes/<int:pk>/', NoteRetrieveUpdateDestroyView.as_view(), name='note-detail'),
]
