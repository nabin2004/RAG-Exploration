from django.db import models
from django.contrib.postgres.fields import ArrayField

class Document(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Chunk(models.Model):
    document = models.ForeignKey(Document, related_name='chunks', on_delete=models.CASCADE)
    text = models.TextField()
    position = models.PositiveIntegerField()

    def __str__(self):
        return f"Chunk {self.position} of Document {self.document_id}"

class Embedding(models.Model):
    chunk = models.OneToOneField(Chunk, related_name='embedding', on_delete=models.CASCADE)
    vector = ArrayField(models.FloatField(), size=384)  # Adjust size as needed

    def __str__(self):
        return f"Embedding for Chunk {self.chunk_id}"
