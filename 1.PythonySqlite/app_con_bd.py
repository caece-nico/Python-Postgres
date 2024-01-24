import sqlite3

directorio_bd = 'D:\\Proyectos\\Python-Postgres\\sqlite\\mi_bd\\'


connection = sqlite3.connect(directorio_bd+'base_prueba')

def create_table():
    connection.execute(
        "CREATE TABLE if not exists alumno  \
        (id integer, \
        nombre varchar(250)\
        )"
        )
def close_conection():
    connection.close()

create_table()
close_conection()