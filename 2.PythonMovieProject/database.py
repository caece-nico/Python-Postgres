import sqlite3
import datetime


CREATE_MOVIES_TABLE = """CREATE TABLE IF NOT EXISTS movies
(title TEXT,
release_timestamp REAL,
watched INTEGER);
"""

INSERT_MOVIES = "INSERT INTO movie (title, release_timestamp, watched) VALUES (?, ?, 0);"
SELECT_ALL_MOVIES = "SELECT * FROM movies;"
SELECT_UPCOMING_MOVIES = "SELECT * FROM movies WHERE release_timestamp > ?;"
SELECT_WATCHED_MOVIES = "SELECT * FROM movies WHERE watched = 1;"
SET_MOVIE_WATCHES = "UPDATE movies SET watched = 1 where title = ?;"

connection = sqlite3.connect('..//sqlite//bd_movies//bd_movie.db')


def create_tables():
    with connection:
        connection.execute(CREATE_MOVIES_TABLE)

def add_movie(title, release_timestamp):
    try:
        with connection:
            connection.execute(INSERT_MOVIES, (title, release_timestamp))
    except Exception as e:
        return ('Error de insert' + str(e))

def get_movies(upcoming=False):
    with connection:
        cursor = connection.cursor()
        if upcoming:
            today_timestamp = datetime.datetime.today().timestamp()
            cursor.execute(SELECT_UPCOMING_MOVIES, (today_timestamp,))
        else:
            cursor.execute(SELECT_ALL_MOVIES)
        
        return cursor.fetchall()

def watch_movie(title):
    try:
        with connection:
            connection.execute(SET_MOVIE_WATCHES, (title,))
    except Exception as e:
        print('La pelicula no existe')

def get_movie_watch():
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_WATCHED_MOVIES)
        return cursor.fetchall()