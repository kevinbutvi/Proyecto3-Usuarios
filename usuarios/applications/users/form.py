from django import forms
from .models import User
from django.contrib.auth import authenticate

class UserRegisterForm(forms.ModelForm):
    """Form definition for MODELNAME."""

    password1 = forms.CharField(
        label = "Contraseña",
        required = True,
        widget = forms.PasswordInput(
            attrs = {
                "placeholder": "contraseña"
                }
            )
        )
    
    password2 = forms.CharField(
        label = "Contraseña",
        required = True,
        widget = forms.PasswordInput(
            attrs = {
                "placeholder": "Repetir contraseña"
            }
        )
    )
    
    
    class Meta:
        """Meta definition for MODELNAMEform."""

        model = User
        fields = (
            "username",
            "email",
            "nombres",
            "apellidos",
            "genero"
            )

    def clean_password2(self):
        if len(self.cleaned_data["password1"]) < 7:
            self.add_error("password1", "La contraseña debe ser mayor a 7 caracteres")
        elif self.cleaned_data["password1"] != self.cleaned_data["password2"]:
            self.add_error("password2", "Las contraseñas no coinciden")



class LoginForm(forms.Form):
    username = forms.CharField(
        label = "Username",
        required = True,
        widget = forms.TextInput(
            attrs = {
                "placeholder": "usuario"
                }
            )
        )

    password = forms.CharField(
        label = "Contraseña",
        required = True,
        widget = forms.PasswordInput(
            attrs = {
                "placeholder": "contraseña"
                }
            )
        )
    
    def clean(self):
        """ Validacion que usuario exista en DB """
        cleaned_data = super(LoginForm, self).clean()
        username = self.cleaned_data["username"]
        password = self.cleaned_data["password"]
        
        if not authenticate(username = username, password = password):
            raise forms.ValidationError("Los datos de usuario no son correctos ")
        
        return (self.cleaned_data)


class UpdatePasswordForm(forms.Form):
    password1 = forms.CharField(
        label = "Contraseña",
        required = True,
        widget = forms.PasswordInput(
            attrs = {
                "placeholder": "contraseña actual"
                }
            )
        )

    password2 = forms.CharField(
        label = "Contraseña",
        required = True,
        widget = forms.PasswordInput(
            attrs = {
                "placeholder": "contraseña NUEVA"
                }
            )
        )


class VerificationForm(forms.Form):
    codregistro = forms.CharField(required=True, max_length=50)
    
    def __init__(self, pk, *args, **kwargs):
        self.id_user = pk
        super(VerificationForm, self).__init__(*args, **kwargs)
    
    def clean_codregistro(self):
        """ Validacion del que el codigo de seguridad sea correcto """
        codigo = self.cleaned_data["codregistro"]
        
        if len(codigo) == 6:
            #Verificamos si el codigo y el id del usuario son validos
            activo = User.objects.cod_validation(
                self.id_user, #Recupero el ID enviado por URL desde la vista, para esto hubo que sobreescribir las funciones '__init__' y declara nueva funcion 'get_form_kwargs' en las views
                codigo
            )
            if not activo:
                raise forms.ValidationError("El codigo de seguridad es incorrecto")
        else:
            raise forms.ValidationError("El codigo de seguridad es incorrecto")
