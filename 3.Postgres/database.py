import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


CREATE_TABLE_USERS = """
CREATE TABLE IF NOT EXISTS users(
    id SERIAL PRIMARY KEY,
    username TEXT
);"""

CREATE_TABLE_MOVIE = """
CREATE TABLE IF NOT EXISTS movies(
    id SERIAL PRIMARY KEY,
    title TEXT,
    release REAL
);"""

CREATE_TABLE_WATCHED = """
CREATE TABLE IF NOT EXISTS watched_movie(
    id SERIAL PRIMARY KEY,
    id_user INTEGER,
    id_movie INTEGER,
    FOREIGN KEY (id_user) REFERENCES users(id),
    FOREIGN KEY (id_movie) REFERENCES movies(id)
);"""

CREATE_INDEX_MOVIE = """CREATE INDEX idx_movie_time ON movies(release);"""

##FUNCIONES IMPORTANTES

FDX_ADD_USERS = """INSERT INTO users( username) values (%s);"""
FDX_ADD_MOVIE = """INSERT INTO movies( title, release) values (%s,%s);"""
FDX_GET_MOVIES = """SELECT * FROM movies;"""
FDX_GET_UPCOMING = """SELECT * FROM movies WHERE release > (%s);"""
FDX_WATCHED_MOVIE = """INSERT INTO watched_movie( id_user, id_movie) values (%s,%s);"""
FDX_BUSCA_TERMINO = """SELECT * FROM movies where title LiKE %s;"""

connection = psycopg2.connect(
                    host='localhost',
                    database = os.environ.get('USER_DB'),
                    user = os.environ.get('USER_NAME'),
                    password = os.environ.get('USER_PASS'),
                    port =  5432
)

with connection:
    with connection.cursor() as cursor:
        cursor.execute("SELECT  VERSION();")
        print(cursor.fetchall())
    
def crea_tablas():
    with connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(CREATE_TABLE_USERS)
                cursor.execute(CREATE_TABLE_MOVIE)
                cursor.execute(CREATE_TABLE_WATCHED)
            except Exception as error:
                raise error
        
def crea_indices():
    with connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(CREATE_INDEX_MOVIE)
            except Exception as error:
                raise error

def add_user(username):
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(FDX_ADD_USERS, (username,))
    except Exception as error:
        raise error 


def add_movie(title, release):
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(FDX_ADD_MOVIE, (title, release))
    except Exception as error:
        raise error
    

def get_movies():
    try:
        with connection:
            cursor = connection.cursor()
            cursor.execute(FDX_GET_MOVIES)
            return cursor.fetchall()
    except Exception as error:
        raise error
    
def get_movies_upcomin(fecha):
    try:
        with connection:
            cursor = connection.cursor()
            cursor.execute(FDX_GET_UPCOMING,(fecha,))
            return cursor.fetchall()
    except Exception as error:
        raise error
    

def buscar_id_movie(tabla, parametro):
    try:
        with connection:
            with connection.cursor() as cursor_i:
                cursor_i.execute(f"SELECT id from movies where title = %s;", (parametro,))
                return cursor_i.fetchone()
    except Exception as error:
        raise error
    
def buscar_id_users(tabla, parametro):
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT id from users where username = %s;", (parametro,))
                return cursor.fetchone()
    except Exception as error:
        raise error
    
def marca_visto(username, movie):
    try:
        id_movie = buscar_id_movie('movies', movie)
        id_usu = buscar_id_users('users',username)
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(FDX_WATCHED_MOVIE,( id_usu[0], id_movie[0]))
    except Exception as error:
        raise error
    

def busca_por_termino(v_pelicula):
    try:
        with connection:
            cursor = connection.cursor()
            cursor.execute(FDX_BUSCA_TERMINO, (f"%{v_pelicula}%",))
            return cursor.fetchall()
    except Exception as error:
        raise error