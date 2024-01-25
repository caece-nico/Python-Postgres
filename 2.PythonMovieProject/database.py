import sqlite3
import datetime


CREATE_MOVIES_TABLE = """CREATE TABLE IF NOT EXISTS movies
(title TEXT,
release_timestamp REAL);
"""

CREATE_WATCHLIST_TABLE = """CREATE TABLE IF NOT EXISTS watched (
watcher_name TEXT,
title TEXT);
"""

INSERT_MOVIES = "INSERT INTO movies (title, release_timestamp) VALUES (?, ?);"
SELECT_ALL_MOVIES = "SELECT * FROM movies;"
SELECT_UPCOMING_MOVIES = "SELECT * FROM movies WHERE release_timestamp > ?;"
SELECT_WATCHED_MOVIES = "SELECT * FROM watched WHERE watcher_name = ?;"
INSERT_WATCHED_MOVIE = "INSERT INTO watched (watcher_name, title) VALUES (?,?);"
SET_MOVIE_WATCHES = "UPDATE movies SET watched = 1 where title = ?;"
DELETE_MOVIE = "DELETE FROM movies WHERE title = ?;"

connection = sqlite3.connect("D:\\Proyectos\\Python-Postgres\\2.PythonMovieProject\\bd_movies.db")


def create_tables():
    with connection:
        connection.execute(CREATE_MOVIES_TABLE)
        connection.execute(CREATE_WATCHLIST_TABLE)

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

def watch_movie(username, title):
    try:
        with connection:
            connection.execute(DELETE_MOVIE, (title,))
            connection.execute(INSERT_WATCHED_MOVIE, (username,title))
    except Exception as e:
        print('La pelicula no existe')

def get_movie_watch(username):
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_WATCHED_MOVIES, (username,))
        return cursor.fetchall()