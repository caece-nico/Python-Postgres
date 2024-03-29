# Introduccion a Python y Sqlite

1. [Intro al proyecto](#1.-intro-al-proyecto)
2. [Que es SQL?](#2.-que-es-sql?)
3. [Cómo usar Sqlite3?](#3.-como-usar-sqlite3?)
    * [Conexiones en DB](#Conexiones-en-db)
    * [Transacciones en BD](#transacciones-en-bd)
    * [Cursores](#cursores)
    * [Where](#where)
    * [DROP TABLE](#drop-table)
    * [UPADTE](#update)
    * [Delete](#delete)
4. [SQL Injection](#4.-sql-injection)
5. [Objetos BD](#5.-objetos-bd)
    * [Claves primarias](#claves-primarias)
    * [ID auto-incremental](#id-auto-incremental)
    * [JOINS](#joins)
    * [Order BY y Limit](#order-by-y-limit)
    * [Like - WildCards](#like-wildcards)
## 1. Intro al proyecto

```
Vamos a crear una app sencilla que interactua con el usuario para que pueda ingresar valores en una base de datos hasta que decida salir.
```

## 2. Que es SQL?

Se usa para intereactuar con Sistemas de bases de datos relacionales.

```sql
SELECT first_name 
FROM users;
```

```sql
INSERT INTO users (first_name, last_name) VALUES('nicolas','apellido');
```

### Que es Sqlite?

Es un sistema más flexible de base de datos útil para hacer pruebas antes de pasar a usar otros motores mas robustos.

## 3. Como usar sqlite3?

El módulo Sqlite ya viene incorporado en Python3 asique no hay que instalar nada.

Para trabajar con bases de datos los mas importante es.

1. Importar el modulo.
2. Crear la conexión al archivo.
3. Cerrar la conexion.


```python
import sqlite3

connection = sqlite3.connect("data.db")
connecton.execute("CREATE TABLE ventas (id integer, agente integer)";
connection.close()
```

## Conexiones en DB

No existe un limite de cuantas conexiones se pueden abrir pero si existe un limite de cuantas conexiones puede soportar una BD.

En el caso de sqlite nos conectamos a un archivo no hay un motor, pero en postgres es distinto.

## Transacciones en BD 

Se pueden ejecutar muchas querys en una transacción pero para que la transaccion finalice de forma correcta todas las querys deben finalizar con exito.

El concepto de transacción es importante porque nos asegura que todo lo que queremos que ocurra uceda de forma correcta y no de forma parcial.

```
commit -> lo usamos para confirmat los cambios.
rollback -> lo usamos para revertir lo que no fué confirmado.
```

_Cómo hacemos un commit?_

Hay dos formas.

+ La forma manual.

```python
def create_table():
    connection.execute("INSERT INTO alumnos values (1, 'Nicolas')")
    connectin.commit()
```

+ La forma automatica usando un _ContextManager_

```python
def create_table():
    with connection:
        connection.execute("INSERT INTO alumnos values (1, 'Nicolas')")
```

## Cursores

```
Es una estructura de datos que permite cargar los resultados de a uno por vez.
```

__sqlite cursores_ Son un poco distintos, en lugar de tener los resultados uno a uno nos devuelve todo junto pero hay formas de manipularlo.__

```python
connection = sqlite3.connect('mi_base.db')
cursor = connection.cursor()

cursor.execute("SELECT * FROM users;")

for row in cursor:
    print(row)

connection.close()
```

```python
connection = sqlite3.connect('mi_base.db')
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

cursor.execute("SELECT * FROM users;")

for row in cursor:
    print(row)

connection.close()
```


Cuando recibimos un cursor con tuplas pordemos decirle al motor quenos revuelve un diccionario.

**IMPORTANTE** A diferencia de otros motores de BD _sqlite_ usa cursores tambien para hacer _inserts_ aunque esta transacción no devuelva nada que podamos iterar.

```python
connection = sqlite3.connect('mi_bd.db')
cursor = connection.cursor()

cursor.execute("INSERT INTO users VALUES (1,'nicolas');")
cursor.execute(f"INSERT INTO users VALUES (1,'{variable}');")
cursor.commit()

connection.close()
```

## Where

```
Lo usamos para hacer filtros. Se escribe desde del FROM
Los operadores son :
```

```python
import sqlte3

connection = sqlite3.connect('mi_db.db')
cursor = connection.cursor()

cursor.execute("SELECT * FROM users WHERE fecha == (?)" , 
                (fecha, ) # Agregamos una "," extra porque es un solo campo.
                )

## Otra forma mas peligrosa - Code injection.

cursor.execute(f"SELECT * FROM users where fecha = '{fecha}'")
```

|operador|descripcion|
|--------|-----------|
|<|lower than (strict)|
|>|greater than (strict)|
|<=|lower equal than|
|>=|greater equal than|
|==|equal|
|!=|Not equal|


## Drop Table


Borramos toda una tabla


```python
connection.execute("DROP TABLE users;")
connection.commit()
```

## Update

```
Lo usamos para modificar un valor dentro de la base de datos.
```

```python
connection = sqlite.connect('mi_db.db')

connection.execute("UPDATE users SET nombre = ? WHERE id = ?", (v_id, v_nombre,))
connection.commit()

```

## Delete

```
Lo usamos para elimiar uno o varios registros de una tabla.
```

```python
connection = sqlite3.connect("mi_base.db")

connection.execute("DELETE FROM users WHERE id = ? and fecha = ?", (v_id, v_fecha))

connection.commit()

connection.close()
```

## 4. SQL Injection

```
Ocurre cuando se ingresa una sentencia malisiosa por parámetro.
Por Ejemplo un DROP TABLE users; 
```

_EJEMPLO EN PYTHON_

```python
v_id = "''; DROP TABLE users;'
cursor.execute(f"SELECT * FROM users where id = {v_id};")
```
Este codigo se ejecutaria de la siguiente manera:

SELECT * FROM users WHERE id = '' ; DROP TABLE users;

al no encontrar nada en la primer query pasa automaticamente a la segunda porque tiene el ";"

_¿Cómo solucionamos esto?_

```python
#USANDO ?
v_id = 1
GET_USER = "SELECT * FROM users WHERE id = ?;"
cursor.execute(GET_USER, (v_id,))
```

## 5. Objetos BD

## Claves Primarias

```
Es una propiedad de cada tabla que permite identificar de forma unívoca cada registro.
Es usado para mapear un registro de una tabla con otra tabla.
```

**TABLA USAARIO** 

|ID|NOMBRE|DIRECCION|
|--|------|---------|
|1|NICOLAS L.|XXXX51|
|1|SILVINA L.|YYYY62|

**TABLA COMPRAS**

|id|id_usaurio|monto|
|--|-----------|----|
|101|1|19.87|
|102|1|23.45|


En este ejemplo vemos uqe hay una relacion donde _usuario_(id) es clave primaria y _compras_(id_usuario) es la foranea

```sql
create table users(
    id INTEGER PRIMARY KEY,
    nombre TEXT,
    dicreccion TEXT);

create table compras(
    id INTEGER PRIMARY KEY,
    id_usuario INTEGER,
    monto REAL,
    FOREIGN KEY(id_usuario) REFERENCES usuario(id)
);
```

## ID Auto-Incremental

EN lugar de ir a buscar el max id en cada tabla **ESTO PUEDE TRAER PROBLEMAS** podemos user una propiedad para generar el siguiente _ID_. El veneficio de esto es evitar la concurrencia.

Todas las tablas en _sqlite_ tienen algo llamado **rowid**
 Estos valores se pueden reutilizar , solo aquellos que en algún momento fueron eliminados.

 ```sql
 create table xx (
    col xx1 INTEGER PRIMARY KEY autoincrement,
 )
 ```


 ## JOINS

 ```
 Lo usamos para trear resultados de dos tablas.
 ```

 ```sql
 select user.id, user.name, movie.title
 from user
 join movie
 on user.id = movie.user_id
 ```

 ## Order BY y Limit

 ```
Se usa para ordenar resultados por una columna o varias. Copcionalmente se puede usar DESC/ASC, por defecto usa ASC.
```

```sql
select id, nombre
from user
where id DESC, username ASC;
```

```
LIMIT se usa al final de la uery para limitar el numero de resultados que queremos ver. Generalmente se usa con ORDER BY para otener los n primeros registros en base a cierta condición.
```


```sql
SELECT *
FROM user
LIMIT 
```

## Like Wildcards

```
Se puede usar LIKE de dos formas:
% para cual numero de caracteres
_ para un caracter

Ej. 'Do%'

Doyle
Do

EJ. %Do - todo lo que termine con Do

Ej. 'Do__s' Match todo lo que empieza con Do y termina con s.
```


```python
MI_QUERY_LIKE = """select * form user where username like ?;"""

connection.execute(MI_QUERY_LIKE, (param, ))
```

## Indices

```
Nos ayudan a optimizar las consultas. Organizan las claves como un arbol que se recorre y va partiendo por los valores de las PK. Se llaman B-Tree.
Hay que tener en cuenta que a veces los inserts se pueden hacer un poco mas lentos por la re-organizacin del indice y el indice es una tabla que ocupa espacio.
```

```sql
CREATE INDEX IDX_MOVIE_RELEASE ON movies(release);
```

_IMPORTANTE_ La columnas pk tienen un index asociado por defecto.