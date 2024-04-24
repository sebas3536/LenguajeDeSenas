import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np

# Cargar los datos de entrenamiento y etiquetas desde el archivo pickle
data_dict = pickle.load(open('./data.pickle', 'rb'))
data = np.asarray(data_dict['data'])
labels = np.asarray(data_dict['labels'])

# Dividir los datos en conjuntos de entrenamiento y prueba
x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, shuffle=True, stratify=labels)

# Inicializar y entrenar el modelo de clasificación (Random Forest)
model = RandomForestClassifier()
model.fit(x_train, y_train)

# Predecir las etiquetas para el conjunto de prueba
y_predict = model.predict(x_test)

# Calcular la precisión del modelo
score = accuracy_score(y_predict, y_test)

# Imprimir la precisión del modelo
print('{}% of samples were classified correctly!'.format(score * 100))

# Guardar el modelo entrenado en un archivo pickle
f = open('model.p', 'wb')
pickle.dump({'model': model}, f)
f.close()


