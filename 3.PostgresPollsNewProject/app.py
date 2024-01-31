import database
from dotenv import load_dotenv
import os
import psycopg2


MENU_PROMPT = """-- Menu --

1) Create new polls
2) List open polls
3) Vote on a poll
4) Show poll votes
5) Select a random winner from a poll option
6) Exit

Enter your choice: """

NEW_OPTION_PROMPT = "Enter new option text (or leave empty to stop adding options): "


def prompt_create_pool(psycopg2, connection):
    poll_title = input("Enter poll title: ")
    poll_owner = input("Enter poll owner: ")

    options = []

    new_option = input(NEW_OPTION_PROMPT)

    while new_option != "":
        options.append(new_option)
        new_option = input(NEW_OPTION_PROMPT)

    try:
        database.create_poll(psycopg2, connection, poll_title, poll_owner, options)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def list_open_poll(psycopg2, connection):
    try:
        polls = database.get_polls(psycopg2, connection)

        for _id, title, owner in polls:
            print(f"{_id}: {title} (created by {owner})")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def prompt_vote_poll(psycopg2, connection):
    poll_id = input('Enter the poll you wanna vote on: ')

    poll_options = database.get_poll_details(psycopg2, connection, poll_id)
    _print_poll_options(poll_options)

    option_id = input('Enter the option you would like to vote for: ')
    username = input('Enter the username you wanna use to vote as: ')

    database.add_poll_vote(psycopg2, connection, option_id, username)


def _print_poll_options(poll_with_options):
    for option in poll_with_options:
        print(f"{option[3]} : {option[4]}")

def show_poll_votes(psycopg2, connection):
    poll_id = int(input("Enter the poll you wanna see the votes for: "))

    try:
        poll_and_votes = database.get_poll_and_vote_results(psycopg2, connection, poll_id)
    except ZeroDivisionError as error:
        print(f"No hay votos aun {error}")
    else:
        for _id, option_text, count, percentage in poll_and_votes:
            print(f"{option_text} got {count} votes ({percentage:.2f}% of total)")

def randomiza_poll_winner(psycopg2, connection):
    poll_id = int(input("Enter poll you´d like to pick a winner for: "))
    poll_options = database.get_poll_details(psycopg2, connection, poll_id)

    option_id = int(input("Enter which is the winning option, we'll pick random winner from votes: "))
    winner = database.get_random_poll_vote(psycopg2, connection, option_id)
    print(f"The randomly selected winner is {winner[0]}")


MI_MENU =  {
    1:prompt_create_pool,
    2:list_open_poll
}

try:
    load_dotenv()
    connection = psycopg2.connect(database=os.getenv('POSTGRES_DB'), 
                              user=os.getenv('POSTGRES_USER'), 
                              password=os.getenv('POSTGRES_PASSWORD'),
                              host='localhost',
                              port=5432)
except (Exception, psycopg2.DatabaseError) as error:
    print(f"Error en crea conexion {error}")

try:
    database.crea_tablas(psycopg2, connection)
except Exception as error:
    print(error)

user_input = int(input(MENU_PROMPT))


while user_input:
    try:
        MI_MENU[user_input](psycopg2, connection)
    except KeyError:
        print('Ingresaste una opción incorrecta')
    
    user_input = input(MENU_PROMPT)
    