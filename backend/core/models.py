from django.db import models
from django.contrib.postgres.fields import ArrayField

class Document(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



class Chunk(models.Model):
    document = models.ForeignKey("Document", on_delete=models.CASCADE, related_name="chunks")
    content = models.TextField()
    index = models.IntegerField()
    # embedding = models.JSONField(null=True, blank=True)
    
    from django.utils import timezone
    created_at = models.DateTimeField(default=timezone.now)
    
    
class Embedding(models.Model):
    from django.db.models import JSONField
    
    chunk = models.OneToOneField(Chunk, on_delete=models.CASCADE, related_name="embedding")
    # vector = ArrayField(models.FloatField(), size=384) 
    vector = JSONField()

    def __str__(self):
        return f"Embedding for Chunk {self.chunk_id}"


class ChatSession(models.Model):
    """Track conversation sessions for context preservation."""
    session_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Session {self.session_id}"


class ChatMessage(models.Model):
    """Store chat history with roles and timestamps."""
    session = models.ForeignKey(ChatSession, related_name='messages', on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=[('user', 'User'), ('bot', 'Bot')])
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role} @ {self.timestamp}"
