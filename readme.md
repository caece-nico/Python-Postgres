# Introducción a Python + Postgres

1. [Introduccion](#1.-introduccion)
    + [Entorno de instalacion](#entorno-de-instalacion)


## 1. Introduccion


## Entorno de instalacion

Para crear este entorno vamos a instalar python en un entorno virtual para trabajarlo local desde nuesta PC.
Tambien vamos a instalar la misma versión de python en __docker__ con las librerias necesarias y __Postgres__ con un volumen externo para no perder los datos.
Agregar este Volumen a __.gitignore__ para no subirlo a github.

### 1. Creacion del entorno virtual de python

Desde una consola __cmd__ hacemos

```bash
python --version

python -m venv d:\proyectos\xxx\mi_venv
```

Con esto ya creamos nuestro entorno virtual con Python, ahora lo activamos

```

D:\Proyectos\Python-Postgres\mi_venv>Scripts\activate

(mi_venv) D:\Proyectos\Python-Postgres\mi_venv>
```

Una vez activo ingresamos a __vcode__ y presionamos ctrl + shitf + p y seleccionamos la opcion __Select Python Interpreter__ y buscamos nuestro entorno creado.

![](/img/select_entorno_virtual_01.png)

_Ya podemos empezar a instalar cosas en nuestro entorno_ Por ej. Librerias, Spark, Flask, etc.

### 2. Creacion de los contenedores

Ahora para poder deployar nuestra aplicacion en un entorno real creamos los contenedores de Python y Postgres.

__¿Porque creamos un contenedor de python si ya tenemos un entorno virtual en nuestra PC?__

Esto lo hacemos porque el entorno virtual es para desarrollo local. Podriamos desarrollar dentro del contendor pero esto trae algunos problemas como el exesivo consumo de recursos.
_Importante_ Todo lo que instalemos en el entorno virtual debe estar tambien en el contenedor.

#### Dockerfile - Python

```
Usamos PYthon desde el entorno virtual por ahora.
```


#### Dockerfile - Postgres

Para INstalar postgres necesitamos crear una carpeta __postgres__ que contenga un archivo __Dockerfile__

__archivo Dockerfile__

```docker
FROM postgres:latest

ENV POSTGRES_USER=nico123
ENV POSTGRES_DB=db
ENV POSTGRES_PASSWORD=nico123
```
En el directorio raíz creamos una fichero _docker-compose.yml_

```docker
version: '3.8'
services:
  postgres_db:
    build: ./postgres/
    container_name: postgres_cta
    restart: always
    ports:
      - 5432:5432
    volumes:
      - ./db/volume/:/var/lib/postgresql/data
```

_notas importantes_ Esta configuración expone el puerto de postgres en el 5432 y crea un volumen __db__ donde persistimos la base de datos.

```bash
docker-compose up
```

#### Sqlite

```
Hay varias formas de usar sqlite.
1. Local 
2. En docker
```

#### 1. Dockerfile - Sqlite


[Guia rápida de configuracion](https://thriveread.com/sqlite-docker-container-and-docker-compose/)


Creamos el directorio sqlite

```docker
FROM alpine:latest
# Install SQLite
RUN apk --no-cache add sqlite
# Create a directory to store the database
WORKDIR /db
# Copy your SQLite database file into the container
COPY initial-db.sqlite /db/
# Expose the port if needed
# EXPOSE 1433
# Command to run when the container starts
CMD ["sqlite3", "/data/initial-db.sqlite"]
```

Despues de crear la imagen haciendo 

```docker
cd sqlite
docker build -t sqlite_db .
```

Ejecutamos la imagen

```docker
docker run -it -v sqlite_data:/data --name sqlite_container sqlite_db -p 3000:3000
```

#### 2. Local - Sqlite

Hacerlo local es mas fácil y rápido.

1. Desde la pagina de sqlite vamos a downloads y buscamos para windows _sqlite tools_ (Precompiled Binaries for Windows
))

[Descargas](https://www.sqlite.org/download.html)

2. Lo descragamos y descomprimimos es un carpeta en el disco D:\src\

3. Creamos una variable de sistema para poder referenciarlo desde linea de comando.

![](/img/sqlite_variable_global_01.png)

4. Desde la linea de comando escribimos el comando para acceder a la terminal

```bash
sqlite3
```
5. Desde el directorio donde estamos posicionados vamos a crear una carpeta que contendrá nuestra BD.

```cmd
mkdir mi_bd
sqlite3 mi_bd/bd_prueba
```

```
Si vamos a ver esta carpeta vemos que aún no hay nada creado, porque el motor recien la crea cuando la empezamos a usar.
```

```
.databses
```

Ya podemos usar esta base de datos desde python.