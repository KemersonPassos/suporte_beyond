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
    nome = models.CharField(max_length=100, verbose_name="Nome")
    email = models.EmailField(unique=True, verbose_name="E-mail")
    telefone = models.CharField(max_length=20, verbose_name="Telefone")

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['nome']

    def __str__(self):
        return self.nome

class Dispositivo(models.Model):
    """
    Modelo para representar um dispositivo associado a um cliente.
    """
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name="Cliente")
    nome = models.CharField(max_length=100, verbose_name="Nome do Dispositivo")
    tipo = models.CharField(max_length=50, verbose_name="Tipo")
    mac_address = models.CharField(max_length=50, unique=True, verbose_name="Endereço MAC")
    localizacao = models.CharField(max_length=100, verbose_name="Localização")
    online = models.BooleanField(default=False, verbose_name="Online")

    class Meta:
        verbose_name = "Dispositivo"
        verbose_name_plural = "Dispositivos"
        ordering = ['cliente__nome', 'nome']

    def __str__(self):
        return f"{self.nome} - {self.cliente.nome}"

class Protocolo(models.Model):
    """
    Modelo principal para o registro de protocolos.
    """
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE, verbose_name="Dispositivo")
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name="Cliente",
                               help_text="Cliente para o qual o protocolo está sendo aberto",
                               null=True, blank=True)  # Temporariamente permitir nulo
    buic = models.CharField(max_length=100, blank=True, null=True, verbose_name="BUIC", 
                           help_text="Código BUIC do dispositivo")
    topico_mqtt = models.CharField(max_length=100, blank=True, null=True, verbose_name="Tópico MQTT")
    payload_exemplo = models.TextField(blank=True, null=True, verbose_name="Payload de Exemplo")
    descricao = models.TextField(verbose_name="Descrição do Problema", 
                                help_text="Descreva detalhadamente o problema reportado")
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='aberto',
        verbose_name="Status"
    )
    # Técnico/atendente que abriu o protocolo (usuário logado no Django)
    tecnico_responsavel = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                          verbose_name="Técnico Responsável")

    class Meta:
        verbose_name = "Protocolo"
        verbose_name_plural = "Protocolos"
        ordering = ['-id']  # Ordenar pelos mais recentes

    def __str__(self):
        return f"Protocolo #{self.id} - {self.cliente.nome} ({self.dispositivo.nome})"
    
    @property
    def numero_protocolo(self):
        """
        Retorna o número do protocolo formatado (ID em formato decimal)
        """
        return f"{self.id:06d}"  # Formata o ID com 6 dígitos: 000001, 000002, etc.

class AtualizacaoProtocolo(models.Model):
    """
    Modelo para a 'linha do tempo' de atualizações de um protocolo.
    """
    protocolo = models.ForeignKey(Protocolo, on_delete=models.CASCADE, related_name='atualizacoes',
                                 verbose_name="Protocolo")
    texto = models.TextField(verbose_name="Atualização", 
                            help_text="Descreva o que foi feito ou observado")
    data_atualizacao = models.DateTimeField(auto_now_add=True, verbose_name="Data da Atualização")
    tecnico = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               verbose_name="Técnico")
    
    class Meta:
        verbose_name = "Atualização do Protocolo"
        verbose_name_plural = "Atualizações do Protocolo"
        ordering = ['data_atualizacao']

    def __str__(self):
        return f"Atualização em #{self.protocolo.id} - {self.data_atualizacao.strftime('%d/%m/%Y %H:%M')}"