from django.db import models

from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager, models.Manager):
    """ Manager del modelo USER """
    def _create_user(self, username, email, password, is_staff, is_superuser, is_active, **extra_fields):
        """ Manager Base para creacion de Usuario """
        user = self.model(
            username = username,
            email = email,
            is_staff = is_staff,
            is_superuser = is_superuser,
            is_active = is_active,
            **extra_fields
        )
        user.set_password(password)
        user.save(using = self.db)
        return (user)
    
    def create_user(self, username, email, password = None, **extra_fields):
        """ Manager para creacion de usuario comun """
        return self._create_user(username, email, password, False, False,  False, **extra_fields)
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        """ Manager para creacion de usuario ADMIN """
        return self._create_user(username, email, password, True, True, True, **extra_fields  )
    
    def cod_validation(self, id_usuario, codigo_registro):
        """ Manager para asignacion de codigo validador a usuario """
        if self.filter(id = id_usuario, codregistro = codigo_registro):
            return (True)
        else:
            return (False)