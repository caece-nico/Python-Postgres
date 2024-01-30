# Introducción a Postgres


1. [SQLite VS Postgres](#1.-sqlite-vs-postgres)
2. [Instalacion de Postgres](#2.-instalacion-de-postgres)
3. [Interactual con Python](#3.-interactuar-con-python)
4. [Datos sensibles y variables de entorno](#4.-datos-sensibles-y-variables-de-entorno)
5. [Introducción a Postgres](#5.-introduccion-a-postgres)
    [Tipo de dato Serial](#tipo-de-dato-serial)
      * [Subtipo de dato Secuencia](#subtipo-de-dato-secuencia)
    [Como pasar valores en Python/postgres](#Como-pasar-valores-en-pythonpostgres?)


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

