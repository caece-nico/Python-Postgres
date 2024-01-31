# Introducción a Postgres


1. [SQLite VS Postgres](#1.-sqlite-vs-postgres)
2. [Instalacion de Postgres](#2.-instalacion-de-postgres)
3. [Interactual con Python](#3.-interactuar-con-python)
4. [Datos sensibles y variables de entorno](#4.-datos-sensibles-y-variables-de-entorno)
5. [Introducción a Postgres](#5.-introduccion-a-postgres)
    [Tipo de dato Serial](#tipo-de-dato-serial)
      * [Subtipo de dato Secuencia](#subtipo-de-dato-secuencia)
    [Como pasar valores en Python/postgres](#Como-pasar-valores-en-pythonpostgres?)
6. [ACID](#acid)
7. [Funcionalidad de Postgres - SQL](#funcionalidad-de-postgres-sql)
  + [Returning](#7.1-returning)
  + [Psycopg2 - execute_value](#7.2-psycopg2-execute_value)


## 1. SQLite vs Postgres

* Size.

SQLite es un archivo de un tamaño pequeño mientras que Postgers puede alcanzar tamaños de Tb.
Postgres Acepta distintas conexiones, etc.

* Velocidad.

Solo una conexion puede leer/escribir en el archivo de SQLite. NO permite la paralelizacion.
Postgres no tiene esta limitación por lo que permite escribir/leer al mismo tiempo.

* Primary Key and Foreign Key

Postgres nos fuerza a usar estas restricciones.

```sql
create table movies(
    id INTEGER PRIMARY KEY,
    NOMBRE VARCHAR2(2500),
    id_usuario INTEGER,
    FOREIGN KEY(ID_USUARIO) REFERENCES USERS(USER_ID) ON DELETE CASCADE
); 
)
```

_Cuando hacemos esto si eliminamos un usuario tambien estamos borrando todo lo relacionado a movives_

Otras opciones pueden ser:

|opcion|descripcion|sql|
|------|-----------|---|
|on restrict|No permite borrar ni usuario ni movie peor no da error.|
|no action| es la opcion por defecto, si se quiere borrar usuario da error|


## 2. Instalacion de postgres

```
Para instalar Postgres se puede usar la Instalacion On-premise, se puede usar el servicio en la nuve gratuito o Docker.
```
* Archivo docker

```docker
FROM postgres:latest

ENV POSTGRES_USER=nico123
ENV POSTGRES_DB=db
ENV POSTGRES_PASSWORD=nico123 
```
* Archivo Docker-compose

```docker
version: '3.8'
services:
  postgres_db_serv:
    build: ./postgres/
    container_name: postgres_udemy
    restart: always
    ports:
      - 5432:5432
    volumes:
      - ./db_postgres_vol/postgres_vol/:/var/lib/postgresql/data
```
### Ejemplo Web

[Sitio de postgres gratuito](wwww.elephantsql.com)

## 3. Interactuar con Python

Para interacturar con _postgres_ necesitamos dos packages.
- Psycopg2
- Psycopg2-binary

1. Update PIP

```python
import psycopg2

url = ""

connection = psycopg2.connect(url)

## En psycopg2 siempre hayq ue crear un cursor

cursor = connection.cursor()

cursor.execute("SELECT * FROM users;")

first_user = cursor.fetch_one()

connection.close()
```

2. Otra forma (MEJOR)


```python
import psycopg2

connection = psycopg2.connect(....)

with cursor.connection() as cursor:
    cursor.execute(...)


```

_Este enfoque es mejor porque cualquier recurso asociado con el cursor es liberado automaticamente despues de su uso._

## 4. Datos sensibles y variables de entorno

[Mas informacion sobre variables de entorno y ejemplos](https://developer.vonage.com/en/blog/python-environment-variables-a-primer)

```
Lo mejor es usar variables de sistema como las que creamos en docker. Generalemnte creamos un file con la extension .env que nos permite crear esta variables de entorno.
```
```python
pip install python-dotenv
```

_otra forma de trabajar con variables de entorno es con la libreria os_

[Mas informacion de OS](https://developer.vonage.com/en/blog/python-environment-variables-a-primer)

```python
from dotenv import load_dotenv

load_dotenv()
```

_Antes de cargar las variables, las mismas deben estar declaradas e un archivo con extencion .env que python reconoce._


## 5. Introduccion a Postgres

### Tipo de dato Serial

En postgers cuando creamos una tabla y queremos que un campo _INTEGER_ sea auto-incremental usamos el tipo _SERIAL_

```sql
CREATE TABLE user(
    id SERIAL PRIMARY KEY,
    nombre TEXT
)
```

### Subtipo de dato secuencia

```sql
CREATE SEQUENCE mi_secuencia;

select currval('mi_secuencia');

select nextval('mi_secuencia');
```


### Como pasar valores en PythonPostgres?

```
Una de las garndes diferencias en Postgres y SQLite es que en SQLite los valores o parametros se pasan con (?,?) mientras que en postgres se usa (%s,%s)
```


```python
FDX_INSERT = """INSERT INTO users(id, nombre) VALUES (%s.%s);"""
```

## ACID

Es una propiedad de base de datos relacionales.

|sigla|propiedad|descipcion|
|-----|---------|----------|
|A|Atomicidad| Las transacciones son indivisibles, cada transaccion debe ser exitosa o fallar, pero no puede haber resultados parciales. Ej. Si hacemos un INSERT y UPDATE en la misma Transaccion ambas deben terminar.
|C|Consistencia| La reglas y constraints se deben cumplir en todo momento. No podemos tener una FK que apunta a un valor de PK que no existe.|
|I|Isolacion|Data solo es visible para cada transaccion que la generó hasta que la misma es commiteada y visible para todas las transacciones|
|D|Durabilidad| HAce referencia a las persistencia de los datos en disco. Un contraejemplo es el procesamiento en memoria, es mas rapido pero riesgoso.|


## 7. Funcionalidad de Postgres SQL

### 7.1 Returning

```
Lo usamos para devolver el ID de lo ultimo insertado. Tambien se puede usar para en DELETE y UPDATE.
```

_EJEMPLO SIN RETURN_


Para aplicar este ejemplo debemos recordar la propiedad ACID (ISOLACION)
done lo que ocurre dentro de una transaccion está aislado de las demas hasta hacer un __commit__
```python
with connection:
  with connection.cursor() as cursor:
    cursor.execute("INSERT INTO polls(titulo, owner) VALUES (%s, %s);", (title, owner))
    cursor.execute("SELECT id FROM polls ORDER BY id DESC LIMIT 1;")
    return cursor.fetchone()[0]
```

Esto funciona porque está todo dentro de una sola transacción y el id (Autoincremental) solo es visible en la transacci+on actual. Pero una vez que salimos del _WITH_ se comitea porque se cierra la conexión.

_CON RETURNING_

```python
with connection:
  with connection.cursor() as cursor:
    cursor.execute("INSERT INTO polls(titulo, owner) values (%s, %s) returning id;",(title, owner))

    return cusor.fetchone()[0] #Tiene el ultimo id insertado. 
```

Este enfoque es mejor y más limpio, hay menos codigo y es 100% SQL.


### 7.2 Psycopg2 execute_value

Dentro de las extencion _extras_ existe una funcionalidad para pasar valores a una query sin hacer un for loop.

```python
from psycopg2.extras import execute_value

mi_lista_tupla = [(1, valor) from valor in otra_lista]

execute_value(cursor, MI_SENTENCIA_INSERT, mi_lista_tupla)
```

Esto es equivalente a hacer.

```python
mi_lista_tupla = [(1, valor) from valor in otra_lista]

for idx, valor in mi_lista_tupla:
  cursor.execute(MI_SENTENCIA_INSERT, (idx, valor))
```