from django.contrib import admin
from .models import Cliente, Dispositivo, Protocolo, AtualizacaoProtocolo

# A classe Inline permite que você edite o histórico de atualizações dentro do Protocolo.
class AtualizacaoProtocoloInline(admin.TabularInline):
    model = AtualizacaoProtocolo
    extra = 1  # Quantidade de formulários extras para adicionar
    
    # O campo 'autor' será somente leitura, já que será preenchido automaticamente
    readonly_fields = ('autor',)

@admin.register(Protocolo)
class ProtocoloAdmin(admin.ModelAdmin):
    list_display = ('dispositivo', 'topico_mqtt', 'status')
    list_filter = ('status',)
    search_fields = ('topico_mqtt', 'dispositivo__nome')
    inlines = [AtualizacaoProtocoloInline]

    # Este método é chamado para salvar o formset do inline.
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            # Preenche o campo 'autor' com o usuário logado antes de salvar
            if not instance.autor_id:
                instance.autor = request.user
            instance.save()
        formset.save_m2m()

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone')
    search_fields = ('nome', 'email')

@admin.register(Dispositivo)
class DispositivoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cliente', 'online', 'tipo', 'mac_address')
    list_filter = ('online', 'tipo')
    search_fields = ('nome', 'cliente__nome', 'mac_address')
