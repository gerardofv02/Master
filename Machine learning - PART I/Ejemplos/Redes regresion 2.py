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

## ahora seleccionar las variables explicativas y la variable que hay q predecir (objetivo)
# Separar las variables predictoras y la variable de respuesta.
# El grupo de variables predictoras se define y se fija
X = df[['cement','blast','water']] 
y = df['strength']

# ahora toca dividir los datos en entrenamiento y test
# 1. Dividir los datos en entrenamiento y test (20% de los datos para test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=seed)
##ahora estandarizar los datos, quitar/sustituir valores missings y pasar de catgegoricas a dunmmies
# en este caso no hya categoricas y no hay missing con loq  solo estandarizamos:
#2. No hay variables categóricas, no hay missing, estandarizo las continuas.
scaler= StandardScaler()
X_train=scaler.fit_transform(X_train) #busco la media y desviación típica en train, después transformo train
X_test=scaler.transform(X_test) #con la media y desviación típica que calculé en train, transformo test
##aqui antes de sleccionar el m,ocelo poderiamos incluir un proceso de sleccion de vairables si lo necesitaramos como por ejemplo con un select fabes, con un arbol,...


# definimois el modelo
red = MLPRegressor(random_state=seed,max_iter=900)
#definimos los parámetros que queremos tunear (probamos las 12 combnionaciones posibles)
params = {
    'hidden_layer_sizes': [5,7,9],
    'activation': ['tanh','relu'],
    'alpha': [0.001,0.0001]
}
scoring_metrics = ['neg_mean_squared_error', 'neg_mean_absolute_error', 'r2'] # esto  se va aevaluar con valores de error
# cv = crossvalidation con n folds con todas las combinaciones de parámetros
grid_search = GridSearchCV(estimator=red, 
                           param_grid=params, 
                           cv=4, scoring = scoring_metrics, refit='neg_mean_squared_error')

#ajusta en entrenamiento con todas las combinaciones
grid_search.fit(X_train, y_train)

##con esto no ha terminado la optimizacion con loq ue se deberia hacer es aummentar el numero de iteracions y anzalizar que lo que estoy analizando es minimo local de error porque si no ha terminado no garantriza lo cerca o lejos q esta de la solcuion

## en este caso vamos a continuar asi con el proceso, analizando los resultados
# Obtener resultados del grid search
results = pd.DataFrame(grid_search.cv_results_)
# Mostrar resultados
print("Resultados de Grid Search:")
print(results[['params','mean_test_neg_mean_absolute_error','mean_test_r2']])
#print(results) #para ver todos los atributos obtenidos y entender cómo usarlos

# Obtener el mejor modelo (en cuanto a optimización del criterio)
best_model = grid_search.best_estimator_
print(grid_search.best_estimator_)

## comomqueremos ser mejor q la maquina lo q vamos a ahcer es ordenar nuestro conjunto de resultados en funcion del valor en test del error absoluto
import pandas as pd

# Supongamos que tienes un DataFrame df con la columna mean_test_neg_mean_absolute_error
# ordenamos así porque está en negativo!! el MSE en general cuanto más bajo, mejor. En este caso, tenemos que aatender al valor absoluto
results = results.sort_values(by='mean_test_neg_mean_absolute_error', ascending=False)  # de mayor a menor para asumir q las mejores arquitecturas quedan arriba 
results
##nos centramos en las mejores parametrización:.

# Escogemos la parametrizaciones mejores candidatas: 0, 1, 2
print("Parametrización 0:")
print(results.iloc[0].params)
print("Parametrización 1:")
print(results.iloc[1].params)
print("Parametrización 2:")
print(results.iloc[2].params)
# tenem,os estas arquitecturas:
# Parametrización 0:
# {'activation': 'relu', 'alpha': 0.001, 'hidden_layer_sizes': 5}
# Parametrización 1:
# {'activation': 'relu', 'alpha': 0.0001, 'hidden_layer_sizes': 5}
# Parametrización 2:
# {'activation': 'relu', 'alpha': 0.0001, 'hidden_layer_sizes': 7}

## segun vemos aqui, tenemos varias veces lo de que tenemos como mejor opcion 5 nodos ocultos, esto noss da a indicar que igual deberiamos probar con 4,5,6

# hacemos la represntacion nde los resultados, tomamos el r2 y el mse:
# se selecciona el modelo candidato, y se procede a analizar su robustez a lo largo de cross validation.
r2_0 = results[['split0_test_r2', 'split1_test_r2','split2_test_r2', 'split3_test_r2']].iloc[0]
r2_1 = results[['split0_test_r2', 'split1_test_r2','split2_test_r2', 'split3_test_r2']].iloc[1]
r2_2 =results[['split0_test_r2', 'split1_test_r2','split2_test_r2', 'split3_test_r2']].iloc[2]

# se selecciona el modelo candidato, y se procede a analizar su robustez a lo largo de cross validation.
# tomamos el valor absoluto porque está en negativo
mse_0 = results[['split0_test_neg_mean_squared_error', 'split1_test_neg_mean_squared_error','split2_test_neg_mean_squared_error', 'split3_test_r2']].iloc[0].abs()
mse_1 = results[['split0_test_neg_mean_squared_error', 'split1_test_neg_mean_squared_error','split2_test_neg_mean_squared_error', 'split3_test_r2']].iloc[1].abs()
mse_2 = results[['split0_test_neg_mean_squared_error', 'split1_test_neg_mean_squared_error','split2_test_neg_mean_squared_error', 'split3_test_r2']].iloc[2].abs()
## represntandolo vemos que como esta en negativo tomamos los valores absolutos

# Crear un boxplot para los cuatro valores de r2
plt.boxplot([r2_0.values,r2_1.values,r2_2.values], tick_labels = ['red0','red1','red2'])
plt.title('Boxplots de r2 para los 4 Splits')
plt.xlabel('Splits de Cross Validation')
plt.ylabel('r2')
plt.show()

# Crear un boxplot para los cuatro valores de MSE
plt.boxplot([mse_0.values,mse_1.values,mse_2.values], tick_labels = ['red0','red1','red2'])
plt.title('Boxplots de MSE para los 4 Splits')
plt.xlabel('Splits de Cross Validation')
plt.ylabel('MSE')
plt.show()


# boxplots con gran amplitud no son deseables, ya que se caracterizan por poca robustez de la solución
## en general este analisis dice que las red 0 y 1 tienen mejor RSE que la red 2 poero su coeficiente r2 es algo mas inestable aunque mejor.
# por otro lado vemos que la red 0 y al red 1 son mas sencillas (por la cantidad de nodos ocultos). Entonces si tuviesemos que empezar a descartar, igual descartiamos la red 2 que tiene 7 nodos en capa oculta. Nos quedfamos entonces con las dos primeras, que la diferencia sesta uinicamente en elk alhpa
print(f'Arquitectura red 0: {results.iloc[0].params}')
print(f'Arquitectura red 1: {results.iloc[1].params}')
# Arquitectura red 0: {'activation': 'relu', 'alpha': 0.001, 'hidden_layer_sizes': 5}
# Arquitectura red 1: {'activation': 'relu', 'alpha': 0.0001, 'hidden_layer_sizes': 5}

# un alpha grande tiene un menor riesgo de sobre ajuste y un alpha pequeño tiene un poqquito mayor riesgo de sobreajuste pero tmb mas capacidad para aprender.

## POR OTRO LADO SI NOS VAMOS AL MODELO PARECE QUE AMBOS ESTAN HACIENDO EXACTAMENTE LO MISMO
# con lo cual ante igualdad de condiciones es preferible que gane con un alpha grande

## pero por otro lado hemos visto que tendriamos que aumentar la parrilla de busqueda de los nodos invisibles 

## por tanto, fijamos la funcion de activacion que ha funcionado bien (relu), nos quedamos con el alpha grande y juego con ops nodos ocultos 

##volvemos a entrenar y validar:>
# Tuneo y evaluación predictiva del modelo para variable dependiente continua
# El grupo de variables predictoras se define y se fija
X = df[['cement','blast','water']]
y = df['strength']

# 1. Dividir los datos en entrenamiento y test (20% de los datos para test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=seed)

#2. No hay variables categóricas, no hay missing, estandarizo las continuas.
scaler= StandardScaler()
X_train=scaler.fit_transform(X_train) #busco la media y desviación típica en train, después transformo train
X_test=scaler.transform(X_test) #con la media y desviación típica que calculé en train, transformo test


red2 = MLPRegressor(random_state=seed,max_iter=800,activation='relu',alpha=0.001)
#definimos los parámetros que queremos tunear
params2 = {
    'hidden_layer_sizes': [3,4,5,6]
}
scoring_metrics = ['neg_mean_squared_error', 'neg_mean_absolute_error', 'r2']
# cv = crossvalidation con n folds con todas las combinaciones de parámetros
grid_search2 = GridSearchCV(estimator=red2, 
                           param_grid=params2, 
                           cv=4, scoring = scoring_metrics, refit='neg_mean_squared_error')

#ajusta en entrenamiento con todas las combinaciones
grid_search2.fit(X_train, y_train)

## volvemos a tener problemas de convergencia, habria que aumentar la cantidad de iteraciones, pero por ahora lo dejamos asi 

##volvemos a ordcenar los resultados obtenidos para ver el mejro modelo:
# Obtener resultados del grid search
results2 = pd.DataFrame(grid_search2.cv_results_)

# Supongamos que tienes un DataFrame df con la columna mean_test_neg_mean_absolute_error
# ordenamos así porque está en negativo!! el MSE en general cuanto más bajo, mejor. En este caso, tenemos que aatender al valor absoluto
results2 = results2.sort_values(by='mean_test_neg_mean_absolute_error', ascending=False)  # de mayor a menor
results2

# Como solo son 4, los miro todos

# se selecciona el modelo candidato, y se procede a analizar su robustez a lo largo de cross validation.
r2_0_2 = results2[['split0_test_r2', 'split1_test_r2','split2_test_r2', 'split3_test_r2']].iloc[0]
r2_1_2 = results2[['split0_test_r2', 'split1_test_r2','split2_test_r2', 'split3_test_r2']].iloc[1]
r2_2_2 =results2[['split0_test_r2', 'split1_test_r2','split2_test_r2', 'split3_test_r2']].iloc[2]
r2_3_2 =results2[['split0_test_r2', 'split1_test_r2','split2_test_r2', 'split3_test_r2']].iloc[3]

# se selecciona el modelo candidato, y se procede a analizar su robustez a lo largo de cross validation.
# tomamos el valor absoluto porque está en negativo
mse_0_2 = results2[['split0_test_neg_mean_squared_error', 'split1_test_neg_mean_squared_error','split2_test_neg_mean_squared_error', 'split3_test_r2']].iloc[0].abs()
mse_1_2 = results2[['split0_test_neg_mean_squared_error', 'split1_test_neg_mean_squared_error','split2_test_neg_mean_squared_error', 'split3_test_r2']].iloc[1].abs()
mse_2_2 = results2[['split0_test_neg_mean_squared_error', 'split1_test_neg_mean_squared_error','split2_test_neg_mean_squared_error', 'split3_test_r2']].iloc[2].abs()
mse_3_2 = results2[['split0_test_neg_mean_squared_error', 'split1_test_neg_mean_squared_error','split2_test_neg_mean_squared_error', 'split3_test_r2']].iloc[3].abs()

# Crear un boxplot para los cuatro valores de r2
plt.boxplot([r2_0_2.values,r2_1_2.values,r2_2_2.values,r2_3_2.values], tick_labels = ['red0','red1','red2','red3'])
plt.title('Boxplots de r2 para los 4 Splits')
plt.xlabel('Splits de Cross Validation')
plt.ylabel('r2')
plt.show()

# Crear un boxplot para los cuatro valores de MSE
plt.boxplot([mse_0_2.values,mse_1_2.values,mse_2_2.values,mse_3_2.values], tick_labels = ['red0','red1','red2','red3'])
plt.title('Boxplots de MSE para los 4 Splits')
plt.xlabel('Splits de Cross Validation')
plt.ylabel('MSE')
plt.show()


# Nótese en la solución que boxplots con gran amplitud no son deseables, ya que se caracterizan por poca robustez de la solución

## viendo esto vemos que la red 3 la podemos descartar y quizartmb la red 2, pero nos la quedamos por sia caso. 
# vemos a ver que pasa con estas redes:
print(f'Arquitectura red 0: {results2.iloc[0].params}')
print(f'Arquitectura red 1: {results2.iloc[1].params}')
print(f'Arquitectura red 2: {results2.iloc[2].params}')
# Arquitectura red 0: {'hidden_layer_sizes': 5}
# Arquitectura red 1: {'hidden_layer_sizes': 6}
# Arquitectura red 2: {'hidden_layer_sizes': 4}

# vemos que la red0 tiene 5 nodos en capa oculta meintras que la 1 tiene 6
#entonces vemos que la red 2 tiene un poco pero los valores y emnos nodos en capa oculta. entonces la decision es la siguiente>:
# depen de de lo que encesitamos para el modelo. si quieremos un modelo que funcione muy bien y que necesite mantenimiento,  bastaria con la red 0.
# funciona mejor q la 1 y es mas sencilla

##si preferimos un modelo mas sencillo aunqeu poierda un poco de calidad, nso quedariamos con la red 2 que es la mass sencilla de todas y se parece n bastante en calidad.

# suponiendo que nos quedamos con una, nos decantamos por la arquitectura de la red 0 
## antes de poner el modelo en  produccion no podemos asumir quie esta sea la paremetrizacion que me quede, se necesita siempre volver a entrenar y vcalidar el modelo. tenemos que poasarlo por el mismo proceso y divison de datos y transformacion con el cual hayamos preparado el gridsearch. definimos el mismo proceso de preparacion, vamos al final y vamos a la parte de entrenamiento definintivo:

from sklearn.metrics import r2_score


# El grupo de variables predictoras se define y se fija
X = df[['cement','blast','water']]
y = df['strength']

# 1. Dividir los datos en entrenamiento y test (20% de los datos para test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=seed)

#2. No hay variables categóricas, no hay missing, estandarizo las continuas.
scaler= StandardScaler()
X_train=scaler.fit_transform(X_train) #busco la media y desviación típica en train, después transformo train
X_test=scaler.transform(X_test) #con la media y desviación típica que calculé en train, transformo test


candidata =MLPRegressor(**results.iloc[0].params, random_state=seed) # mir ed canditat es la red 0
# Ajustar el mejor modelo con todo el conjunto de entrenamiento
candidata.fit(X_train, y_train) #la entrenamois con los valores de entrenmainto y los datos seran los q definan mi red final

# Predicciones en conjunto de entrenamiento y prueba
y_train_pred = candidata.predict(X_train)
y_test_pred = candidata.predict(X_test)
#ahora hacemos calculamos esto apra ver realemnte si hay mas o menos sobreajuste, sise parecen o no, analizamos metricas,...

errores = y_train - y_train_pred
# Calcular diferentes medidas de bondad de ajuste
mae = mean_absolute_error(y_test, y_test_pred)
mae_tr = mean_absolute_error(y_train, y_train_pred)
mse = mean_squared_error(y_test, y_test_pred)
mse_tr = mean_squared_error(y_train, y_train_pred)
rmse = np.sqrt(mse)
rmse_tr = np.sqrt(mse_tr)
r2_tr = r2_score(y_train, y_train_pred)
r2_ts = r2_score(y_test, y_test_pred)

# Imprimir las métricas
print(f'MAE (Error Absoluto Medio test): {mae:.2f}')
print(f'MSE (Error Cuadrático Medio test): {mse:.2f}')
print(f'RMSE (Raíz del Error Cuadrático Medio test): {rmse:.2f}')
print(f'R² test: {r2_ts:.2f}')

print(f'MAE (Error Absoluto Medio tr): {mae_tr:.2f}')
print(f'MSE (Error Cuadrático Medio tr): {mse_tr:.2f}')
print(f'RMSE (Raíz del Error Cuadrático Medio tr): {rmse_tr:.2f}')
print(f'R² tr: {r2_tr:.2f}')