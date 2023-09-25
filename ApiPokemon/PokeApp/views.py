from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Usuario

import requests


@login_required #Requiere que este logueado
def pokemon_info(request, id): 
    if request.user.is_authenticated: #se verifica que el usuario este autentificado
        api_url = f"https://pokeapi.co/api/v2/pokemon/{id}/"

        try:
            response = requests.get(api_url) #se realiza la solicitud a la api

            if response.status_code == 200:
                info = response.json() #se convierte la respues en un diccionario

                #Obtiene las habilidades
                abilities = [ability['ability']['name'] for ability in info['abilities']]

                #Obtiene la imagen
                image = info['sprites']['front_default']

                #Renderiza una plantilla con los datos del pokemon
                return render(request, 'pokemon.html', {'info': info, 'abilities': abilities, 'image': image}) 

            else: #si la solicitud falla muestra un mensaje en la plantilla error
                return render(request, 'error.html', {'mensaje': 'No se pudo mostrar el Pokémon'})
        
        except requests.exceptions.RequestException as e: #si la solucitud a la api falla muestra un mensaje
            return render(request, 'error.html', {'mensaje': 'Hubo un error en la solicitud'})
    else: #si el usuario no esta logueado lo redirige al login
        return redirect('iniciar') 


def pokemon_lista(request):
    # url de la api para extraer los pokemones
    api_url = "https://pokeapi.co/api/v2/pokemon/"

    try:
        #solicitud a la api
        response = requests.get(api_url)

        # Verifica la solicitud 
        if response.status_code == 200:
            #convierte la respuesta en diccionario
            data = response.json()
            
            #extrae la lista de nombres de Pokémon
            pokemon_lista = [pokemon['name'] for pokemon in data['results']]

            #plantilla con los nombres de los pokemones
            return render(request, 'pokemon_lista.html', {'pokemon_lista': pokemon_lista})
        else:
            #si la solicitud no fue exitosa muestra un mensaje de error
            return render(request, 'error.html', {'msj_error': 'No se pudo obtener la lista de Pokémon'})
    except requests.exceptions.RequestException as e:
        #si hay un error en la solicitud muestra un mensaje de error
        return render(request, 'error.html', {'msj_error': 'Error en la solicitud a la API'})
    

def registar_usuario(request):
    if request.method == 'POST':
        # Verifica si la solicitud es de tipo POST

        # Obtiene los datos de los campos del formulario
        email = request.POST['email']
        contrasenia = request.POST['contrasenia']

        # Crea el usuario utilizando tu modelo personalizado CustomUser
        user = Usuario.objects.crear_usuario(email=email, password=contrasenia)

        # Redirige a la página de registro con un mensaje de usuario creado
        return render(request, 'registrar.html', {'creada': 'Usuario creado'})

    # Si la solicitud no es POST, redirige a la página de registro
    return render(request, 'registrar.html')


def iniciar(request):

    # Verifica si la solicitud es de tipo POST
    if request.method == 'POST':

        # Obtiene los datos de los campos del formulario
        email = request.POST['email']
        contrasenia = request.POST['contrasenia']

        # Autentifica el usuario comparando las credenciales
        user = authenticate(request, email=email, password=contrasenia)

        if user is not None:
            # Si se autentifica el usuario, se inicia sesión y se redirige a la plantilla pokemon_lista
            login(request, user)

            return redirect('pokemon_lista')

        else: # Si no se autentifica el usuario, se redireje al login con un mensaje de error
            error = 'Correo o contraseña incorrecta'
            return render(request, 'login.html', {'msj_error': error})
    # Si la solicitud no es de tipo POST se redirige al login
    return render(request, 'login.html')


def cerrar(request):
    #Cierra la sesion del usuario
    logout(request)

    return redirect('pokemon_lista') #Redirige a la plantilla pokemon_lista