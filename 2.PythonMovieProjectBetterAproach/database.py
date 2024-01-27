import sqlite3


CREATE_TABLE_USERS = """
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    username TEXT
);"""

CREATE_TABLE_MOVIE = """
CREATE TABLE IF NOT EXISTS movies(
    id NUMBER PRIMARY KEY,
    title TEXT,
    release REAL
);"""

CREATE_TABLE_WATCHED = """
CREATE TABLE IF NOT EXISTS watched_movie(
    id INTEGER PRIMARY KEY,
    id_user INTEGER,
    id_movie INTEGER,
    FOREIGN KEY (id_user) REFERENCES users(id),
    FOREIGN KEY (id_movie) REFERENCES movies(id)
);"""


##FUNCIONES IMPORTANTES

FDX_ADD_USERS = """INSERT INTO users(id, username) values (?,?);"""
FDX_ADD_MOVIE = """INSERT INTO movies(id, title, release) values (?,?,?);"""
FDX_GET_MOVIES = """SELECT * FROM movies;"""
FDX_GET_UPCOMING = """SELECT * FROM movies WHERE release > (?);"""
FDX_WATCHED_MOVIE = """INSERT INTO watched_movie(id, id_user, id_movie) values (?,?,?);"""


connection = sqlite3.connect("D:\\Proyectos\\Python-Postgres\\2.PythonMovieProjectBetterAproach\\db_movies.db")

def crea_tablas():
    with connection:
        try:
            connection.execute(CREATE_TABLE_USERS)
            connection.execute(CREATE_TABLE_MOVIE)
            connection.execute(CREATE_TABLE_WATCHED)
        except Exception as e:
            return sqlite3.DatabaseError 
        
def get_max_id(tabla):
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT MAX(id) from {tabla};")
        return cursor.fetchone()
    except Exception as error:
        raise error

def add_user(username):
    try:
        with connection:
            max_id = get_max_id('users')
            max_ids = 0
            if max_id[0] is None:
                max_ids += 1
                connection.execute(FDX_ADD_USERS, (max_ids,username))
            else:
                max_ids = int(max_id[0]) + 1
                connection.execute(FDX_ADD_USERS, (max_ids,username))
    except Exception as error:
        raise error 


def add_movie(title, release):
    try:
        with connection:
            max_id = get_max_id('movies')
            max_ids = 0
            if max_id[0] is None:
                max_ids = 1
            else:
                max_ids = int(max_id[0]) + 1
            connection.execute(FDX_ADD_MOVIE, (max_ids, title, release))
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
            cursor = connection.cursor()
            cursor.execute(f"SELECT id from movies where title = ?;", (parametro,))
            return cursor.fetchall()
    except Exception as error:
        raise error
    
def buscar_id_users(tabla, parametro):
    try:
        with connection:
            cursor = connection.cursor()
            cursor.execute(f"SELECT id from users where username = ?;", (parametro,))
            return cursor.fetchone()
    except Exception as error:
        raise error
    
def marca_visto(username, movie):
    try:
        with connection:
            id_movie = buscar_id_movie('movies', movie)
            id_usu = buscar_id_users('users',username)
            id_movie_val = id_movie[0]
            id_usu_val = id_usu[0]
            print(id_movie_val[0])
            print(id_usu_val[0])
            connection.execute(FDX_WATCHED_MOVIE,(2, id_usu_val[0], id_movie_val[0]))
    except Exception as error:
        raise error