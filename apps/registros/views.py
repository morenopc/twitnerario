# -*- coding: UTF8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, RequestContext
from registros.forms import RegistrosForm
from django.http import HttpResponse

#
# Registro
#
#@login_required
def registro(request):
    
    form=RegistrosForm(request.POST or None)
    if form.is_valid():
        t=str(request.POST['twitter'] or None)
        h=int(request.POST['horas'] or None)
        m=int(request.POST['minutos'] or None)
        
        if m>=30:
            m-=30
        else:
            m+=30
            h-=1
        
        #info=horarios(str(request.POST['ponto']),str(request.POST['linha']))
        form.save()
        #return render_to_response('registros/sucesso.html', context_instance=RequestContext(request,{'info':info}))
        
        return render_to_response('registros/sucesso.html', context_instance=RequestContext(request,{'twitter':t,'m':m,'h':h}))
    
    return render_to_response('registros/registro.html', context_instance=RequestContext(request,{'form':form}))
    
