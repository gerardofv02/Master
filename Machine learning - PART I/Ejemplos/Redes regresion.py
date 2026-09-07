#importar las librerías necesarias
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree
import seaborn as sns
import plotly.graph_objects as go
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler, StandardScaler, Normalizer, Binarizer, RobustScaler, label_binarize
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, PowerTransformer
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.tree import DecisionTreeClassifier, export_text, DecisionTreeRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, roc_curve, auc
from sklearn.metrics import make_scorer, mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score
import os
os.chdir('C:/Users/gerar/Desktop/Master/Master/Machine learning - PART I/Data')
seed=12345 #fijamos la semilla de aleatorización para que sea la misma en todo el proceso
#Reemplaza con la ruta correcta y nombre de tu archivo
file_path = 'compress.csv' 
#convertir a data frame el archivo
df = pd.read_csv(file_path)
print(df.head())
#La variable de interés es strength
#analizamos la frecuencia de cada clase
print(f'\n Instancias: {df.shape[0]}; Variables: {df.shape[1]}')

#renombramos variables para usarlas más cómodamente
nuevos_nombres = ['cement', 'blast','ash','water','plasticizer','coarse','fine','day','strength']

# Asignar nuevos nombres a las columnas
df.columns = nuevos_nombres
print("\nDataFrame con columnas renombradas:")
print(df)

##minimo de exploracion
# representamos la relación enre la variable de interés y las variables input
# relaciones no lineales, aparente buen escenario para el uso de redes
sns.regplot(x=df['cement'], y=df['strength'], ci=None,fit_reg=False)
plt.xlabel('cement')
plt.ylabel('strength')
plt.title('Diagrama de Dispersión')
plt.show()


# Crear el diagrama de dispersión con regresión
sns.regplot(x=df['water'], y=df['strength'], ci=None,fit_reg=False)
plt.xlabel('water')
plt.ylabel('strength')
plt.title('Diagrama de Dispersión')
plt.show()

## verificamos las cosas necesarias antes de empezar: no hayan datos faltantes, datos estandarizados y las categoricas a dummies
# hay valores perdidos?
df.isna().sum()
# organiza las variables según su naturaleza
#hacer una lista con las variables input numericas
num_cols = ['cement', 'blast','ash','water','plasticizer','coarse','fine','day','strength']
#hacer una lista con las variables input categóricas: no hay

## ahora toca separar datos en entrenamiento y test y crear el modelo
# Separar las variables predictoras y la variable de respuesta.
# El grupo de variables predictoras se define y se fija
X = df[['cement','blast','water']] 
y = df['strength']

# 1. Dividir los datos en entrenamiento y test (20% de los datos para test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=seed)

#2. No hay variables categóricas, no hay missing, estandarizo las continuas.
scaler= StandardScaler()
X_train=scaler.fit_transform(X_train) #busco la media y desviación típica en train, después transformo train
X_test=scaler.transform(X_test) #con la media y desviación típica que calculé en train, transformo test

#primer approach a red neuronal: definimos la arquitectura
############ ESTO HA SIDO COMENTADO EN CUANTO HA DADO EL WARNING DE NO TERMINADO####################
# red1 = MLPRegressor(random_state=seed, hidden_layer_sizes=(5),activation='tanh',
#                      alpha=0.001,solver='adam',max_iter=200, learning_rate_init=0.01)
# # Construir el modelo de red ajustando los pesos a datos de train (ya estandarizados con media y desviación típica de train)
# red1.fit(X_train, y_train)
#######################################################################################################
## aqui nos da un error, esto se debe a que a alcanzado el numero maximo de iteraciones y no ha terminado (en este caso 200 (max_iter))

## añadimos mas para que termine bien 
red1 = MLPRegressor(random_state=seed, hidden_layer_sizes=(5),activation='tanh',
                     alpha=0.001,solver='adam',max_iter=1000, learning_rate_init=0.01)
# Construir el modelo de red ajustando los pesos a datos de train (ya estandarizados con media y desviación típica de train)
red1.fit(X_train, y_train)

## COMO VEMOS QUE HA FUNCIONADO FALTA EVALUARLO###################################################################
######################### ESTO SIRVE PARA VER SI ESTA SOBREAJUSTANDO, SI SE APRECE EL DE ENTRENAMIENTO AL DE TEST
# una vez ajustado el modelo en datos de train, lo evaluamos en datos de test
# es importante comparar los resultados en tr/ts para evitar underfiiting/overfitting
# Predicciones en el conjunto de entrenamiento y prueba
y_train_pred = red1.predict(X_train)
y_test_pred = red1.predict(X_test)

# Calcular métricas de rendimiento
mse_train = mean_squared_error(y_train, y_train_pred)
mse_test = mean_squared_error(y_test, y_test_pred)
r2_train = r2_score(y_train, y_train_pred)
r2_test = r2_score(y_test, y_test_pred)

print(f'MSE en conjunto de entrenamiento: {mse_train:.4f}')
print(f'MSE en conjunto de prueba: {mse_test:.4f}')
print(f'R2 en conjunto de entrenamiento: {r2_train:.4f}')
print(f'R2 en conjunto de prueba: {r2_test:.4f}')
### ESTO ES UN CASO EN EL QUE PODRIAMOS ESTAR HABLANDO DE SOBREAJUSTE PORQE EL R2 EN TRAIN ES RELATIVAMENTE MAS ALTO QUE EN TEST. Si lo hago mejor en train q en test y parto de que la red es un modelo es muy ciomplejo y la base de datos muy pequeña esto me tiene que dar la idea de que estoy sobreajustando y que deberia reduicir la complejidad del modelo
##################################################################################
########## REPRESENTAMOS GRAFICAMENTE ESTO@############################
# Graficar predicciones vs. observaciones reales
plt.scatter(y_test, y_test_pred)
plt.xlabel('Valor Real')
plt.ylabel('Predicción')
plt.title('Predicciones vs. Observaciones Reales')
plt.show()
#########################################################
###################### APLICAMOS TMB PROCESO DE VALIDACION CRUZADA####################
#Aplicamos validación cruzada para obtener una evaluación más robusta
cv_scores = cross_val_score(red1, X, y, cv=5, scoring='neg_mean_squared_error') # EL NEG, ESTO LO QUE HACE ES MAXIMIZAR EL NEGATIVO DE ESE ERROR. ESTO SE DEBE A QUE EL ALGORITMO DE MAXIMIZACION TRATA DE MAXIMIZO
cv_mse_mean = -np.mean(cv_scores) #PARA VERLO ES MULTIPLICXNADOLO POR -1

print(f'MSE promedio mediante validación cruzada: {cv_mse_mean:.4f}')

###################################################################################
###############################################################################################