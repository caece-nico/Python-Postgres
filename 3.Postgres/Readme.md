# Introducción a Postgres


1. [SQLite VS Postgres](#1.-sqlite-vs-postgres)
2. [Instalacion de Postgres](#2.-instalacion-de-postgres)
3. [Interactual con Python](#3.-interactuar-con-python)


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