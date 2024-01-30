import database
from dotenv import load_dotenv
import os
import psycopg2



try:
    load_dotenv()
    connection = psycopg2.connect(database=os.getenv('POSTGRES_DB'), 
                              user=os.getenv('POSTGRES_USER'), 
                              password=os.getenv('POSTGRES_PASSWORD'))
except Exception as error:
    print(f"Error en crea conexion {error}")


def crea_tablas():
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(database.CREATE_OPTIONS)
                cursor.execute(database.CREATE_POLLS)
                cursor.execute(database.CREATE_VOTES)
    except Exception as error:
        return f"Error en crea tablas " + str(error)
    

try:
    crea_tablas()
except Exception as error:
    print(error)