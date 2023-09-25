from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class UsuarioManager(BaseUserManager):
    def crear_usuario(self, email, password=None):
        if not email: #Verifica que sea un correo
            raise ValueError('El Email es obligatorio.')
        email = self.normalize_email(email) #Se normaliza el correo en minusculas
        usuario = self.model(email=email) #se cre una instancia con el correo
        usuario.set_password(password) #Guarda la contraseña segura con hash
        usuario.save(using=self._db) #se guarda el usuario en la base de datos
        return usuario 

class Usuario(AbstractBaseUser):
    email = models.EmailField(unique=True) #campo de correo
    is_active = models.BooleanField(default=True) #campo para activacion de la cuenta

    objects = UsuarioManager() #se asigna el gestor de usuario

    USERNAME_FIELD = 'email' #se usa el correo como identificador para iniciar sesion

