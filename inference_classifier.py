import pickle
import cv2
import mediapipe as mp
import numpy as np

# Cargar el modelo
model_dict = pickle.load(open('./model.p', 'rb'))
model = model_dict['model']

# Configurar la captura de video
cap = cv2.VideoCapture(0)

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

# Definir el diccionario de etiquetas
labels_dict = {0: 'Hello', 1: 'I love you', 2: 'Thank you'}
default_word = "Unknown"  # Palabra predeterminada si no se reconoce ninguna de las palabras esperadas
detected_word = default_word  

# Cargar las imágenes predeterminadas para cada palabra
images_dict = {
    'Hello': cv2.imread('img/Hello.png'),
    'Thank you': cv2.imread('img/Thank_you.png'),
    'I love you': cv2.imread('img/I_love.png')
}

while True:
    data_aux = []  # Lista para almacenar las características de la mano en x & en y
    x_ = []
    y_ = []

    ret, frame = cap.read()  
    H, W, _ = frame.shape  

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convertir el fotograma a formato RGB

    # Procesar la mano con MediaPipe Hands
    results = hands.process(frame_rgb)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())

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

        # Realizar la predicción utilizando el modelo
        prediction = model.predict([np.asarray(data_aux)])

        # Obtener el gesto predicho y mostrarlo en el fotograma
        detected_word = labels_dict.get(int(prediction[0]), default_word)
        cv2.putText(frame, detected_word, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Mostrar la imagen predeterminada correspondiente a la palabra detectada
        image = images_dict.get(detected_word)
        if image is not None:
            cv2.imshow('image', image)

    # Mostrar el fotograma procesado en una ventana
    cv2.imshow('frame', frame)

    # Salir del bucle si se presiona la tecla 'q'   
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la cámara y cerrar todas las ventanas
cap.release()
cv2.destroyAllWindows()