from django.urls import path
from . import views

urlpatterns = [
    path('agente/', views.dashboard_agente, name='dashboard_agente'),
    path('medico/', views.dashboard_medico, name='dashboard_medico'),
    path('cadastrar/', views.cadastrar_paciente, name='cadastrar_paciente'),
    path('editar/<int:pk>/', views.editar_paciente, name='editar_paciente'),
    path('excluir/<int:pk>/', views.excluir_paciente, name='excluir_paciente'),
    # APIs para o mapa
    path('api/mapa/agente/', views.mapa_dados_agente, name='mapa_dados_agente'),
    path('api/mapa/medico/', views.mapa_dados_medico, name='mapa_dados_medico'),
]
