from psycopg2.extras import execute_values #importantes

CREATE_POLLS = """CREATE TABLE IF NOT EXISTS polls 
(id SERIAL PRIMARY KEY, title TEXT, owner_username TEXT);"""
CREATE_OPTIONS = """CREATE TABLE IF NOT EXISTS options(
id SERIAL PRIMARY KEY, option_text TEXT, poll_id INTEGER, FOREIGN KEY(poll_id) REFERENCES polls(id));"""
CREATE_VOTES = """CREATE TABLE IF NOT EXISTS votes
(username TEXT, option_id INTEGER, FOREIGN KEY(option_id) REFERENCES options(id));"""

SELECT_ALL_POLLS = """SELECT * FROM polls; """
SELECT_POLL_WITH_OPTIONS = """SELECT poll.id, options.option_text FROM polls INNER JOIN options 
ON polls.id = options.poll_id
WHERE polls.id = %s;"""
SELECT_LATEST_POLLS = """SELECT * FROM polls INNER JOIN options
ON polls.id = options.polls_id WHERE polls.id = (SELECT id FROM polls 
ORDER BY id DESC LIMIT 1);"""
SELECT_RANDOM_POLL_VOTE = """SELECT * FROM votes WHERE option_id = %s
ORDER BY RANDOM() LIMIT 1;"""
SELECT_POLL_VOTE_DETAILS = """SELECT options.id, options.option_text, COUNT(votes.option_id),
COUNT(votes.option_id) / SUM(COUNT(votes.option_id)) OVER() * 100
FROM options
LEFT JOIN votes ON options.id = votes.option_id
WHERE options.poll_id = %s
GROUP BY options.id;
"""

INSERT_OPTION = "INSERT INTO options (option_text, poll_id) VALUES (%s, %s);"
INSERT_VOTE = "INSERT INTO votes (username, option_id) VALUES (%s, %s);"


def crea_tablas(psycopg2, connection):
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(CREATE_POLLS)
                cursor.execute(CREATE_OPTIONS)
                cursor.execute(CREATE_VOTES)
    except (Exception, psycopg2.DataError) as error:
        raise  error  
    

def get_polls(psycopg2, connection):
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(SELECT_ALL_POLLS)
                return cursor.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        raise error
    
def get_latest_poll(psycopg2, connection):
   try:
       with connection:
           with connection.cursor() as cursor:
               cursor.execute(SELECT_LATEST_POLLS)
               return cursor.fetchall()
   except (Exception, psycopg2.DatabaseError) as error:
       raise error


def get_poll_details(connection, poll_id):
    pass


def get_poll_and_vote_results(psycopg2,connection, poll_id):
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(SELECT_POLL_VOTE_DETAILS, (poll_id,))
                return cursor.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        raise error

def get_random_poll_vote(psycopg2, connection, option_id):
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(SELECT_RANDOM_POLL_VOTE, (option_id,))
                return cursor.fetchone()
    except (Exception, psycopg2.DatabaseError) as error:
        raise error



def create_poll(psycopg2, connection, poll_title, poll_owner, options):
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO polls(title, owner_username) values (%s, %s) returning id",(poll_title, poll_owner))

                poll_id = cursor.fetchone()[0]

                opciones_lista = [(opcion_val, poll_id) for opcion_val in options]

                for v_options in opciones_lista:
                    cursor.execute(INSERT_OPTION, v_options)

                #execute_values(cursor, INSERT_OPTION, opciones_lista)

    except (Exception, psycopg2.DatabaseError) as error:
        raise error

def add_poll_vote(connection, user_name, option_id):
    pass


