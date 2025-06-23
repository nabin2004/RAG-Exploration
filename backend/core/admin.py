from django.contrib import admin
from .models import Document, Chunk, Embedding, ChatSession, ChatMessage

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'uploaded_at')
    search_fields = ('title',)


@admin.register(Chunk)
class ChunkAdmin(admin.ModelAdmin):
    list_display = ('id', 'document', 'index')
    list_filter = ('document',)
    search_fields = ('text',)


@admin.register(Embedding)
class EmbeddingAdmin(admin.ModelAdmin):
    list_display = ('id', 'chunk')
    search_fields = ('chunk__text',)


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'session_id', 'created_at', 'updated_at')
    search_fields = ('session_id',)


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'session', 'role', 'timestamp')
    list_filter = ('role',)
    search_fields = ('content',)
