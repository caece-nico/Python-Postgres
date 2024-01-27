import database
from datetime import datetime

def promt_add_user():
    try:
        user_name_input = input('Ingrese el nombre de usuario: ')
        database.add_user(user_name_input)
    except Exception as error:
        print(error)
try:
    valor = database.crea_tablas()
    print('Error en la llamda: ' + str(valor))
except Exception as e:
    print(str(e))

def promt_add_movie():
    try:
        title_input = input('Ingrese el nombre de la pelicula: ')
        release_date = input('ingrese la fecha de la pelicula (dd-mm-yyyy): ')
        fecha_timestamp = datetime.strptime(release_date,'%d-%m-%Y')
        fecha_timestamp = fecha_timestamp.timestamp()
        database.add_movie(title_input, fecha_timestamp)
    except Exception as error:
        print(error)

def view_all_movies():
    peliculas = database.get_movies()

    for film in peliculas:
        try:
            fecha = datetime.fromtimestamp(film[2])
            fecha = datetime.strftime(fecha, '%d-%m-%Y')
            print(f"Titulo: {film[1]} Fecha: {fecha}")
        except Exception as error:
            print(error)

def view_upcoming_movies():
    try:
        fecha_hoy = datetime.today()
        fecha_hoy = datetime.timestamp(fecha_hoy)
        peliculas = database.get_movies_upcomin(fecha_hoy)
        for film in peliculas:
            fecha = datetime.fromtimestamp(film[2])
            fecha = datetime.strftime(fecha, '%d-%m-%Y')
            print(f"La pelicula {film[1]} se estrenará el dia {fecha}")
    except Exception as error:
        print(error)

def prompt_view_movie():
    try:
        usuario = input('Ingrese el usuario: ')
        movie = input('Ingrese la pelicula que vio: ')
        database.marca_visto(usuario, movie)
    except Exception as error:
        print(error)
        
menu = """Opciones disponibles:
1) Agregar usuario.
2) Agregar Pelicula.
3) Mostrar lista de peliculas.
4) Mostrar lista de estrenos.
5) Marcar pelicula vista.
6) Salir.

La opcion ingresada es: 
"""
print(menu)
user_input = input('Ingrese una opcion: ')

while user_input != "6":

    if user_input == "1":
        promt_add_user()
    elif user_input == "2":
        promt_add_movie()
    elif user_input == "3":
        view_all_movies()
    elif user_input == "4":
        view_upcoming_movies()
    elif user_input == "5":
        prompt_view_movie()
    else:
        print('La opcion ingresa no es correcta')

    user_input = input('Ingrese una opcion: ')
