import sqlite3

actividades = []

connection = sqlite3.connect(f"../sqlite/mi_bd/base_prueba")
connection.row_factory = sqlite3.Row # COn esto devolvemos un diccionario en lugar de una Tupla.

def create_table():
    with connection:
        connection.execute("CREATE TABLE IF NOT EXISTS actividades \
                           (descripcion TEXT, \
                           fecha TEXT);"
                           )
        
def add_entry(description, date):
    connection.execute(f"INSERT INTO actividades values \
                       ('{description}' ,\
                        '{date}');")
    connection.commit()


def add_entry_code_injection(description, date):
    print("Entro por injection")
    connection.execute("INSERT INTO actividades values (?,?);" ,\
                       (description, date)
                    )
    connection.commit()

def get_entry(fecha):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM actividades WHERE fecha = (?) ;", \
                   (fecha,))

    return cursor.fetchall()


def close_connextion():
    connection.close()       