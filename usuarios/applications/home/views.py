import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView




class FechaMixin(object):
    """ Clase de prueba """
    def get_context_data(self, **kwargs):
        context = super(FechaMixin, self).get_context_data(**kwargs)
        context['fecha'] = datetime.datetime.now()
        return (context)


class HomePage(LoginRequiredMixin,TemplateView):
    """ Vista Home Login """
    # LoginRequiredMixin para que solo vean la vista usuarios logeados 
    template_name = "home/index.html"
    login_url = reverse_lazy("users_app:login-user") # Direccion de redireccion para usuarios no logueados 

class TemplatePruebaMixin(FechaMixin,TemplateView):
    """ Clase que hereda de Fechamixin para prueba template y enviar datos por contextdata """
    template_name = "home/mixin.html"
