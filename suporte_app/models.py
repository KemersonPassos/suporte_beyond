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
    Adicionado o campo de status.
    """
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE)
    topico_mqtt = models.CharField(max_length=100)
    payload_exemplo = models.TextField()
    descricao = models.TextField(blank=True)
    
    # Campo de status com as opções definidas acima
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='aberto'
    )

    def __str__(self):
        return f"Protocolo {self.topico_mqtt} ({self.dispositivo.nome})"

class AtualizacaoProtocolo(models.Model):
    """
    Novo modelo para a 'linha do tempo' de atualizações de um protocolo.
    """
    protocolo = models.ForeignKey(Protocolo, on_delete=models.CASCADE, related_name='atualizacoes')
    
    # Campo para armazenar o texto da atualização
    texto = models.TextField()
    
    # Campo para registrar a data e hora da atualização
    data_atualizacao = models.DateTimeField(auto_now_add=True)
    
    # Campo para saber quem fez a alteração
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"Atualização em {self.protocolo.id} por {self.autor.username}"
