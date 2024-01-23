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

