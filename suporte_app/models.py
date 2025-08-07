from django.db import models

# A classe Cliente é definida primeiro
class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20)

    def __str__(self):
        return self.nome

# Agora, a classe Dispositivo pode usar Cliente sem precisar de um import
class Dispositivo(models.Model):
    # Usamos o nome da classe 'Cliente' diretamente
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)  # Ex: 'Beyond One', 'Mini IR'
    mac_address = models.CharField(max_length=50, unique=True)
    localizacao = models.CharField(max_length=100)
    online = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nome} - {self.cliente.nome}"

# E a classe Protocolo pode usar Dispositivo sem precisar de um import
class Protocolo(models.Model):
    # Usamos o nome da classe 'Dispositivo' diretamente
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE)
    topico_mqtt = models.CharField(max_length=100)
    payload_exemplo = models.TextField()
    descricao = models.TextField(blank=True)

    def __str__(self):
        return f"Protocolo {self.topico_mqtt} ({self.dispositivo.nome})"

# Teste