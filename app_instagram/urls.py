from django.views import View
from django.urls import path, include
from .views import RegisterView,login_user,register_user,HomeView,ConfigView,logout_user,ConfigDatosView,get_user_data


urlpatterns = [
    
    path('signup/', RegisterView.as_view(), name='signup'),
    path('home/', HomeView.as_view(), name='home'),
    path('login/', login_user, name='login_user'),
    path('register/', register_user, name='register'),
    path('config/', ConfigView.as_view(), name='config'),
    path('configDatos/', ConfigDatosView.as_view(), name='configDatos'),
    path('logout/', logout_user, name='logout'),
    path('get_user_data/', get_user_data, name='get_user_data'),
]