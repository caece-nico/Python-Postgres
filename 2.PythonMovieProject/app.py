from datetime import datetime
import database

def prompt_add_movie():
    try:
        title = input('Movie title: ')
        release_date = input('Release date (dd-mm-yyyy): ')
        parsed_date = datetime.strptime(release_date,"%d-%m-%Y")
        timestamp = parsed_date.timestamp()
        error = database.add_movie(title, timestamp)
        print(error)
    except Exception as e:
        print(e)


def print_upcoming_movies(tipo, movies):
    print(f"-----{tipo} MOVIES----")
    for movie in movies:
        movie_date = datetime.fromtimestamp(movie[1])
        human_date = movie_date.strftime("%b %d %Y")
        print(f"Pelicula = { movie[0]} fecha = {human_date}")
    print("\n\n")

def prompt_watched_movie():
    try:
        user_input_title = input('Ingrese la pelicula: ')
        database.watch_movie(user_input_title)
    except Exception as e:
        print(e)

menu = """Please select one of the following options:
1) Add new movie.
2) View upcoming movies.
3) View all movies.
4) Watch a movie.
5) View watched movies.
6) Exit.

Your Selection: """

welcome = 'Bienvenido al sistema de peliculas'
database.create_tables()

print(welcome)

user_input = input(menu)

while user_input != '6':

    if user_input == '1':
        prompt_add_movie()
    elif user_input == '2':
        print_upcoming_movies('Upcoming', database.get_movies(True))
    elif user_input == '3':
        print_upcoming_movies('All', database.get_movies(False))
    elif user_input == '4':
        prompt_watched_movie()
    elif user_input == '5':
        pass
    else:
        print('Se eligió una opción incorrecta')

    user_input = input(menu)