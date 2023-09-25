# En tu archivo urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
   
    #url para ver la informacion del pokemon
    path('pokemon/<int:id>/', views.pokemon_info, name='pokemon_info'),
    #url para la ver la lista de pokemones
    path('', views.pokemon_lista, name='pokemon_lista'),
    #url para ver registrarse
    path('crear_usuario/', views.registar_usuario, name='registrar'),
    #url para loguearse
    path('iniciar/', views.iniciar, name='iniciar'),
    #url para login de django (cuando el usuario no esta autentificado y entre a un pokemon)
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    #url para cerrar sesion
    path('cerrar/', views.cerrar, name='cerrar'),
]
