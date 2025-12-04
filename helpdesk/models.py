from django.db import models
from django.contrib.auth.models import User

STATUS_CHOICES = [
    ('NOVO', 'Novo'),
    ('ANDAMENTO', 'Em Andamento'),
    ('PENDENTE', 'Pendente'),
    ('FECHADO', 'Fechado'),
]

PRIORIDADE_CHOICES = [
    ('BAIXA', 'Baixa'),
    ('MEDIA', 'Média'),
    ('ALTA', 'Alta'),
    ('CRITICA', 'Crítica'),
]

class Chamado(models.Model):
    
    assunto = models.CharField(max_length=200, verbose_name="Assunto")
    descricao = models.TextField(verbose_name="Descrição Detalhada")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='NOVO',verbose_name="Status")
    prioridade = models.CharField(max_length=10, choices=PRIORIDADE_CHOICES, default='MEDIA',verbose_name="Prioridade")
    empresa = models.CharField(max_length=100, verbose_name="Empresa do Solicitante")
    data_abertura = models.DateTimeField(auto_now_add=True, verbose_name="Data de Abertura")
    data_encerramento = models.DateTimeField(null=True, blank=True, verbose_name="Data de Encerramento")
    usuario_abertura = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='chamados_abertos', verbose_name="Usuário de Abertura")
    tecnico_responsavel = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='chamados_atribuidos')
    
    class Meta:
        verbose_name = "Chamado"
        verbose_name_plural = "Chamados"
        ordering = ['data_abertura']

    def __str__(self):
        return f"Chamado #{self.pk} - {self.assunto}"

    def is_aberto(self):
        return self.status in ['NOVO', 'ANDAMENTO', 'PENDENTE']