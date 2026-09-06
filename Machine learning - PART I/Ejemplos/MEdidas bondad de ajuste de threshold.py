

## aqui es para analizar el threshold o la probabilidad de clasificacion de catergorias.

# en este caso trabajremos con un dataset de pruebas

import pandas as pd

# Cargar el dataset Pima Indians Diabetes desde un archivo CSV
url = 'https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv'
df = pd.read_csv(url, header=None)
df.columns

# La última columna es la variable objetivo
X = df.iloc[:, :-1]
y = df.iloc[:, -1]

print(X.head())
print(y.head())

## lo q hace es calsificar tipo de diabetes añadiendo variables objetivos y demas
# Análisis rápido sobre las características de la base
print(f'Número de filas y columnas {df.shape}') # Mostrar la forma del DataFrame (número de filas y columnas)
print(f'Tipo de los datos {df.dtypes}') # Mostrar los tipos de datos de las columnas
print(f'Estadísticas descriptivas {df.describe()}') # Mostrar estadísticas descriptivas del DataFrame
print(f'Matriz de correlación {df.corr()}') # Calcular la matriz de correlación entre las características numéricas
print(f'Número de muestras por categoría {df.groupby(df.iloc[:, -1]).size()}') # Contar el número de muestras por categoría
## pasamos alproceso de machine leargning####################################################
# Establecer una semilla concreta (en este caso, 12345)
SEED = 12345

# Para aleatorización en Python
import random
random.seed(SEED)

# Para aleatorización en numpy
import numpy as np
np.random.seed(SEED)

from sklearn.linear_model import LogisticRegression
# Definir el modelo de regresión, lo hacemos sin parámetros
model = LogisticRegression(random_state=SEED)
#¿qué pasa al no establecer iteraciones?
#model = LogisticRegression(max_iter=2000,random_state=SEED)
#Entrenar el modelo
model.fit(X, y)

#Obtener predicciones
y_pred = model.predict_proba(X)[:,1]

## esto no es buena practica ya que no estamos dividiendo el dataset en datos de prueba y de entrenamiento

### esto  o es un error y el algoritmo de optimizacion no ha terminado pero no es bueno

from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, confusion_matrix, auc, recall_score, precision_score
# accuracy = accuracy_score(y, y_pred)
# print(f"Accuracy: {accuracy}") -> ESTO DA ERROR A POSTA

###importante antes de empezar a obtener las metricas de socre hay q binarizar las métricas, ya que si no da error

########## que se peude calcualr usando estas probabilidades:
### la curva roc
from sklearn.metrics import roc_curve, auc
#roc_curve calcula las tasas fpr y tpr para distintos punto de corte, establecidos por el sistema dependiendo de los datos
fpr, tpr, thresholds = roc_curve(y, y_pred)
print(f"Tasa de falsos positivos: {fpr[:5]}")
print(f"Tasa de verdaderos positivos: {tpr[:5]}")
print(f"Puntos de corte (thresholds): {thresholds}")

### que umbarl usar?: dependiendo del problema, hay que usar uno u otro. si quiero mejorar la sensibilidad, hay que usar una bajo mientras que si quiero usar uno que mejore la precision, tiene que ser uno alto

import numpy as np

# Calcular el índice de Youden para cada umbral
youden_index = tpr - fpr

# Encontrar el umbral que maximiza el índice de Youden
best_threshold = thresholds[np.argmax(youden_index)]

print(f"Umbral óptimo según el índice de Youden: {best_threshold}")

## suponiendo que tomamos este umbral como binarizacion, obtenemos entonces las categorias:

threshold=best_threshold
y_pred_binary = (y_pred >= threshold).astype(int)
## tmb calculamos las metricas necesarias
#matriz de confusión
cm = confusion_matrix(y, y_pred_binary)
tn, fp, fn, tp= cm[0][0], cm[0][1], cm[1][0], cm[1][1]     
print(f"Los elementos de la matriz de confusión son tn: {tn}; fp: {fp}; fn: {fn} y tp: {tp}.")


import matplotlib.pyplot as plt
import seaborn as sns
clases = ['0', '1']

# Crear un mapa de calor para mejorar la visualización
plt.figure(figsize=(2, 2))
sns.heatmap(cm, annot=True, cmap='Greens', fmt='g', xticklabels=clases, yticklabels=clases)
plt.xlabel('Valores predichos')
plt.ylabel('Valores reales')
plt.title('Matriz de confusión')
plt.show()
plt.close()

accuracy = accuracy_score(y, y_pred_binary)
print(f"Accuracy: {accuracy}")

precision=precision_score(y, y_pred_binary)
print(f"Precisión: {precision}")

f1=f1_score(y, y_pred_binary)
print(f"F1_score: {f1}")

recall = recall_score(y, y_pred_binary)
print(f"Recall/sensibilidad: {recall}")

#########3 con todo esto hemos generado un dataframe para poder ver como se comporta cada metrica csegun el punto de binarización.

 # Iterar a través de thresholds para comparar resultados
thresholds = [0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7]
results_df = pd.DataFrame(columns=["FP", "FN", "TP", "TN","recall","precision","accuracy","f1","TH"])
for threshold in thresholds:
    y_pred_binary = (y_pred >= threshold).astype(int)
    clases = ['0', '1']
    cm = confusion_matrix(y, y_pred_binary)
    fp, fn, tp, tn = cm[0][1], cm[1][0], cm[1][1], cm[0][0]
 # Create a heatmap of the confusion matrix
    plt.figure(figsize=(2, 2))
    sns.heatmap(cm, annot=True, cmap='Blues', fmt='g', xticklabels=clases, yticklabels=clases)
    plt.xlabel('Predicciones')
    plt.ylabel('Etiquetas reales')
    plt.title('Threshold=' + str(threshold) + ' Matriz de confusión ')
    #si se quisieran guardar las imágenes
    #filename = 'TH=' + str(threshold) + ' Confusion Matrix ' + '.png'
    #filename = filename.replace("\n", "_").replace(" ", "_").replace(".", "") 
        
    plt.show()
    plt.close()

    accuracy = accuracy_score(y, y_pred_binary)
    print(f"Accuracy: {accuracy}")

    precision=precision_score(y, y_pred_binary)
    print(f"Precisión: {precision}")
    
    f1=f1_score(y, y_pred_binary)
    print(f"F1_score: {f1}")

    recall = recall_score(y, y_pred_binary)
    print(f"Recall/sensibilidad: {recall}")
    new_row = pd.DataFrame({
                "FP": [fp],
                "FN": [fn],
                "TP": [tp],
                "TN": [tn],
                "recall": [recall],
                "precision": [precision],
                "accuracy": [accuracy],
                "f1": [f1],                
                "TH": [threshold],
            })
      # Concatenar la nueva fila al DataFrame de resultados
    results_df = pd.concat([results_df, new_row], ignore_index=True)
## ahora vemos gráficamente para encontrar un punto de corte q nos pueda servir::

import matplotlib.pyplot as plt
import pandas as pd

plt.figure(figsize=(10, 6))

# Graficar cada métrica con su respectiva coloración y marcador
plt.plot(results_df['TH'], results_df['recall'], label='Recall', color='yellow', marker='o')
plt.plot(results_df['TH'], results_df['precision'],label='Precision', color='purple', marker='s')
plt.plot(results_df['TH'], results_df['accuracy'], label='Accuracy', color='red', marker='x')
plt.plot(results_df['TH'], results_df['f1'], label='F1', color='pink', marker='d')

# Configuración de la gráfica
plt.title('Evolución de las métricas en función del thresholds')
plt.xlabel('Threshold (TH)')
plt.ylabel('Valor')
plt.legend()

# Mostrar la cuadrícula
plt.grid(True)

# Mostrar la gráfica
plt.show()

