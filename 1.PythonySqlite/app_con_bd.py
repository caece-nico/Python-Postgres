from db_conection import create_table, close_connextion, add_entry, add_entry_code_injection, get_entry

def visualizar_tareas(cursor):
    #Cursor tiene un diccionario, no una Tupla
    for data in cursor:
        print(f" nombre = {data['descripcion']} ,fecha= {data['fecha']}\n")

def ingresar_tarea(con_code_injection):

    tarea = input('Ingre la tarea')
    horario = input('Ingrese un horario')

    if con_code_injection:
        add_entry(tarea,horario)
    else:
        add_entry_code_injection(tarea,horario)


print("Welcome")

texto = """Ingrese una de las siguientes opciones \n
        1) Ingresar una nueva tarea. \n
        2) Visualizar tareas anteriores. \n
        3) salir. 
        """

create_table()

opcion = input(texto) 
fecha='2023.01.25' #Fecha fija que e pasamos a a función de busqueda.
while opcion != "3":

    if opcion == "1":
        ingresar_tarea(con_code_injection = False)

    elif opcion == "2":
        visualizar_tareas(get_entry(fecha))

    else:
        print('Opcion incorrecta')

    opcion = input(texto) 

close_connextion()



