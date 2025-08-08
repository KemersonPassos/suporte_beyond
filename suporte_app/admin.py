from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Cliente, Dispositivo, Protocolo, AtualizacaoProtocolo

# A classe Inline permite que você edite o histórico de atualizações dentro do Protocolo.
class AtualizacaoProtocoloInline(admin.TabularInline):
    model = AtualizacaoProtocolo
    extra = 1
    
    # O campo 'tecnico' será somente leitura, já que será preenchido automaticamente
    readonly_fields = ('tecnico', 'data_atualizacao')
    fields = ('texto', 'tecnico')  # Removemos data_atualizacao dos fields editáveis
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Se o protocolo já existe (editando)
            return ('tecnico', 'data_atualizacao')
        return ('tecnico',)  # Se é um novo protocolo, só o tecnico é readonly

@admin.register(Protocolo)
class ProtocoloAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'tecnico_responsavel', 'dispositivo', 'buic', 'descricao_curta', 'status', 'data_criacao')
    list_filter = ('status', 'tecnico_responsavel', 'cliente', 'dispositivo__cliente')
    search_fields = ('id', 'cliente__nome', 'dispositivo__nome', 'buic', 'descricao')
    list_per_page = 25
    ordering = ('-id',)  # Ordenar pelos protocolos mais recentes primeiro
    
    inlines = [AtualizacaoProtocoloInline]
    
    readonly_fields = ('id', 'tecnico_responsavel', 'data_criacao')
    
    # Remove os fieldsets fixos - vamos usar get_fieldsets dinâmico

    def get_fieldsets(self, request, obj=None):
        """
        Retorna fieldsets diferentes para criação e edição
        """
        if obj:  # Editando protocolo existente
            return (
                ('Informações do Protocolo', {
                    'fields': ('id', 'cliente', 'tecnico_responsavel', 'dispositivo', 'buic'),
                    'description': 'O ID e Técnico Responsável são preenchidos automaticamente.'
                }),
                ('Detalhes do Problema', {
                    'fields': ('descricao', 'status'),
                    'classes': ('wide',),
                }),
                ('Informações MQTT (Opcional)', {
                    'fields': ('topico_mqtt', 'payload_exemplo'),
                    'classes': ('collapse',),
                }),
            )
        else:  # Criando novo protocolo
            return (
                ('Informações do Protocolo', {
                    'fields': ('cliente', 'tecnico_responsavel', 'dispositivo', 'buic'),
                    'description': 'O Técnico Responsável é preenchido automaticamente.'
                }),
                ('Detalhes do Problema', {
                    'fields': ('descricao', 'status'),
                    'classes': ('wide',),
                }),
                ('Informações MQTT (Opcional)', {
                    'fields': ('topico_mqtt', 'payload_exemplo'),
                    'classes': ('collapse',),
                }),
            )

    def get_readonly_fields(self, request, obj=None):
        """
        Torna o ID e tecnico_responsavel readonly sempre
        """
        if obj:  # Se está editando um protocolo existente
            return ('id', 'tecnico_responsavel', 'data_criacao')
        return ('tecnico_responsavel',)  # Quando criando, só o técnico é readonly

    def save_model(self, request, obj, form, change):
        """
        Automaticamente define o técnico responsável como o usuário logado
        """
        if not obj.tecnico_responsavel_id:
            obj.tecnico_responsavel = request.user
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        """
        Automaticamente define o técnico das atualizações como o usuário logado
        """
        instances = formset.save(commit=False)
        for instance in instances:
            if not instance.tecnico_id:
                instance.tecnico = request.user
            instance.save()
        formset.save_m2m()
        
    def descricao_curta(self, obj):
        """
        Exibe a descrição com um limite de 50 caracteres e reticências
        """
        if obj.descricao and len(obj.descricao) > 50:
            return f"{obj.descricao[:50]}..."
        return obj.descricao or "Sem descrição"
    descricao_curta.short_description = "Descrição do Problema"

    def data_criacao(self, obj):
        """
        Exibe a data de criação do protocolo (baseada no primeiro registro de atualização)
        """
        primeira_atualizacao = obj.atualizacoes.first()
        if primeira_atualizacao:
            return primeira_atualizacao.data_atualizacao.strftime("%d/%m/%Y %H:%M")
        return "N/A"
    data_criacao.short_description = "Data de Criação"

    def get_queryset(self, request):
        """
        Otimiza as consultas incluindo relacionamentos
        """
        queryset = super().get_queryset(request)
        return queryset.select_related('dispositivo', 'cliente', 'tecnico_responsavel', 'dispositivo__cliente').prefetch_related('atualizacoes')

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'quantidade_dispositivos')
    search_fields = ('nome', 'email')
    list_per_page = 50
    
    def quantidade_dispositivos(self, obj):
        """
        Mostra a quantidade de dispositivos do cliente
        """
        return obj.dispositivo_set.count()
    quantidade_dispositivos.short_description = "Qtd. Dispositivos"

@admin.register(Dispositivo)
class DispositivoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cliente', 'status_online', 'tipo', 'mac_address', 'localizacao')
    list_filter = ('online', 'tipo', 'cliente')
    search_fields = ('nome', 'cliente__nome', 'mac_address')
    list_per_page = 50
    
    def status_online(self, obj):
        """
        Exibe o status online com cores
        """
        if obj.online:
            return mark_safe('<span style="color: green; font-weight: bold;">● Online</span>')
        else:
            return mark_safe('<span style="color: red; font-weight: bold;">● Offline</span>')
    status_online.short_description = "Status"

# Personalização do site admin
admin.site.site_header = "Sistema de Suporte Beyond"
admin.site.site_title = "Suporte Beyond"
admin.site.index_title = "Painel de Administração"