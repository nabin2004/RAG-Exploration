from django.db import models
from django.utils import timezone

class Task(models.Model):
    TASK_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('RUNNING', 'Running'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]

    task_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=TASK_STATUS_CHOICES, default='PENDING')
    result = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.task_id}) - {self.status}"

    def mark_started(self):
        self.status = 'RUNNING'
        self.started_at = timezone.now()
        self.save()

    def mark_completed(self, result=None):
        self.status = 'COMPLETED'
        self.completed_at = timezone.now()
        self.result = result
        self.save()

    def mark_failed(self, result=None):
        self.status = 'FAILED'
        self.completed_at = timezone.now()
        self.result = result
        self.save()
