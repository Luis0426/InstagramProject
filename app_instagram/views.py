from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import View, ListView, CreateView, DeleteView
from django.core import serializers
from .models import UsuarioInsta
#Importaciones para el inicio de sesion
from django.contrib.auth import logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password,make_password
from .models import UsuarioInsta
from django.contrib.auth import login, authenticate
import json



class RegisterView(View):
    def get(self, request):
        return render(request, 'signup.html')
    
class ConfigView(View):
    def get(self, request):
        return render(request, 'config.html')

class ConfigDatosView(View):
    def get(self, request):
        return render(request, 'configDatos.html')

class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')

@csrf_exempt
def logout_user(request):
    logout(request)
    return JsonResponse({'status': 'success', 'message': 'Sesión cerrada correctamente', 'redirect_url': '/'})

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parsear datos JSON enviados desde el frontend
            correo = data.get('email')
            password = data.get('password')

            # Autenticar al usuario con `authenticate`
            user = authenticate(request, username=correo, password=password)

            if user is not None:
                # Iniciar sesión con `login`
                login(request, user)
                return JsonResponse({'status': 'success', 'message': 'Inicio de sesión exitoso'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Credenciales incorrectas'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Método no permitido'})
    

@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        try:
            # Parsear los datos JSON enviados desde el frontend
            data = json.loads(request.body)
            correo = data.get('email')
            password = data.get('password')
            usuario = data.get('username')
            nombre = data.get('name')

            # Verificar si el correo o usuario ya existe
            if UsuarioInsta.objects.filter(correo=correo).exists():
                return JsonResponse({'status': 'error', 'message': 'El correo ya está registrado'})
            if UsuarioInsta.objects.filter(usuario=usuario).exists():
                return JsonResponse({'status': 'error', 'message': 'El nombre de usuario ya está en uso'})

            # Registrar el usuario
            nuevo_usuario = UsuarioInsta(
                correo=correo,
                password=make_password(password),  # Hashear la contraseña antes de guardarla (opcional)
                usuario=usuario,
                nombre=nombre
            )
            nuevo_usuario.save()

            return JsonResponse({'status': 'success', 'message': 'Usuario registrado exitosamente'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Método no permitido'})

#VISTA PARA CONSULTAR DATOS DE USUARIO
@login_required
def get_user_data(request):
    try:
        # Obtén el usuario autenticado
        user = request.user  # Este es el usuario logueado basado en UsuarioInsta
        
        # Encuentra el usuario correspondiente en el modelo UsuarioInsta
        usuario_insta = UsuarioInsta.objects.get(correo=user.correo)
        
        # Prepara los datos para la respuesta
        data = {
            'nombre_usuario': usuario_insta.usuario,  # El nombre de usuario personalizado
            'nombre_personal': usuario_insta.nombre,  # El nombre real
            'correo': usuario_insta.correo,           # El correo electrónico
            'contraseña': '********'                 # Ocultar la contraseña por seguridad
        }
        return JsonResponse({'status': 'success', 'data': data})
    
    except UsuarioInsta.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Usuario no encontrado'}, status=404)
