# Introduccion a Python y Sqlite

1. [Intro al proyecto](#1.-intro-al-proyecto)
2. [Que es SQL?](#2.-que-es-sql?)
3. [Cómo usar Sqlite3?](#3.-como-usar-sqlite3?)
    * [Conexiones en DB](#Conexiones-en-db)
    * [Transacciones en BD](#transacciones-en-bd)

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