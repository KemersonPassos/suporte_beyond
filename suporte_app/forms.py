from django import forms
from .models import Protocolo

class ProtocoloForm(forms.ModelForm):
    """
    Formulário para a criação de um novo protocolo.
    """
    class Meta:
        model = Protocolo
        fields = ['cliente', 'dispositivo', 'descricao', 'buic', 'topico_mqtt', 'payload_exemplo', 'status']
        labels = {
            'cliente': 'Cliente',
            'dispositivo': 'Dispositivo',
            'descricao': 'Descrição do Problema',
            'buic': 'BUIC',
            'topico_mqtt': 'Tópico MQTT',
            'payload_exemplo': 'Payload de Exemplo',
            'status': 'Status',
        }
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'dispositivo': forms.Select(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'buic': forms.TextInput(attrs={'class': 'form-control'}),
            'topico_mqtt': forms.TextInput(attrs={'class': 'form-control'}),
            'payload_exemplo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }