# Proyecto de Detección de Señas en Lenguaje de Python

Este repositorio contiene el código y los recursos necesarios para construir un sistema de detección de señas en lenguaje de señas utilizando Python. El proyecto se divide en cuatro partes principales:

## 1. Recolecta de Imágenes
En esta etapa, se proporciona un script para la captura y almacenamiento de imágenes de manos que serán utilizadas como datos de entrada para el modelo de detección.

## 2. Creación de un Conjunto de Datos Etiquetado
Una vez recolectadas las imágenes, se procede a etiquetarlas manualmente o mediante algún proceso automatizado. Este conjunto de datos etiquetado servirá como la base sobre la cual el modelo de detección será entrenado.

## 3. Carga y Preparación de Datos de Entrenamiento
Este paso implica la carga de los datos de entrenamiento y sus etiquetas desde un archivo pickle previamente generado. Además, se realiza una división de estos datos en conjuntos de entrenamiento y prueba para la evaluación del modelo.

## 4. Entrenamiento y Evaluación del Clasificador
Se entrena un clasificador de Bosques Aleatorios (Random Forest) utilizando el conjunto de datos de entrenamiento preparado en la etapa anterior. Luego, se evalúa el rendimiento del modelo utilizando el conjunto de prueba.

## Ejecución del Modelo
Finalmente, se proporciona un script de ejecución que utiliza el modelo entrenado para detectar señas en nuevas imágenes de manos. Este script es la culminación del proyecto y muestra cómo utilizar el modelo en un entorno práctico.

## Conexión a la Base de Datos
Para la gestión de datos, se utiliza una base de datos MySQL. Se proporciona un script de conexión `conexion.py` en la carpeta correspondiente, que contiene la siguiente función:


```python
import mysql.connector

def conectar_db():
    connection = mysql.connector.connect(
        host="",
        user="",
        password="",
        database=""
    )
    return connection

```
## Script SQL para crear la base de datos y la tabla necesaria
``` MYSQL
# Crear la base de datos (si no existe)
CREATE DATABASE IF NOT EXISTS imagenes_bd;

# Usar la base de datos imagenes_bd
USE imagenes_bd;

# Crear la tabla imagenes
CREATE TABLE imagenes (
  id_imagen INT AUTO_INCREMENT PRIMARY KEY,
  id_clase INT NOT NULL,
  nombre_imagen VARCHAR(255) NOT NULL,
  imagen LONGBLOB NOT NULL,
  fecha_captura DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX (id_clase),
  INDEX (fecha_captura)
);
```
 ## ¡Completar las credenciales de conexión en el archivo conexion.py antes de utilizarlo!
