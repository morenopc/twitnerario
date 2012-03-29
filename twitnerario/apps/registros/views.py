# -*- coding: UTF8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, RequestContext
from registros.models import Registros
from registros.forms import RegistrosForm
from django.http import HttpResponse
from core.tweet import less30minutes

#
# Registro
#
#@login_required
def registro(request):
    rs=Registros.objects.none()
    form=RegistrosForm(request.POST or None)
    if form.is_valid():
        t=str(request.POST['twitter'] or None)
        l=int(request.POST['linha'] or None)
        p=int(request.POST['ponto'] or None)
        h=int(request.POST['horas'] or None)
        m=int(request.POST['minutos'] or None)
        
        # remove registros duplicados
        rs=Registros.objects.filter(twitter=t,ponto=p,linha=l,horas=h,minutos=m)
        if rs.count() > 0:
            rs.delete()
            
        #t=less30minutes(h,m)
        #h=t[0]
        #m=t[1]
        
        #info=horarios(str(request.POST['ponto']),str(request.POST['linha']))
        form.save()
        #return render_to_response('registros/sucesso.html', context_instance=RequestContext(request,{'info':info}))
        
        return render_to_response('registros/sucesso.html', context_instance=RequestContext(request,{'twitter':t,'m':m,'h':h}))
    
    return render_to_response('registros/registro.html', context_instance=RequestContext(request,{'form':form}))
    
