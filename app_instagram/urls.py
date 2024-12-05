from . import views
from django.urls import path, include
from .views import RegisterView,login_user,register_user,HomeView,ConfigView,logout_user,ConfigDatosView,get_user_data, delete_account, perfilView, search_user, buscarView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('signup/', RegisterView.as_view(), name='signup'),
    path('home/', HomeView.as_view(), name='home'),
    path('perfil/', perfilView.as_view(), name='perfil'),
    path('buscar/', buscarView.as_view(), name='bucar'),
    path('search_user/', search_user, name='search_user'),
    path('login/', login_user, name='login_user'),
    path('register/', register_user, name='register'),
    path('config/', ConfigView.as_view(), name='config'),
    path('configDatos/', ConfigDatosView.as_view(), name='configDatos'),
    path('logout/', logout_user, name='logout'),
    path('get_user_data/', get_user_data, name='get_user_data'),
    path('delete_account/', delete_account, name='delete_account'),
    path('modify-username/', views.modify_username, name='modify_username'),
    path('modify-personal-name/', views.modify_personal_name, name='modify_personal_name'),
    path('modify-password/', views.modify_password, name='modify_password'),

]

# Servir archivos MEDIA en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)