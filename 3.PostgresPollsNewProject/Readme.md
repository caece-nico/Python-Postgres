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
  + [Nested querys](#7.3-nested-querys)
  + [SQL built-in functions](#7.4-sql-built-in-functions)
  * [Group BY](#7.5-group-by)
  + [Windows Functions](#7.6-window-functions)
  + [Partition BY](#7.7-partition-by)
  + [Distinct ON](#7.8-distinct-on)
  + [SQL VIEW](#7.9-sql-view)
  + [Constraints - CHECK](#7.10-contraints-check)
8 [Python HINTING](#8.-python-hinting)



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

### 7.3 Nested Querys

```
Necesitamos nested querys para obtener  las ultimas polls y sus opciones
```

```sql
select *
from polls
inner join options on polls.id = options.poll_id
where polls.id =
                  (
                    select id 
                    from polls 
                    order by id 
                    desc limit 1)                 
```

+ Las nested querys se pueden usar en _SELECT_ _WHERE_ , etc.

__EJEMPLO__

Cuantas opciones tienen las encuentas?

```sql
select id,
        (select count(*) from options where options.poll_id = polls.id) as cuenta
from polls;
```

__EJEMPLO CON INSERT__

```sql
INSERT INTO poll_authors(
                        select poll_owner from polls
                        );
```

### WITH

_Buscamos los datos de la ultima polls ingresada_

```sql
WITH latest_id as(
  SELECT id FROM polls ORDER BY id DESC LIMIT 1
)

select *
from polls inner join options on polls.id = options.poll_id 
where polls.id = (select * from latest_id);
```

### 7.4 SQL built-in Functions

```
Existen muchas funciones en SQL que se pueden usar.
```
__MATEMATICA__

|funcion|descripcion|
|-------|-----------|
|random()| value entre 0 y 1|
|abs(x) | valor absoluto de x|
|mod(y,x) | el resto entre y/x|

__AGREGACION____

|funcion|descripcion|
|-------|-----------|
|count(expr)| Valor total de registros|
|avg(expr) | Devuelve el promedio |
|max(exp) | Devuelve el maximo |

+ ¿Cómo obtener un valor random?

```sql
SELECT *
FROM votes
WHERE option_id = %s 
ORDER BY random()
LIMIT 1;
```

### 7.5 Group BY

```
Se usa para devolver valores de columnas agrupadas.
Se usa con function calculadas como AVG, COUNT, MAX, MIN, ETC
```

```sql
SELECT poll_owner, COUNT(*)
FROM polls
GROUP BY poll_owner;
```

_¿Cómo optenemos el % de la votacion de una encuenta por cada opcion?_

```sql
select 
	id , 
	options.option_text , 
	count(votes.option_id),
	count(votes.option_id) /   sum(count(votes.option_id)) over() * 100
from options
left join votes 
on options.id = votes.option_id 
where options.poll_id  = 3
group by options.id
```
__Porqué hacemos esto: sum(count(votes.option_id)) over() * 100?__

Ya que todos los datos están en la misma tabla y necesitamos dividir el total de la suma de cada opción por el total de votos de una encuesta, la única forma de optener el total de votos para toda la poll = 3 es usando la sentencia _over_ ya que nos permite volver sobre toda la tabla y no sobre la agrupación.


### 7.6 Window Functions

```
Las windows functions tienen acceso a todo lo que tenemos en el FROM.
Si no ponemos nada en el OVER() Postgres asume que la tabla relacionado es todo a lo que tenga acceso.
Widows Functions solo tienen acceso a los registros que fueron filtrados en el WHERE.
```

#### ORDER BY  - Window Functions.

```
Queremos ver la cantidad toal de votos que recibió cada encuesta y luego hacer un ranking de la misma para ver cual fue la mas votada.
```

```sql
select p.title,count(v.option_id), rank() over(order by count(v.option_id) desc)
from polls p
left join "options" o 
on p.id  = o.poll_id 
left join votes v  
on o.id = v.option_id 
group by p.title;
```

_En este caso __OVER()__ no puede ir solo porque sino iria contra toda la tabla, pero queremos que ordene el count() total__

### 7.7 Partition BY

__EJEMPLO__

Queremos ver agrupado por _title_ el total de votos por cada opcion y rankeado por _titulo_  + _opacion_

```sql
select p.title , o.option_text , count(v.option_id), dense_rank () over(partition by p.title order by count(v.option_id ))
from polls p 
left join "options" o 
on p.id = o.poll_id 
left join votes v 
on v.option_id  = o.id 
group by p.title, o.option_text 
```

+ _dense_rank() vs rank()_

Cuando tenemos valores dentro de un __rank__ que no cambian el _rank_ no tomo en cuenta el valor siguiente y lo saltea.
El _dense_rank_ empieza desde el ultimo valor rankeado.

ejemplo rank.

|vendedor|totales|rank|dense_rank|
|--------|-------|----|----------|
|nicolas|456|1|1|
|patricio|456|1|1|
|alejandro|456|1|1|
|martin|345|4|2|

```
En este ejemplo tenemos los tres primeros vendedores con rank 1 pero el último tiene el valor total de regsitros salteados.
Si usaramos dense_rank el ranking quedarias 1->1->1->2
```

### 7.8 DISTINCT ON

```
Esta sentencia nos permite optener el primer registro de un set de registros agrupados.
```

_EJEMPLO_

Queremos obetenr la opcion mas votada de cada encuesta.

```sql
SELECT 
        distinct on (options.option_text)  opti ,
        count(votes.option_id)
from polls
left join options on polls.id = options.poll_id
left join votes ON votes.option_id  = options.id
group by opti , options.option_text
order by opti desc, count(votes.option_id) desc;
```

__NO FUNCIONA__ Remplazar por rank()

### 7.9 SQL VIEW

```
Una vista es un nombre para una query.
Son parecidas a las tablas pero si la vista no está materializada la query se ejecuta siempre, caso contrario no.
```

```sql
CREATE VIEW most_voted_options as
  SELECT *
  FROM votes;
```

|Tipos de vistas|Descripcion|Limitaciones|
|---------------|-----------|------------|
|UPDATABLE VIEWS| Tambien llamada simple VIEW, permite UPDATE, DELETE y INSERTS|1. No puede tener mas de una tabla en el FROM, HAVING, Agg. Functions. 2. No Usa los operadores UNION, INTERSECT, etc o Window Functions.|

```sql
INSERT INTO mi_vista VALUES (xx,xx);
```

```
Podemos insertar en una vista sin seguir la condición del WHERE
... WHERE salary > 5000;
Pero no podemos hacer UPDATE o DELETE de registros que no están en la vista.
```

_LOCAL CHECK OPTION_

La usamos para que solo podamos modificar una vista siguiendo la condición del WHERE.

```sql
CREATE VIEW mostrar_sueldos as
  SELECT *
  FROM employees
  WHERE  salary > 5000
  WITH LOCAL CHECK OPTION;
```
No acepta INSERT, DELETE o UPDATE con sueldos < 5000

_WITH CASCADE CHECK OPTION_

Si no especificamos esta opción las _sub-vistas_ pueden hacer inserts o deletes violando la restrinccion de la vista padre.

```sql
CREATE VIEW mostrar_sueldo_investigadores AS
SELECT *
FROM mostrar_sueldos
WHERE DEP_ID = 'investigadores'
WITH CHECK OPTION;
```

Esta vista  aceptaria  un INSERT con una salario menor a 5000 pero no un departamento distinto de 'investigacion'

_Si queremos reforzar esta relación a la vista hija le agregamos __WITH CASCADE CHECK OPTION__._


#### Vistas Materializadas.


```
Son vistas donde los datos estan persistidos en disco, la query no se ejecuta cada vez que se llama.
Mas rápidas pero ocupan espacio y se deben refrescar. Utiles cuando no necesitamos la ultima data.
```

```sql
CREATE MATERIZALIZED VIEW name AS .....

REFRESH MATERIALIZED  VIEW name;
```

### 7.10 Contrainsts CHECK

```
Es una restriccion a nivel de una o mas columnas, útil para limitar lo que se inserta o hace update.
```

```sql
CREATE TABLE ventas(
  id INTEGER PRIMARY KEY,
  articulo_id INTEGER,
  monto FLOAT CHECK (monto > 0), -- para una columna.
  discount_price FLOAT,
  CHECK (monto > discount_price); -- para varias columnas.
)
```

# 8. Python Hinting.

```
Permite evitar Bugs. Cada paremetro de una función le decimos de que tipo debe ser y que debe devolver.
```

```python
from typing import List, Touple

Poll = Tuple[int, int, str] #id, count, username

def mi_funcion(connection, poll_id: int):
  pass

def otra_funcion(connection, name: str, options: List[str]):
  pass

def otra_funcion(connection, name: str) -> Poll:
  pass
```

Ejemplos.

|Necesidad|Type hint|Ejemplo|
|---------|---------|--------|
|Esperamos una lista de strings| List[str]|def funcion(dato: List[str])|
|Quiero devolver una tuple de Postgres que tiene int, int, str| dato = Tuple[int, int, str]| def funcion(dato: int) -> dato:|
|Si no quiero devolver nada de un funcion|None| def funcion() -> None:
