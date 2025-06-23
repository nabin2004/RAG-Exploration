from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls), 
    
    path('api/core/', include('core.urls')),
    # path('api/api/', include('api.urls')),
    # path('api/rag/', include('rag.urls')),
    # path('api/tasks/', include('tasks.urls')),
    # path('api/auth/', include('django.contrib.auth.urls')), 
]
