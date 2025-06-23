# signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Document, Chunk
from .utils import chunk_text
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Document, Chunk, Embedding, ChatMessage
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


@receiver(post_save, sender=Document)
def create_chunks_on_document_save(sender, instance, created, **kwargs):
    if not created:
        instance.chunks.all().delete()

    chunks = chunk_text(instance.content)

    for i, content in enumerate(chunks):
        Chunk.objects.create(document=instance, content=content, index=i)

embed_model = SentenceTransformer("all-MiniLM-L6-v2")

@receiver(post_save, sender=Chunk)
def create_embedding_for_chunk(sender, instance, created, **kwargs):
    if created:
        print(f"Embedding signal triggered for Chunk ID {instance.id}")  # debug print
        vector = embed_model.encode([instance.content], convert_to_numpy=True)[0]
        embedding = Embedding(chunk=instance, vector=vector.tolist())
        embedding.save()
        print(f"Created embedding for chunk {instance.id}")
        
@receiver(post_delete, sender=Chunk)
def delete_embedding_on_chunk_delete(sender, instance, **kwargs):
    embedding = getattr(instance, "embedding", None)
    if embedding:
        embedding.delete()
        print(f"Deleted embedding for chunk {instance.id}")

@receiver(post_save, sender=ChatMessage)
def update_chat_session_timestamp(sender, instance, created, **kwargs):
    if created:
        session = instance.session
        session.save() 
