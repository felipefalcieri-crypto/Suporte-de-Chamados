from django.contrib import admin
from django.urls import path, include
from helpdesk import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.vizualizarHome, name='home'),
    path('tickets_abertos/', views.ticketsAbertos, name='tickets_abertos'),
    path('ticket/<int:chamado_id>/', views.detalhe_ticket, name='detalhe_ticket'),
    path('ticket/<int:chamado_id>/atualizar/', views.atualizar_chamado, name='atualizar_chamado'),
    path('chamado/abrir/', views.abertura_chamado, name='abertura_chamado'),
]
