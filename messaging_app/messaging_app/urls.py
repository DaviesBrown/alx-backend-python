from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chats.urls')),  # Mount chats API under /api/
    path('api-auth/', include('rest_framework.urls')),  # DRF browsable API login/logout
]

