from django.contrib import admin
from .models import UserProfile, QueryLog

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'preferred_language', 'created_at')
    search_fields = ('user__username', 'preferred_language')

@admin.register(QueryLog)
class QueryLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'query_text', 'created_at')
    search_fields = ('query_text', 'user__username')
    list_filter = ('created_at',)
