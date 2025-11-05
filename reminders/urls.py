from django.urls import path
from . import views

urlpatterns = [
    path('paciente/', views.dashboard_paciente, name='dashboard_paciente'),
    path('lembretes/', views.lembretes_view, name='lembretes'),
    path('excluir/<int:pk>/', views.excluir_alarme, name='excluir_alarme'),
    path('verificar/', views.verificar_alarmes, name='verificar_alarmes'),
]
