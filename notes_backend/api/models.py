from django.db import models
from django.contrib.auth.models import User

# PUBLIC_INTERFACE
class Note(models.Model):
    """
    A model representing a personal note.
    """
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, related_name='notes', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
