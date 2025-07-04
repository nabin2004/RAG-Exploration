# Generated by Django 5.2.3 on 2025-06-22 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.CharField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('RUNNING', 'Running'), ('COMPLETED', 'Completed'), ('FAILED', 'Failed')], default='PENDING', max_length=20)),
                ('result', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('started_at', models.DateTimeField(blank=True, null=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
