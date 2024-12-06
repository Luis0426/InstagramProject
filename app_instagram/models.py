from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.core.validators import FileExtensionValidator
import os
import uuid
from bson import ObjectId

def user_profile_image_path(instance, filename):
    # Se asegura de que el nombre del archivo sea único
    extension = filename.split('.')[-1]
    unique_filename = f"{uuid.uuid4().hex}.{extension}"
    return os.path.join(f'perfil/{instance.usuario}/', unique_filename)


class UsuarioManager(BaseUserManager):
    def create_user(self, correo, password=None, **extra_fields):
        if not correo:
            raise ValueError('El correo es obligatorio')
        correo = self.normalize_email(correo)
        user = self.model(correo=correo, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(correo, password, **extra_fields)

class UsuarioInsta(AbstractBaseUser):
    correo = models.EmailField(unique=True)
    usuario = models.CharField(max_length=255, unique=True)
    nombre = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    imagen_perfil = models.ImageField(
        upload_to=user_profile_image_path,
        null=True,
        blank=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])]
    )
    objects = UsuarioManager()
    
    
    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['usuario', 'nombre']

    def __str__(self):
        return self.correo

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class Publicacion(models.Model):
    usuario = models.ForeignKey(UsuarioInsta, on_delete=models.CASCADE, related_name='publicaciones')
    imagen = models.ImageField(upload_to='publicaciones/', validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])])
    descripcion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Publicación de {self.usuario.usuario} en {self.fecha_creacion}'
    

class Relacion(models.Model):
    seguidor = models.ForeignKey(UsuarioInsta, on_delete=models.CASCADE, related_name='siguiendo')
    seguido = models.ForeignKey(UsuarioInsta, on_delete=models.CASCADE, related_name='seguidores')
    fecha_seguimiento = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.seguidor.usuario} sigue a {self.seguido.usuario}'



class Like(models.Model):
    usuario = models.ForeignKey(UsuarioInsta, on_delete=models.CASCADE)
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE, related_name='likes')
    fecha_like = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.usuario.usuario} le dio like a {self.publicacion.id}'



class Comentario(models.Model):
    usuario = models.ForeignKey(UsuarioInsta, on_delete=models.CASCADE)
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE, related_name='comentarios')
    texto = models.TextField()
    fecha_comentario = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comentario de {self.usuario.usuario} en {self.publicacion.id}'

def generate_object_id():
    return str(ObjectId())

class Post(models.Model):
    id = models.CharField(max_length=24, primary_key=True, default=generate_object_id)
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    imagen = models.ImageField(upload_to='posts/')
    usuario = models.ForeignKey('UsuarioInsta', on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def str(self):
        return self.titulo