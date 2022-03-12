import imp
from multiprocessing import AuthenticationError

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail

from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, View
from django.views.generic.edit import FormView

from .form import (LoginForm, UpdatePasswordForm, UserRegisterForm, VerificationForm)
from .functions import code_generator
from .models import User




class UserRegisterView(FormView):
    """ Vista para registro de Usuario, requiere validacion por codigo via mail """
    template_name = "users/register.html"
    form_class = UserRegisterForm
    success_url = "/"
    
    def form_valid(self, form):
        # Se genera codigo de verificacion
        codigo = code_generator()
        # Se guarda la instancia de USUARIO en dicha variable para poder manipular el ID y poder enviarlo por url para hacer la validacion del codigo de seguridad
        usuario = User.objects.create_user(
            form.cleaned_data["username"],
            form.cleaned_data["email"],
            form.cleaned_data["password1"],
            nombres = form.cleaned_data["nombres"],
            apellidos = form.cleaned_data["apellidos"],
            genero = form.cleaned_data["genero"],
            codregistro = codigo,
            )
        # Enviar el codigo al email del usuario se usa 'send_email'
        asunto = "Confirmacion de usuario"
        mensaje = "Codigo de Verificacion: " + codigo
        email_remitente = "developertest.kevin@gmail.com"
        #
        send_mail(asunto, mensaje, email_remitente, [form.cleaned_data["email"],])
        
        # Redirigir a pantalla de validacion
        return(HttpResponseRedirect(reverse(
            "users_app:user-verification",
            kwargs={"pk": usuario.id} # ACA se hace referencia a la instancia creada arriba y se accede al id para poder linkear el usuario con el codigo de seguridad y poder activarlo
            )))


class LoginUser(FormView):
    """ Vista de autenticacion para el login """
    template_name = "users/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("home_app:panel") 
    
    def form_valid(self, form):
        """ Autenticacion del Login """
        user = authenticate(
            username = form.cleaned_data["username"],
            password = form.cleaned_data["password"]
            )
        login(self.request,user)
        return super(LoginUser, self).form_valid(form)


class LogoutView(View):
    """ Vista para logout al hacer clic en 'cerrar sesion'. SE INTERSEPTA LA FUNC. GET """
    def get(self, request, *args, **kwargs):
        logout(request)
        return(HttpResponseRedirect(reverse("users_app:login-user")))


class UpdatePasswordView(LoginRequiredMixin, FormView):
    """ Clase de cambio de password de usuario """
    # LoginRequiredMixin Garantiza que solo vean la vista usuarios logueados """
    template_name = "users/update.html"
    form_class = UpdatePasswordForm
    login_url = reverse_lazy("users_app:login-user")# Redireccion de usuario no esta registrado 
    success_url = reverse_lazy("users_app:login-user") # Redireccion OK
    
    def form_valid(self, form):
        usuario = self.request.user # Instancia del usuario
        user = authenticate(
            username = usuario.username,
            password = form.cleaned_data["password1"]
            )
        if user:
            """ Si user es TRUE, (Pudo autenticar arriba), entonces se cambia la pass """
            new_password = form.cleaned_data["password2"]
            usuario.set_password(new_password)
            usuario.save()
        logout(self.request)
        return super(UpdatePasswordView, self).form_valid(form)


class CodVerificationView(FormView):
    """ Vista de verificacion de usuario"""
    template_name = "users/verification.html"
    form_class = VerificationForm
    success_url = reverse_lazy("users_app:login-user")
    
    def get_form_kwargs(self):
        """ Funcion para obtener Kwargs y poder utilizarlos como validacion en el FORM """
        kwargs = super(CodVerificationView, self).get_form_kwargs()
        kwargs.update({
            "pk": self.kwargs["pk"]
        })
        return (kwargs)

    def form_valid(self, form):
        User.objects.filter(
            id = self.kwargs["pk"]
        ).update(is_active = True)
        return super(CodVerificationView, self).form_valid(form)
