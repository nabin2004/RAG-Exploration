from django.contrib import admin
from .models import Document, Chunk, Embedding

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')
    search_fields = ('title',)

@admin.register(Chunk)
class ChunkAdmin(admin.ModelAdmin):
    list_display = ('document', 'position')
    search_fields = ('text',)
    list_filter = ('document',)

@admin.register(Embedding)
class EmbeddingAdmin(admin.ModelAdmin):
    list_display = ('chunk',)
