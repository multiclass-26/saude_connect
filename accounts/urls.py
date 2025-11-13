from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('logout/', views.logout_view, name='logout'),
    path('comunidade/', views.comunidade_view, name='comunidade'),
    path('informacoes/', views.informacoes_view, name='informacoes'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('mapa/', views.mapa_view, name='mapa'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]
