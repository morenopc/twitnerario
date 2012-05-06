# -*- coding: UTF8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, RequestContext
from registros.models import Registros
from registros.forms import RegistrosForm
from django.http import HttpResponse

#
# Registro
#
def registro(request):
    rs=Registros.objects.none()
    form=RegistrosForm(request.POST or None)
    if form.is_valid():
        t=request.POST['twitter'] or None
        l=request.POST['linha'] or None
        p=request.POST['ponto'] or None
        h=int(request.POST['horas'] or None)
        m=int(request.POST['minutos'] or None)
        
        # se duplicado então remove o anterior
        rs=Registros.objects.filter(twitter=t,ponto=p,linha=l,horas=h,minutos=m)
        if rs.count() > 0:
            rs.delete()
          
        form.save()
        return render_to_response('registros/sucesso.html', context_instance=RequestContext(request,{'twitter':t,'m':m,'h':h}))
    
    return render_to_response('registros/registro.html', context_instance=RequestContext(request,{'form':form}))
    
