import pickle
import mediapipe as mp
import cv2
import numpy as np
from conexion_db import conectar_db  # Importa la función conectar_db desde el módulo conexion_db

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

# Lista para almacenar las características de las manos y las etiquetas
data = []
labels = []

# Obtener la conexión a la base de datos
connection = conectar_db()
cursor = connection.cursor()

# Consulta para obtener todas las imágenes de la base de datos
cursor.execute("SELECT id_clase, imagen FROM imagenes")
imagenes = cursor.fetchall()

# Iterar sobre cada imagen obtenida de la base de datos
for imagen in imagenes:
    clase = imagen[0]
    img_bytes = imagen[1]

    # Convertir los datos binarios de la imagen a un array de bytes
    img_nparr = np.frombuffer(img_bytes, np.uint8)

    # Decodificar la imagen desde el array de bytes
    img = cv2.imdecode(img_nparr, cv2.IMREAD_COLOR)

    # Lista auxiliar para almacenar las características de la mano en x e y
    data_aux = []
    x_ = []
    y_ = []

    # Convertir la imagen a formato RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Procesar la imagen con MediaPipe Hands
    results = hands.process(img_rgb)
    if results.multi_hand_landmarks:
        # Recorrer todos los puntos de la mano y guardar las coordenadas
        for hand_landmarks in results.multi_hand_landmarks:
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                x_.append(x)
                y_.append(y)

            # Normalizar las coordenadas de los puntos de la mano
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                data_aux.append(x - min(x_))
                data_aux.append(y - min(y_))
        # Agregar las características de la mano y la etiqueta a las listas de datos y etiquetas
        data.append(data_aux)
        labels.append(clase)

# Guardar los datos y las etiquetas en un archivo pickle
with open('data.pickle', 'wb') as f:
    pickle.dump({'data': data, 'labels': labels}, f)

# Cerrar la conexión a la base de datos
cursor.close()
connection.close()

f = open('data.pickle', 'wb')
pickle.dump({'data': data, 'labels': labels}, f)
f.close()
