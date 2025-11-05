from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.setup_view import setup_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('setup/', setup_view, name='setup'),  # URL temporária para criar dados
    path('', include('accounts.urls')),
    path('pacientes/', include('patients.urls')),
    path('lembretes/', include('reminders.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
