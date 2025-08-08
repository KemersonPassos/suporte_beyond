from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Cliente, Dispositivo, Protocolo, AtualizacaoProtocolo

# A classe Inline permite que você edite o histórico de atualizações dentro do Protocolo.
class AtualizacaoProtocoloInline(admin.TabularInline):
    model = AtualizacaoProtocolo
    extra = 1
    
    # O campo 'autor' será somente leitura, já que será preenchido automaticamente
    readonly_fields = ('autor',)
    fields = ('texto', 'autor')
    
    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Protocolo)
class ProtocoloAdmin(admin.ModelAdmin):
    list_display = ('id', 'autor', 'dispositivo', 'buic', 'descricao_curta', 'status')
    list_filter = ('status', 'autor')
    search_fields = ('id', 'dispositivo__nome', 'buic')
    inlines = [AtualizacaoProtocoloInline]
    
    # Campos que aparecerão na página de adição/alteração
    fields = ('dispositivo', 'buic', 'descricao', 'status')
    readonly_fields = ('id', 'autor')

    def save_model(self, request, obj, form, change):
        if not obj.autor_id:
            obj.autor = request.user
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if not instance.autor_id:
                instance.autor = request.user
            instance.save()
        formset.save_m2m()
        
    def descricao_curta(self, obj):
        # Exibe a descrição com um limite de 50 caracteres e reticências
        if obj.descricao and len(obj.descricao) > 50:
            return f"{obj.descricao[:50]}..."
        return obj.descricao
    descricao_curta.short_description = "Descrição do Problema"

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone')
    search_fields = ('nome', 'email')

@admin.register(Dispositivo)
class DispositivoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cliente', 'online', 'tipo', 'mac_address')
    list_filter = ('online', 'tipo')
    search_fields = ('nome', 'cliente__nome', 'mac_address')
