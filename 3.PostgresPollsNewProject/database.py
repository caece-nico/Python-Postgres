CREATE_POLLS = """CREATE TABLE IF NOT EXISTS polls 
(id SERIAL PRIMARY KEY, title TEXT, owner_username TEXT);"""
CREATE_OPTIONS = """CREATE TABLE IF NOT EXISTS options(
id SERIAL PRIMARY KEY, option_text TEXT, poll_id INTEGER, FOREIGN KEY(poll_id) REFERENCES polls(id));"""
CREATE_VOTES = """CREATE TABLE IF NOT EXISTS votes
(username TEXT, option_id INTEGER, FOREIGN KEY(option_id) REFERENCES options(id));"""

SELECT_ALL_POLLS = """SELECT * FROM polls; """
SELECT_POLL_WITH_OPTIONS = """SELECT poll.id, options.option_text 
FROM polls 
INNER JOIN options 
ON polls.id = options.poll_id
WHERE polls.id = %s;"""






def crea_tablas(psycopg2, connection):
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(CREATE_POLLS)
                cursor.execute(CREATE_OPTIONS)
                cursor.execute(CREATE_VOTES)
    except (Exception, psycopg2.DataError) as error:
        raise  error  
    

def get_polls(connection):
    try:
        with connection:
            with connection.cursor as cursor:
                cursor.execute(SELECT_ALL_POLLS)
                return cursor.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        raise error