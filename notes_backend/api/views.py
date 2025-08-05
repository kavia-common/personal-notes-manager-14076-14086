from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from .models import Note
from .serializers import (
    NoteSerializer,
    RegisterSerializer,
    LoginSerializer,
    UserSerializer,
)
from rest_framework.permissions import IsAuthenticated, AllowAny

@api_view(['GET'])
def health(request):
    """Health check endpoint."""
    return Response({"message": "Server is up!"})

# PUBLIC_INTERFACE
class NoteListCreateView(generics.ListCreateAPIView):
    """
    GET: List user's notes. 
    POST: Create a new note for the authenticated user.
    """
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# PUBLIC_INTERFACE
class NoteRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve a note by id.
    PUT: Update a note.
    DELETE: Delete a note.
    """
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)

# PUBLIC_INTERFACE
class RegisterView(APIView):
    """
    User registration endpoint.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Automatic login after registration (optional)
            login(request, user)
            return Response({
                "user": UserSerializer(user).data,
                "message": "Registration successful."
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# PUBLIC_INTERFACE
class LoginView(APIView):
    """
    User login endpoint.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return Response({
                    "user": UserSerializer(user).data,
                    "message": "Login successful."
                }, status=status.HTTP_200_OK)
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# PUBLIC_INTERFACE
class LogoutView(APIView):
    """
    User logout endpoint.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful."}, status=status.HTTP_200_OK)

# PUBLIC_INTERFACE
class UserView(APIView):
    """
    Get details of the authenticated user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
