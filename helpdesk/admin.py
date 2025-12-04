from django.contrib import admin
from .models import Chamado

@admin.register(Chamado)
class ChamadoAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'assunto', 'empresa', 'status', 'prioridade', 'tecnico_responsavel', 'data_abertura', 'data_encerramento')
    list_filter = ('status', 'prioridade', 'tecnico_responsavel', 'data_abertura')
    search_fields = ('assunto', 'descricao', 'empresa')
    list_editable = ('status', 'prioridade', 'tecnico_responsavel')
    ordering = ('-data_abertura',)