from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Note

# PUBLIC_INTERFACE
class NoteSerializer(serializers.ModelSerializer):
    """
    Serializer for the Note model.
    """
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'owner']

# PUBLIC_INTERFACE
class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user instances (for listing or detail).
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# PUBLIC_INTERFACE
class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user.
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user

# PUBLIC_INTERFACE
class LoginSerializer(serializers.Serializer):
    """
    Serializer for logging in a user.
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
