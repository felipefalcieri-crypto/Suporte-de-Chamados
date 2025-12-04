from django import forms
from django.contrib.auth.models import User, Group
from .models import Chamado 

class ChamadoAtualizacaoForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            grupo_tecnicos = Group.objects.get(name='Técnicos')
            tecnicos_queryset = User.objects.filter(groups=grupo_tecnicos).order_by('username')
            self.fields['tecnico_responsavel'].queryset = tecnicos_queryset
        except Group.DoesNotExist:
            pass 

    class Meta:
        model = Chamado
        fields = ['status', 'tecnico_responsavel']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'tecnico_responsavel': forms.Select(attrs={'class': 'form-select'}),
        }

class ChamadoForm(forms.ModelForm):
    class Meta:
        model = Chamado
        fields = ['assunto', 'descricao', 'empresa', 'prioridade','tecnico_responsavel','usuario_abertura']
        widgets = {
            'assunto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Resumo do problema'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Detalhe o máximo possível...'}),
            'empresa': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Digite o nome da empresa'}), 
            'prioridade': forms.Select(attrs={'class': 'form-select'}),
            'tecnico_responsavel': forms.Select(attrs={'class': 'form-select'}),
            'usuario_abertura': forms.Select(attrs={'class': 'form-select'}),
        }