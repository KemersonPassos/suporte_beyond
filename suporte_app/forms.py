from django import forms
from .models import Protocolo

class ProtocoloForm(forms.ModelForm):
    """
    Formulário para a criação de um novo protocolo.
    """
    class Meta:
        model = Protocolo
        fields = ['dispositivo', 'descricao', 'buic', 'topico_mqtt', 'payload_exemplo']
        labels = {
            'dispositivo': 'Dispositivo',
            'descricao': 'Descri\u00e7\u00e3o do Problema',
            'buic': 'BUIC',
            'topico_mqtt': 'T\u00f3pico MQTT',
            'payload_exemplo': 'Payload de Exemplo',
        }
        widgets = {
            'dispositivo': forms.Select(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control'}),
            'buic': forms.TextInput(attrs={'class': 'form-control'}),
            'topico_mqtt': forms.TextInput(attrs={'class': 'form-control'}),
            'payload_exemplo': forms.Textarea(attrs={'class': 'form-control'}),
        }
