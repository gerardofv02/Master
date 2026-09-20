## vamos a crear un ejemplo de arboles con random forest

#########################################################################333
# ESte primer ejemplo es de clasificacion
##########################################################################
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier, export_text, DecisionTreeRegressor
from sklearn.tree import plot_tree
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, roc_curve, auc
from sklearn.metrics import make_scorer, mean_absolute_error, mean_squared_error, r2_score
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns  

# NOTA IMPORTANTE: AQUÍ SÓLO SE MUESTRA EL CÓDIGO NECESARIO PARA APLICAR RANDOM FOREST.

# RECUÉRDESE LA IMPORTANCIA DE LOS PASOS A SEGUIR PARA IMPLEMENTAR DE FORMA ADECUADA UN MODELO:
# (1) CARGAR BASE DE DATOS Y CONOCER FRECUENCIA DE CLASES O DISTRIBUCIÓN DE ACUERDO CON EL TIPO DE PROBLEMA.
# (2) DIVIR TRAIN, TEST Y COMPROBAR SI LA DISTRIBUCIÓN DE LA VARIABLE DEPENDIENTE ES SIMILAR EN AMBOS SETS.
# (3) AJUSTAR EL MODELO Y VALORAR LAS NECESIDADES DE INVESTIGACIÓN PARA DAR MÁS PESO A UNAS MEDIDAS DE BONDAD DE AJUSTE CON RESPECTO A OTRAS. 
# (3.1) APLICAR VALIDACIÓN CRUZADA Y, EN CASO DE NECESIDAD, UN GRIDSEARCH PARA CONOCER LAS BONDADES DE AJUSTE PARA DISTINTAS PARAMETRIZACIONES.
# (4) HACER PREDICCIONES SOBRE TRAIN Y TEST CON EL FIN DE OBSERVAR EL POSIBLE SOBREAJUSTE. VALORAR EN TEST LA CAPACIDAD PREDICTIVA DEL MODELO.
# (5) SELECCIONAR LAS ALTERNATIVAS QUE MÁS NOS INTERESEN POR SU BONDAD DE AJUSTE ESPECÍFICA.
# (6) MOSTRAR BOXPLOTS DE SU PERFORMANCE EN LAS DISTINTAS VALIDACIONES PARA VALORAR LA ROBUSTEZ Y TOMAR UNA DECISIÓN.
# (7) HACER UN INFORME DE LA PARAMETRIZACIÓN Y BONDAD DE AJUSTE DEL MODELO FINAL SELECCIONADO.

import os
os.chdir('/home/jerry/Documents/master/Master/Machine learning - PART III/Data')

file_path = 'arboles.csv'  # Reemplaza con la ruta correcta de tu archivo
file_path_2 = 'arboles.csv'
df = pd.read_csv(file_path_2)
print(df.head())
print(f'\nLa frecuencia de cada clase es: \n{df.chd.value_counts(normalize=True)}')

# Categorizar la variable de respuesta
df['chd'] = df['chd'].apply(lambda x: 'Yes' if x == 1 else 'No')
print(df.head())

print(df.isna().sum())
#es importante tratar de forma adecuada las variables categóricas. Se convierten en numéricas con la regla: one hot encoding.
df[['famhist']] = pd.get_dummies(df[['famhist']],drop_first=True)
# Separar las variables predictoras y la variable de respuesta.
X = df.drop('chd', axis=1)
y = df['chd']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)
# ES IMPORTANTE QUE LA DISTRIBUCIÓN DE LAS CLASES SEA 'SIMILAR' EN TRAIN Y TEST.
print(f'La frecuencia de cada clase en train es: \n{y_train.value_counts(normalize=True)}')
print(f'\nLa frecuencia de cada clase en test es: \n{y_test.value_counts(normalize=True)}')


print(df.head())

# Crear el árbol de decisión base. 
# OJO, estos no son los mejores parámetros; solo son ilustraciones para la comparación con bagging.
base_classifier = DecisionTreeClassifier(min_samples_split=10, criterion='gini', max_depth = 5, random_state = 123)
base_classifier.fit(X_train, y_train)
y_pred_base = base_classifier.predict(X_test)
# Evaluar el rendimiento del modelo
accuracy_a = accuracy_score(y_test, y_pred_base)
print(f'Precisión del árbol estándar: {accuracy_a}')

######################3###################################
# vamos a ver con un modelo en concreto
#######################################################
# n_estimators: Número de árboles en el bosque
# max_depth: Profundidad máxima de cada árbol
# min_samples_split: Número mínimo de muestras requeridas para dividir un nodo interno
# min_samples_leaf: Número mínimo de muestras requeridas para estar en un nodo hoja
# max_features: Número o proporción de características para ajustar cada árbol
# bootstrap: Si se deben realizar remuestreos con reemplazo (True) o sin reemplazo (False)
# n_jobs: Número de trabajadores para entrenar los árboles de forma paralela
# random_state: Semilla para reproducibilidad
RF_model = RandomForestClassifier(n_estimators = 60,bootstrap = True, max_depth = 20, min_samples_split=10, criterion='entropy',min_samples_leaf = 10,random_state=123)
RF_model.fit(X_train, y_train)
y_pred_rf = RF_model.predict(X_test)

# Evaluar el rendimiento del modelo
accuracy_rf = accuracy_score(y_test, y_pred_rf)
print(f'Precisión del modelo con RF estándar: {accuracy_rf}')

# Crear un gráfico de dispersión para comparar las predicciones
plt.figure(figsize=(10, 6))

plt.scatter(np.arange(len(y_test)), y_test, color='green', label='True Values', marker='o', s=100)
plt.scatter(np.arange(len(y_test)), y_pred_base, color='orange', label=f'Base Árbol Decisión (Acc: {accuracy_a:.2f})', marker='x', s=70)
plt.scatter(np.arange(len(y_test)), y_pred_rf, color='blue', label=f'Base Random Forest (Acc: {accuracy_rf:.2f})', marker='x', s=70)

plt.title('Predicciones RandomForest')
plt.xlabel('Índice de la Muestra')
plt.ylabel('Etiqueta de Clase')
plt.legend()
plt.show()

# se procede a observar el posible sobreajuste comparando predicciones en train y test.
# predicciones significativamente mayores en train que en test puede indicar sobreajuste.
# Predicciones en conjunto de entrenamiento y prueba
y_train_pred = RF_model.predict(X_train)
y_test_pred = RF_model.predict(X_test)
print(f'Se tiene un accuracy para train de: {accuracy_score(y_train,y_train_pred)}')
print(f'Se tiene un accuracy para test de: {accuracy_score(y_test,y_test_pred)}')
print('Nótese la diferencia en accuracy para ambos conjuntos de datos y el posible sobreajuste.')
## esto parece que tiene una difernecia notable, lo cual seguramnete hayaos tenido algo mal del modelo y habra q realziarlo de nuevo
## deberiamos de haber puesto menos sobreparametrizacion en train, no es q este mal el modelo pero indica q tenemos una señal de alarma y tenemos una parametrizacion distintas para mejroar el futuro

print(RF_model.get_params)

######################################################################## 
# Ahora lo vamos a hacer con grid para encontrar el mejor mdoelo
######################################################################

# Se puede seleccionar un grill extenso y meditado sobre los distintos parámetros con los que jugar.
params = {
    'n_estimators' : [50,100,150,200,250],
    'max_depth': [2, 3, 5, 10, 20],
    'bootstrap': [True, False],
    'min_samples_leaf' : [3,10,30],
    'min_samples_split': [5, 10, 20, 50, 100],
    'criterion': ["gini", "entropy"]
}

scoring_metrics = ['accuracy', 'precision_macro', 'recall_macro', 'f1_macro']
#recordar que arbol2 es el árbol cuyas VI son todas las variables.
# cv = crossvalidation
grid_search_RF = GridSearchCV(estimator=RF_model, 
                           param_grid=params, 
                           cv=4, scoring = scoring_metrics, refit='accuracy')
grid_search_RF.fit(X_train, y_train)

print('En el caso anterior, se observa que el parámetro max_depth tiene un valor de 20, indicador que de mayores valores\n pueden suponer mejora, por lo que modificar el grill puede ser indicado en ese parámetro. \nIgualmente puede ocurrir con min_samples_split, el cual, parece indicar la búsqueda \nde valores menores y más continuados, por ejemplo: [8,9,10,11,12]')

##3 obtenemos cual es el mejor modelo
# Obtener el mejor modelo
best_model_RF = grid_search_RF.best_estimator_
print(grid_search_RF.best_estimator_)
y_pred_rf = best_model_RF.predict(X_test)
accuracy_rf_gs = accuracy_score(y_test, y_pred_rf)
# Evaluar el rendimiento del modelo
print(f'Precisión del árbol estándar: {accuracy_rf_gs}')

# se procede a observar el posible sobreajuste comparando predicciones en train y test.
# predicciones significativamente mayores en train que en test puede indicar sobreajuste.
# Predicciones en conjunto de entrenamiento y prueba
y_train_pred = best_model_RF.predict(X_train)
y_test_pred = best_model_RF.predict(X_test)
print(f'Se tiene un accuracy para train de: {accuracy_score(y_train,y_train_pred)}')
print(f'Se tiene un accuracy para test de: {accuracy_score(y_test,y_test_pred)}')
print('Comprobar que la diferencia no sea muy grande por temas de sobreajuste')

# Obtener resultados del grid search
results = pd.DataFrame(grid_search_RF.cv_results_)
print(results.head())
print(results.columns)
# Ordenar el DataFrame por la métrica de interés (por ejemplo, accuracy)
sorted_results = results.sort_values(by='mean_test_accuracy', ascending=True).head(5)
print(sorted_results)

# se selecciona el modelo candidato, y se procede a analizar su robustez a lo largo de cross validation.
res_1 = sorted_results[['split0_test_accuracy', 'split1_test_accuracy','split2_test_accuracy', 'split3_test_accuracy']].iloc[0]
res_2 = sorted_results[['split0_test_accuracy', 'split1_test_accuracy','split2_test_accuracy', 'split3_test_accuracy']].iloc[1]
res_3 = sorted_results[['split0_test_accuracy', 'split1_test_accuracy','split2_test_accuracy', 'split3_test_accuracy']].iloc[2]
res_4 = sorted_results[['split0_test_accuracy', 'split1_test_accuracy','split2_test_accuracy', 'split3_test_accuracy']].iloc[3]
res_5 = sorted_results[['split0_test_accuracy', 'split1_test_accuracy','split2_test_accuracy', 'split3_test_accuracy']].iloc[4]

# Crear un boxplot para los cuatro valores de accuracy
plt.boxplot([res_1.values,res_2.values,res_3.values,res_4.values,res_5.values], labels = ['res_1','res_2','res_3','res_4','res_5'])
plt.title('Boxplots de Accuracy para los 4 Splits')
plt.xlabel('Splits de Cross Validation')
plt.ylabel('Accuracy')
plt.show()
# Nótese en la solución que boxplots con gran amplitud no son deseables, ya que se caracterizan por poca robustez de la solución
# seleccionemos el segundo modelo dada su mayor robustez con respecto al propuesto por GridSearch
# nótese que "**" es para desempaquetar una lista de valores.
random_f_2 = RandomForestClassifier(**sorted_results['params'].iloc[1],random_state=123)
random_f_2.fit(X_train, y_train)
res_rf_2 = random_f_2.predict(X_test)
print(accuracy_score(y_test,res_rf_2))

# Si se quiere conocer quién tiene mayor robustez en sensibilidad por cuestiones de criterio exógeno:
print(sorted_results[['std_test_recall_macro']])
print('Resultados para Modelo')
print(classification_report(y_test, res_rf_2))

#############################################################################
# vamos ahora con un ejemplo de regresion  (aqui las cajitas bajas son las buenas mientras que en el otro(clasificacion) lado las buenas son las cajitas altas)
######################################################################



file_path = 'compress.csv'  # Reemplaza con la ruta correcta de tu archivo
file_path_3 = 'compress.csv'  # Reemplaza con la ruta correcta de tu archivo

compress = pd.read_csv(file_path_3)
compress.head()

# Separar las variables predictoras y la variable de respuesta.
X_c = compress.drop('cstrength', axis=1)
y_c = compress['cstrength']

RF_R = RandomForestRegressor(n_estimators = 60,bootstrap = True, max_depth = 20, min_samples_split=10, criterion='absolute_error',min_samples_leaf = 10,random_state=123)
# Crear un conjunto de entrenamiento y uno de prueba
X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X_c, y_c, test_size=0.2, random_state=123)
# Construir el modelo de árbol de decisiones
RF_R.fit(X_train_c, y_train_c)
#se valora el posible sobreajuste
pred_rf_c_train = RF_R.predict(X_train_c)
pred_rf_c_test = RF_R.predict(X_test_c)
print(f'MAE del modelo en train:{mean_absolute_error(y_train_c,pred_rf_c_train)}')
print(f'MAE del modelo en test:{mean_absolute_error(y_test_c,pred_rf_c)}')
# En caso de necesitar probar diferentes parametrizaciones. En este caso, iremos directamente a la validación cruzada.
params_c = {
    'max_depth': [2, 3, 5, 10, 20],
    'min_samples_split': [5, 10, 20, 50, 100],
    'criterion': ['squared_error', 'friedman_mse', 'absolute_error', 'poisson']
}
# Definir las métricas de evaluación que deseas utilizar

print(RF_R.get_params())
scoring_metrics_c = {
    'MAE': make_scorer(mean_absolute_error),
    'MSE': make_scorer(mean_squared_error)
}
# los parámetros necesitan presentar formato lista.
params = {
    'bootstrap': [True], 
    'criterion': ['absolute_error'], 
    'max_depth': [20], 
    'max_features': [1.0], 
    'min_samples_leaf': [10], 
    'min_samples_split': [10],
    'n_estimators': [60],
    'random_state': [123]
}
grid_search_rf_c = GridSearchCV(estimator=RF_R, 
                           param_grid=params, 
                           cv=4, scoring = scoring_metrics_c, refit='MAE')
grid_search_rf_c.fit(X_train_c, y_train_c)

pd.DataFrame(grid_search_c.cv_results_)

res_1 = pd.DataFrame(grid_search_c.cv_results_)[['split0_test_MAE', 'split1_test_MAE','split2_test_MAE','split3_test_MAE']].iloc[0]
print(res_1)
# Crear un boxplot para los cuatro valores de accuracy
plt.boxplot([res_1.values], labels = ['res_1'])
plt.title('Boxplots de la robustez en MAE')
plt.xlabel('Splits de Cross Validation')
plt.ylabel('MAE')
plt.show()

indices = np.arange(1, len(y_test_c) + 1)

plt.figure(figsize=(8, 6))
plt.scatter(indices, y_test_c, color='darkgreen', label='reales')  # Puedes ajustar el color según tus preferencias

plt.scatter(indices, pred_rf_c_test, color='red', alpha=0.5, label='Random Forest')  # Puedes ajustar el color y la transparencia según tus preferencias

plt.title('Scatter Plot de valores reales vs ranfom forest')
plt.xlabel('Observaciones')
plt.ylabel('Valores')
plt.legend()  # Agregar leyenda
plt.grid(True)
plt.show()

# Calcular diferentes medidas de bondad de ajuste
mae = mean_absolute_error(y_test_c, pred_rf_c_test)
mse = mean_squared_error(y_test_c, pred_rf_c_test)
rmse = np.sqrt(mse)
r2 = r2_score(y_test_c, pred_rf_c_test)

# Imprimir las métricas
print(f'MAE (Error Absoluto Medio): {mae:.2f}')
print(f'MSE (Error Cuadrático Medio): {mse:.2f}')
print(f'RMSE (Raíz del Error Cuadrático Medio): {rmse:.2f}')
print(f'R2: {r2}')