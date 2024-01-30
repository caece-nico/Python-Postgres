import database
from dotenv import load_dotenv
import os
import psycopg2

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