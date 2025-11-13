from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.setup_view import setup_view
from accounts.popular_mapa_view import popular_mapa_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('setup/', setup_view, name='setup'),  # URL temporária para criar dados
    path('popular-mapa/', popular_mapa_view, name='popular_mapa'),  # Popular dados do mapa
    path('', include('accounts.urls')),
    path('pacientes/', include('patients.urls')),
    path('lembretes/', include('reminders.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
