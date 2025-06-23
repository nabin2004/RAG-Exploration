# core/serializers.py
from rest_framework import serializers
from .models import ChatMessage, ChatSession, Chunk, Document, Embedding

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = '__all__'

class ChatSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatSession
        fields = '__all__'

class ChunkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chunk
        fields = '__all__'

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

class EmbeddingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Embedding
        fields = '__all__'
