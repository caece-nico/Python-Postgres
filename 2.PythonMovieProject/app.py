from datetime import datetime

menu = """Please select one of the following options:
1) Add new movie.
2) View upcoming movies.
3) View all movies.
4) Watch a movie.
5) View watched movies.
6) Exit.

Your Selection: """

welcome = 'Bienvenido al sistema de peliculas'

print(welcome)

user_input = input(menu)

while user_input != '6':

    if user_input == '1':
        pass
    elif user_input == '2':
        pass
    elif user_input == '3':
        pass
    elif user_input == '4':
        pass
    elif user_input == '5':
        pass
    else:
        print('Se eligió una opción incorrecta')

    user_input = input(menu)