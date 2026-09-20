## vamos a crear un ejemplo de arboles con bagging

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import BaggingClassifier, RandomForestClassifier, BaggingRegressor
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
df = pd.read_csv(file_path)
print(df.head())
print(f'\nLa frecuencia de cada clase es: \n{df.chd.value_counts(normalize=True)}')

# Categorizar la variable de respuesta
df['chd'] = df['chd'].apply(lambda x: 'Yes' if x == 1 else 'No')
print(df.head())

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

# Crear el modelo de Bagging
# n_estimators int, default=10: Número de modelos a aplicar.
# max_samples int or float, default=1.0: número de valores máximos a extraer para cada modelo. puede ser con numero literal o %
# max_features int or float, default=1.0: número de variables a utilizar para cada modelo.
# boostrap bool, default=True: con o sin reemplazo aplicado a las observaciones.
# bootstrap_features bool, default=False: con o sin reemplazo aplicado a las variables.
# oob_score bool, default=False: Out of Bag. model.oob_score_ devuelve un error medio 
# cometido en los casos fuera de la bolsa. Para todos los errores: 
# model.oob_decision_function_
import sklearn
sklearn.set_config(enable_metadata_routing=True)
bagging_model = BaggingClassifier(base_classifier, max_samples = 300, max_features = 9,n_estimators=10, random_state=123, oob_score = True) 
bagging_model.fit(X_train, y_train)
y_pred_bagging = bagging_model.predict(X_test)

# Evaluar el rendimiento del modelo
accuracy_b = accuracy_score(y_test, y_pred_bagging)
print(f'Precisión del modelo con Bagging estándar: {accuracy_b}')
print(f'Se observa una diferencia del modelo baggin con respecto al árbol de decisión de: \n{accuracy_b-accuracy_a}')

# Crear un gráfico de dispersión para comparar las predicciones
plt.figure(figsize=(10, 6))

plt.scatter(np.arange(len(y_test)), y_test, color='green', label='True Values', marker='o', s=100)
plt.scatter(np.arange(len(y_test)), y_pred_base, color='blue', label=f'Base Decision Tree (Acc: {accuracy_a:.2f})', marker='x', s=70)
plt.scatter(np.arange(len(y_test)), y_pred_bagging, color='red', label=f'Bagging (Acc: {accuracy_b:.2f})', marker='^', s=70)

plt.title('Comparación de Predicciones entre Árbol Base y Bagging')
plt.xlabel('Índice de la Muestra')
plt.ylabel('Etiqueta de Clase')
plt.legend()
plt.show()

# se procede a observar el posible sobreajuste comparando predicciones en train y test.
# predicciones significativamente mayores en train que en test puede indicar sobreajuste.
# Predicciones en conjunto de entrenamiento y prueba
y_train_pred = bagging_model.predict(X_train)
y_test_pred = bagging_model.predict(X_test)
print(f'Se tiene un accuracy para train de: {accuracy_score(y_train,y_train_pred)}')
print(f'Se tiene un accuracy para test de: {accuracy_score(y_test,y_test_pred)}')
print('Nótese la diferencia en accuracy para ambos conjuntos de datos y el posible sobreajuste. \nEsto puede deberse al modelo base seleccionado')

## tuneo y evaluación predictiva del modelo para variable dependiente categórica.
params = {
    'max_depth': [2, 3, 5, 10, 20],
    'min_samples_split': [5, 10, 20, 50, 100],
    'criterion': ["gini", "entropy"]
}
scoring_metrics = ['accuracy', 'precision_macro', 'recall_macro', 'f1_macro']
#recordar que arbol2 es el árbol cuyas VI son todas las variables.
# cv = crossvalidation
grid_search_tree = GridSearchCV(estimator=base_classifier, 
                           param_grid=params, 
                           cv=4, scoring = scoring_metrics, refit='accuracy')
grid_search_tree.fit(X_train, y_train)
# Obtener el mejor modelo
best_model_tree = grid_search_tree.best_estimator_
print(grid_search_tree.best_estimator_)
y_pred_base = best_model_tree.predict(X_test)
accuracy_t = accuracy_score(y_test, y_pred_base)
# Evaluar el rendimiento del modelo
print(f'Precisión del árbol estándar: {accuracy_t}')

# modelo ejemplo de bagging, sin buscar sus mejores parámetros, teniendo en cuenta todas las variables y 400 estimators
bagging_model = BaggingClassifier(best_model_tree, max_features = 9,n_estimators=400, random_state=123, oob_score = True)
bagging_model.fit(X_train, y_train)
y_pred_bagging = bagging_model.predict(X_test)

# Evaluar el rendimiento del modelo
accuracy_b = accuracy_score(y_test, y_pred_bagging)
print(f'Precisión del modelo con Bagging estándar: {accuracy_b}')
print(f'Se observa una diferencia del modelo baggin con respecto al árbol de decisión de: \n {accuracy_b-accuracy_t}')

# Definir el espacio de búsqueda de parámetros
param_grid = {
    'n_estimators': [10, 50, 100,250],
    'max_samples': [1,75,150,300],
    'max_features': [1,4,7,9],
    'bootstrap': [True, False],
    'bootstrap_features': [True, False]
}
scoring_metrics = ['accuracy', 'precision_macro', 'recall_macro', 'f1_macro']

import warnings
warnings.filterwarnings("ignore")
# Configurar la búsqueda de parámetros con validación cruzada
# Nótese que el gridsearch y param_grid se está haciendo con el modelo bagging, y no con el base, el cuál también se pueden
# modificar sus parámetros.
grid_search_b = GridSearchCV(bagging_model, param_grid, cv=5, scoring='accuracy')

# Realizar la búsqueda en la cuadrícula utilizando los datos
grid_search_b.fit(X_train, y_train)

# Obtener los mejores parámetros y la mejor puntuación
best_params = grid_search_b.best_params_
best_score = grid_search_b.best_score_

print(f'Mejores parámetros: {best_params}')
# Obtener el mejor modelo
best_model_bagging = grid_search_b.best_estimator_
y_pred_best_bagging = best_model_bagging.predict(X_test)

# Evaluar el rendimiento del modelo
accuracy_b_b = accuracy_score(y_test, y_pred_best_bagging)
print(f'Precisión del modelo con Bagging CV y best_params: {accuracy_b_b}')

# se procede a observar el posible sobreajuste comparando predicciones en train y test.
# predicciones significativamente mayores en train que en test puede indicar sobreajuste.
# Predicciones en conjunto de entrenamiento y prueba
y_train_pred = best_model_bagging.predict(X_train)
y_test_pred = best_model_bagging.predict(X_test)
print(f'Se tiene un accuracy para train de: {accuracy_score(y_train,y_train_pred)}')
print(f'Se tiene un accuracy para test de: {accuracy_score(y_test,y_test_pred)}')
print('Nótese que ya no encontramos problemas aparentes de sobreajuste')
model_names = ['árbol', 'Bagging', 'Bagging: CV \n SearchGrid']
scores = [accuracy_a, accuracy_b, accuracy_b_b]
# Crear el diagrama de barras
plt.figure(figsize=(5, 3))
bars = plt.bar(np.arange(len(model_names)), scores, color=['lightblue', 'orange', 'darkred'])
plt.xticks(np.arange(len(model_names)), model_names, rotation=45, ha='right')
plt.ylim(0, 1.0)  # Ajustar el rango del eje y según tus necesidades
plt.title('Puntuaciones de Modelos')
plt.xlabel('Modelos')
plt.ylabel('Precisión')

# Añadir los valores encima de las barras centrados
for bar, score in zip(bars, scores):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01, f'{score:.2f}', ha='center', color='black')

plt.show()

# Crear un gráfico de dispersión para comparar las predicciones
plt.figure(figsize=(7, 5))

plt.scatter(np.arange(len(y_test)), y_test, color='green', label='True Values', marker='o', s=100)
plt.scatter(np.arange(len(y_test)), y_pred_base, color='blue', label=f'Base Decision Tree (Acc: {accuracy_a:.2f})', marker='x', s=70)
plt.scatter(np.arange(len(y_test)), y_pred_bagging, color='red', label=f'Bagging (Acc: {accuracy_b:.2f})', marker='^', s=70)
plt.scatter(np.arange(len(y_test)), y_pred_best_bagging, color='orange', label=f'Bagging: CV/GS (Acc: {accuracy_b_b:.2f})', marker='x', s=70)
plt.title('Comparación de Predicciones entre Árbol Base, Bagging y Bagging CV-GridSearch')
plt.xlabel('Índice de la Muestra')
plt.ylabel('Etiqueta de Clase')
plt.legend()
plt.show()

# Crear el gráfico del error OOB
plt.figure(figsize=(10, 6))
plt.plot(np.arange(1, len(best_model_bagging.oob_decision_function_) + 1), best_model_bagging.oob_decision_function_, marker='o', linestyle='-', color='blue')
plt.title('Error OOB a medida que avanzan las iteraciones')
plt.xlabel('Número de iteraciones')
plt.ylabel('Error OOB')
plt.show()

# Obtener resultados del grid search
results = pd.DataFrame(grid_search_b.cv_results_)
results.head()

# Ordenar el DataFrame por la métrica de interés (por ejemplo, accuracy)
sorted_results = results.sort_values(by='rank_test_score', ascending=True).head(5)
print(sorted_results)

# se selecciona el modelo candidato, y se procede a analizar su robustez a lo largo de cross validation.
res_1 = sorted_results[['split0_test_score', 'split1_test_score','split2_test_score', 'split3_test_score']].iloc[0]
res_2 = sorted_results[['split0_test_score', 'split1_test_score','split2_test_score', 'split3_test_score']].iloc[1]
res_3 = sorted_results[['split0_test_score', 'split1_test_score','split2_test_score', 'split3_test_score']].iloc[2]
res_4 = sorted_results[['split0_test_score', 'split1_test_score','split2_test_score', 'split3_test_score']].iloc[3]
res_5 = sorted_results[['split0_test_score', 'split1_test_score','split2_test_score', 'split3_test_score']].iloc[4]

# Crear un boxplot para los cuatro valores de accuracy
plt.boxplot([res_1.values,res_2.values,res_3.values,res_4.values,res_5.values], label = ['res_1','res_2','res_3','res_4','res_5'])
plt.title('Boxplots de Accuracy para los 4 Splits')
plt.xlabel('Splits de Cross Validation')
plt.ylabel('Accuracy')
plt.show()
# Nótese en la solución que boxplots con gran amplitud no son deseables, ya que se caracterizan por poca robustez de la solución

print(sorted_results['params'].iloc[0])

# nótese que "**" es para desempaquetar una lista de valores.
bagging_0 = BaggingClassifier(best_model_tree,**sorted_results['params'].iloc[0],random_state=123)
bagging_0.fit(X_train, y_train)
res_0 = bagging_0.predict(X_test)

bagging_1 = BaggingClassifier(best_model_tree,**sorted_results['params'].iloc[1],random_state=123)
bagging_1.fit(X_train, y_train)
res_1 = bagging_1.predict(X_test)

bagging_2 = BaggingClassifier(best_model_tree,**sorted_results['params'].iloc[2],random_state=123)
bagging_2.fit(X_train, y_train)
res_2 = bagging_2.predict(X_test)

bagging_3 = BaggingClassifier(best_model_tree,**sorted_results['params'].iloc[3],random_state=123)
bagging_3.fit(X_train, y_train)
res_3 = bagging_3.predict(X_test)

bagging_4 = BaggingClassifier(best_model_tree,**sorted_results['params'].iloc[4],random_state=123)
bagging_4.fit(X_train, y_train)
res_4 = bagging_4.predict(X_test)
accuracy_score(y_test,res_0)

# A continuación, se observa, igualmente, las matrices de confusión para determinar - en caso de que haya una preferencia - si se busca 
# más sensibilidad o especificidad (en ámbitos como en el de la salud, esto es crucial)
print('Resultados para Modelo 0')
print(classification_report(y_test, res_0))
print('Resultados para Modelo 1')
print(classification_report(y_test, res_1))
print('Resultados para Modelo 2')
print(classification_report(y_test, res_2))
print('Resultados para Modelo 3')
print(classification_report(y_test, res_3))
print('Resultados para Modelo 4')
print(classification_report(y_test, res_4))
print('\nEn este caso, el modelo seleccionado como "best_estimator", no sólo \nes el que presenta mejor puntuación media, sino también mejor balance medio')

model_names = ['Modelo_0', 'Modelo_1', 'Modelo_2', 'Modelo_3','Modelo_4']
scores = [accuracy_score(y_test,res_0), accuracy_score(y_test,res_1), accuracy_score(y_test,res_2),accuracy_score(y_test,res_3),accuracy_score(y_test,res_4)]
# Crear el diagrama de barras
plt.figure(figsize=(5, 3))
bars = plt.bar(np.arange(len(model_names)), scores, color=['lightblue', 'orange', 'darkred','red','yellow'])
plt.xticks(np.arange(len(model_names)), model_names, rotation=45, ha='right')
plt.ylim(0, 1.0)  # Ajustar el rango del eje y según tus necesidades
plt.title('Puntuaciones de Modelos')
plt.xlabel('Modelos')
plt.ylabel('Precisión')

# Añadir los valores encima de las barras centrados
for bar, score in zip(bars, scores):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01, f'{score:.2f}', ha='center', color='black')

plt.show()
print('Recuérdese no valorar únicamente estas puntuaciones, sino también los boxplots.\nEn ocasiones puede ser mejor sacrificar algo de precisión por mayor sensibilidad, o especificidad')