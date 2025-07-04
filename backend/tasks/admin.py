from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_id', 'name', 'status', 'created_at', 'started_at', 'completed_at')
    list_filter = ('status', 'created_at', 'started_at', 'completed_at')
    search_fields = ('task_id', 'name')
