from django.shortcuts import render, redirect, get_object_or_404
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
from django.contrib import messages
from .models import UsuarioInsta


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

class perfilView(View):
    def get(self, request):
        return render(request, 'perfil.html')

class buscarView(View):
    def get(self, request):
        username = request.GET.get('usuario')
        usuario = get_object_or_404(UsuarioInsta, usuario=username)
        return render(request, 'buscar.html', {'nombre_usuario': usuario.usuario, 'correo': usuario.correo})

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views import View
from .models import UsuarioInsta

@csrf_protect
def search_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            usuario = UsuarioInsta.objects.get(usuario=username)
            return JsonResponse({
                'status': 'success',
                'data': {
                    'nombre_usuario': usuario.usuario,
                    'nombre_personal': usuario.nombre,
                    'correo': usuario.correo
                }
            })
        except UsuarioInsta.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Usuario no encontrado'}, status=404)
    
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


@csrf_exempt
@login_required
def delete_account(request):
    if request.method == 'POST':
        try:
            user = request.user  # Usuario autenticado
            usuario_insta = UsuarioInsta.objects.get(correo=user.correo)  # Buscar en la base de datos
            usuario_insta.delete()  # Eliminar usuario de la base de datos
            logout(request)  # Cerrar sesión
            return JsonResponse({
                'status': 'success', 
                'message': 'Tu cuenta ha sido eliminada.', 
                'redirect_url': '/login/'  # Redirige al login después de eliminar
            })
        except UsuarioInsta.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Usuario no encontrado.'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Método no permitido.'}, status=405)


#VISTA PARA MODIFICAR EL NOMBRE DE USUARIO
@login_required
def modify_username(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_username = data.get('new_username', '').strip()

        # Validar que el nombre no esté vacío
        if not new_username:
            return JsonResponse({'status': 'error', 'message': 'El nombre de usuario no puede estar vacío.'}, status=400)

        # Verificar si el nombre ya existe
        if UsuarioInsta.objects.filter(usuario=new_username).exists():  # Cambié 'username' a 'usuario'
            return JsonResponse({'status': 'error', 'message': 'El nombre de usuario ya está en uso.'}, status=400)

        # Actualizar el nombre de usuario
        user = request.user
        user.usuario = new_username  # Cambié 'username' a 'usuario'
        user.save()

        return JsonResponse({'status': 'success', 'message': 'Nombre de usuario modificado con éxito.'})

    return JsonResponse({'status': 'error', 'message': 'Método no permitido.'}, status=405)

#VISTA PARA MODIFICAR NOMBRE PERSONAL
@login_required
def modify_personal_name(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_personal_name = data.get('new_personal_name', '').strip()

        # Validar que el nombre no esté vacío
        if not new_personal_name:
            return JsonResponse({'status': 'error', 'message': 'El nombre personal no puede estar vacío.'}, status=400)

        # Actualizar el nombre personal
        user = request.user
        user.nombre = new_personal_name  # Cambié al campo correcto (nombre personal)
        user.save()

        return JsonResponse({'status': 'success', 'message': 'Nombre personal modificado con éxito.'})

    return JsonResponse({'status': 'error', 'message': 'Método no permitido.'}, status=405)

#VISTA PARA MODIFICAR CONTRASEÑA
@login_required
def modify_password(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        current_password = data.get('current_password', '').strip()
        new_password = data.get('new_password', '').strip()
        confirm_password = data.get('confirm_password', '').strip()

        # Validar que los campos no estén vacíos
        if not current_password or not new_password or not confirm_password:
            return JsonResponse({'status': 'error', 'message': 'Todos los campos son obligatorios.'}, status=400)

        # Validar la contraseña actual
        user = request.user
        if not check_password(current_password, user.password):
            return JsonResponse({'status': 'error', 'message': 'La contraseña actual es incorrecta.'}, status=400)

        # Validar que las contraseñas nuevas coincidan
        if new_password != confirm_password:
            return JsonResponse({'status': 'error', 'message': 'Las contraseñas nuevas no coinciden.'}, status=400)

        # Cambiar la contraseña
        user.set_password(new_password)
        user.save()

        return JsonResponse({'status': 'success', 'message': 'Contraseña modificada con éxito.', 'redirect_url': '/'})

    return JsonResponse({'status': 'error', 'message': 'Método no permitido.'}, status=405)