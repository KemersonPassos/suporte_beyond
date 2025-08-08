from django.db import models
from django.contrib.auth.models import User

# Opções de status para o protocolo.
STATUS_CHOICES = (
    ('aberto', 'Aberto'),
    ('em_andamento', 'Em Andamento'),
    ('concluido', 'Concluído'),
)

class Cliente(models.Model):
    """
    Modelo para representar um cliente.
    """
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20)

    def __str__(self):
        return self.nome

class Dispositivo(models.Model):
    """
    Modelo para representar um dispositivo associado a um cliente.
    """
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    mac_address = models.CharField(max_length=50, unique=True)
    localizacao = models.CharField(max_length=100)
    online = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nome} - {self.cliente.nome}"

class Protocolo(models.Model):
    """
    Modelo principal para o registro de protocolos.
    """
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE)
    buic = models.CharField(max_length=100, blank=True, null=True) # Campo BUIC adicionado
    topico_mqtt = models.CharField(max_length=100, blank=True, null=True)
    payload_exemplo = models.TextField(blank=True, null=True)
    descricao = models.TextField(blank=True)
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='aberto'
    )
    # Adicionado o autor do protocolo
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Protocolo {self.id} ({self.dispositivo.nome})"

class AtualizacaoProtocolo(models.Model):
    """
    Novo modelo para a 'linha do tempo' de atualizações de um protocolo.
    """
    protocolo = models.ForeignKey(Protocolo, on_delete=models.CASCADE, related_name='atualizacoes')
    
    texto = models.TextField()
    data_atualizacao = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"Atualização em {self.protocolo.id} por {self.autor.username}"
