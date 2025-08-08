from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import ProtocoloForm
from .models import Protocolo, AtualizacaoProtocolo
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required

@login_required
def gerar_protocolo(request):
    """
    View para exibir o formulário de criação de protocolo e o formset de atualizações.
    """
    AtualizacaoProtocoloFormset = inlineformset_factory(
        Protocolo,
        AtualizacaoProtocolo,
        fields=('texto',),
        extra=1,
        can_delete=False
    )
    
    if request.method == 'POST':
        form = ProtocoloForm(request.POST)
        formset = AtualizacaoProtocoloFormset(request.POST)
        
        if form.is_valid() and formset.is_valid():
            protocolo = form.save(commit=False)
            protocolo.autor = request.user
            protocolo.save()
            
            instances = formset.save(commit=False)
            for instance in instances:
                instance.protocolo = protocolo
                instance.autor = request.user
                instance.save()
            
            return redirect('protocolo_detalhe', pk=protocolo.id)
    else:
        form = ProtocoloForm()
        formset = AtualizacaoProtocoloFormset()
    
    context = {
        'form': form,
        'formset': formset
    }
    return render(request, 'suporte_app/gerar_protocolo.html', context)

@login_required
def protocolo_detalhe(request, pk):
    """
    View para exibir os detalhes de um protocolo, incluindo o seu ID.
    """
    protocolo = get_object_or_404(Protocolo, pk=pk)
    context = {
        'protocolo': protocolo
    }
    return render(request, 'suporte_app/protocolo_detalhe.html', context)
