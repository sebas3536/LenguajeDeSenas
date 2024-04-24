#Recoleccion de imagenes N°1 


import cv2
from conexion_db import conectar_db  # Importa la función conectar_db desde el módulo conexion_db

# Número de clases de datos a recopilar
number_of_classes = 3
# Tamaño del conjunto de datos por clase
dataset_size = 100

# Inicializar la captura de video desde la cámara web
cap = cv2.VideoCapture(0)

# Obtener la conexión a la base de datos
connection = conectar_db()
cursor = connection.cursor()

# Iterar sobre cada clase de datos a recopilar
for j in range(number_of_classes):
    print('Recopilación de datos para la clase {}'.format(j))

    # Esperar a que el usuario esté listo para capturar datos
    done = False
    while True:
        ret, frame = cap.read()
        # Mostrar un mensaje en la ventana de video
        cv2.putText(frame, 'Listo? Presiona "Q" ! :)', (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3,
                    cv2.LINE_AA)
        cv2.imshow('frame', frame)
        # Esperar hasta que el usuario presione la tecla "q" para continuar
        if cv2.waitKey(25) == ord('q'):
            break

    # Capturar y guardar las imágenes para la clase actual
    counter = 0
    while counter < dataset_size:
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        cv2.waitKey(25)

        # Convertir la imagen a formato de bytes
        _, img_encoded = cv2.imencode('.jpg', frame)
        img_bytes = img_encoded.tobytes()

        # Insertar la imagen en la base de datos
        cursor.execute("INSERT INTO imagenes (id_clase, nombre_imagen, imagen) VALUES (%s, %s, %s)",
                       (j, 'imagen_{}_{}.jpg'.format(j, counter), img_bytes))
        connection.commit()

        counter += 1

# Liberar la captura de video y cerrar todas las ventanas
cap.release()
cv2.destroyAllWindows()

# Cerrar la conexión a la base de datos
cursor.close()
connection.close()




"""
import os
import cv2

# Directorio donde se guardarán los datos recopilados
DATA_DIR = './data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Número de clases de datos a recopilar
number_of_classes = 3
# Tamaño del conjunto de datos por clase
dataset_size = 100

# Inicializar la captura de video desde la cámara web
cap = cv2.VideoCapture(0)

# Iterar sobre cada clase de datos a recopilar
for j in range(number_of_classes):
    # Crear un directorio para almacenar las imágenes de la clase actual
    if not os.path.exists(os.path.join(DATA_DIR, str(j))):
        os.makedirs(os.path.join(DATA_DIR, str(j)))

    print('Recopilación de datos para la clase {}'.format(j))

    # Esperar a que el usuario esté listo para capturar datos
    done = False
    while True:
        ret, frame = cap.read()
        # Mostrar un mensaje en la ventana de video
        cv2.putText(frame, 'Listo? Presiona "Q" ! :)', (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3,
                    cv2.LINE_AA)
        cv2.imshow('frame', frame)
        # Esperar hasta que el usuario presione la tecla "q" para continuar
        if cv2.waitKey(25) == ord('q'):
            break

    # Capturar y guardar las imágenes para la clase actual
    counter = 0
    while counter < dataset_size:
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        cv2.waitKey(25)
        # Guardar la imagen en el directorio correspondiente
        cv2.imwrite(os.path.join(DATA_DIR, str(j), '{}.jpg'.format(counter)), frame)

        counter += 1

# Liberar la captura de video y cerrar todas las ventanas
cap.release()
cv2.destroyAllWindows()

"""