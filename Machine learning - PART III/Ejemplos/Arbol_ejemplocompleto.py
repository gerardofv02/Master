###########3 EJEMPLO  (siguiende el ejemplo 2)


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree
import seaborn as sns
from sklearn.tree import DecisionTreeClassifier, export_text, DecisionTreeRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, roc_curve, auc
from sklearn.metrics import make_scorer, mean_absolute_error, mean_squared_error, r2_score

import os
os.chdir('/home/jerry/Documents/master/Master/Machine learning - PART III/Data')

file_path = 'arboles.csv'  # Reemplaza con la ruta correcta de tu archivo

df = pd.read_csv(file_path)
print(df.head()) 
print(f'\nLa frecuencia de cada clase es: \n{df.chd.value_counts()}')

# Se observa si se tiene algún valor perdido.
print(df.isna().sum()) ## no tiene

# Categorizar la variable de respuesta
df['chd'] = df['chd'].apply(lambda x: 'Yes' if x == 1 else 'No')
print(df.head())
# Separar las variables predictoras y la variable de respuesta.
X = df[['tobacco']]
y = df['chd']

## PARAMETROS PARA ELEGIR PARA CREAR EL ARBOL:
# min_sample_split: el número mínimo de casos que contiene una hoja para que pueda ser creada.
# criterion: Criterio de división: “gini”, “entropy”, “log_loss”.
# max_depth = Profundidad máxima del árbol. En caso de no especificar, el clasificador sigue segmentando hasta que
# las hojas son puras, o se alcanza el min_sample_split. Con caracter ilustrativo, se selecciona bajo.
arbol1 = DecisionTreeClassifier(min_samples_split=30, criterion='gini', max_depth = 2)
# Crear un conjunto de entrenamiento y uno de prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Se vuelve a entrenar el árbol con más variables. No necesariamente tiene que utilizar todas, por lo que es importante
# conocer la importancia predictiva de cada variable en el modelo.

#es importante tratar de forma adecuada las variables categóricas. Se convierten en numéricas con la regla: one hot encoding.
df[['famhist']] = pd.get_dummies(df[['famhist']],drop_first=True)
# Separar las variables predictoras y la variable de respuesta.
X = df.drop('chd', axis=1)
y = df['chd']
#Se selecciona profundidad 4 sólo con caracter ilustrativo, al simplificar el árbol.
arbol2 = DecisionTreeClassifier(min_samples_split=30, criterion='gini', max_depth = 4)
# Crear un conjunto de entrenamiento y uno de prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# Construir el modelo de árbol de decisiones
arbol2.fit(X_train, y_train)

# Se estudia la importancia - o valor predictivo - de cada variable en el modelo.
print(pd.DataFrame({'nombre': arbol2.feature_names_in_, 'importancia': arbol2.feature_importances_}))

## vemos la importancia de las variables graficamente
# Ordenar el DataFrame por importancia en orden descendente
df_importancia = pd.DataFrame({'Variable': arbol2.feature_names_in_, 'Importancia': arbol2.feature_importances_}).sort_values(by='Importancia', ascending=False)

# Crear un gráfico de barras
plt.bar(df_importancia['Variable'], df_importancia['Importancia'], color='skyblue')
plt.xlabel('Variable')
plt.ylabel('Importancia')
plt.title('Importancia de las características')
plt.xticks(rotation=45, ha='right')  # Rotar los nombres en el eje x para mayor legibilidad
plt.tight_layout()

# Mostrar el gráfico
plt.show()

plt.figure(figsize=(15, 15))
plot_tree(arbol2, feature_names=X.columns.tolist(), class_names=['No', 'Yes'], filled=True,
         proportion = True)
plt.show()
file_path = 'compress.csv'  # Reemplaza con la ruta correcta de tu archivo

compress = pd.read_csv(file_path)
print(compress.head())

print(compress.isna().sum())

# Separar las variables predictoras y la variable de respuesta.
X_c = compress.drop('cstrength', axis=1)
y_c = compress['cstrength']
# criterion: Criterio de división: “squared_error”, “friedman_mse”, “absolute_error”, “poisson”}, default=”squared_error”.
# Se selecciona squared error con motivos ilustrativos. Es equivalente a la reducción de varianza.
# A priori, con motivos ilustrativos, se mantiene min_sample_split y max_depth en estos valores para facilitar la visualización del árbol.
# Recordar que estos son parámetros a modificar para encontrar el modelo óptimo.
# cpp_alpha es el parámetro de complejidad, el cual establece “penalizaciones” si se producen muchas divisiones. Cuanto más alto
# más pequeño será el árbol.
# criterios elegidos disitntos ya que no podemos coger o gini,...
arbol3 = DecisionTreeRegressor(min_samples_split=30, criterion='squared_error', max_depth = 4, ccp_alpha = 0.01)
# Crear un conjunto de entrenamiento y uno de prueba
X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X_c, y_c, test_size=0.2, random_state=42)
# Construir el modelo de árbol de decisiones
arbol3.fit(X_train_c, y_train_c)


print(pd.DataFrame({'nombre': arbol3.feature_names_in_, 'importancia': arbol3.feature_importances_}))

# Ordenar el DataFrame por importancia en orden descendente
df_importancia_c = pd.DataFrame({'Variable': arbol3.feature_names_in_, 'Importancia': arbol3.feature_importances_}).sort_values(by='Importancia', ascending=False)
# Crear un gráfico de barras
plt.bar(df_importancia_c['Variable'], df_importancia_c['Importancia'], color='skyblue')
plt.xlabel('Variable')
plt.ylabel('Importancia')
plt.title('Importancia de las características')
plt.xticks(rotation=45, ha='right')  # Rotar los nombres en el eje x para mayor legibilidad
plt.tight_layout()

# Mostrar el gráfico
plt.show()

plt.figure(figsize=(20, 15))
plot_tree(arbol3, feature_names=X_c.columns.tolist(), filled=True,
         proportion = True)
plt.show()

## en este ejemplo que hemos generado, se ha generado uin arbol mas grande debido a que hay mas cantidad de nodos y mas cantidad  de variables que usamos. Pero esta claro que hemos overextendido ya que vemos nodos en los q hya muy pocas muestras (0.8% por ejemplo)    
## aqui hay overfitting y habria qu hacer poda o cambiar las variables de entrada para que uedara mejor

## tuneo y evaluación predictiva del modelo para variable dependiente categórica.

params = {
    'max_depth': [2, 3, 5, 10, 20],
    'min_samples_split': [5, 10, 20, 50, 100],
    'criterion': ["gini", "entropy"]
}
scoring_metrics = ['accuracy', 'precision_macro', 'recall_macro', 'f1_macro']
#recordar que arbol2 es el árbol cuyas VI son todas las variables.
# cv = crossvalidation
grid_search = GridSearchCV(estimator=arbol2, 
                           param_grid=params, 
                           cv=4, scoring = scoring_metrics, refit='accuracy')
grid_search.fit(X_train, y_train)

# Obtener resultados del grid search
results = pd.DataFrame(grid_search.cv_results_)

# Mostrar resultados
print("Resultados de Grid Search:")
print(results[['params', 'mean_test_accuracy', 'mean_test_precision_macro', 'mean_test_recall_macro', 'mean_test_f1_macro']])

# Obtener el mejor modelo
best_model = grid_search.best_estimator_
print(grid_search.best_estimator_)
## si la profundidad vemos q ha salido el 3, pero no hemos probado el 4, se tendria q probar el 4. Al igual que si el split es de 100 y es el maximo q he puesto, habira q tirar mas para ir probando cual es el mejor model

print(results.columns)

# Para seleccionar una parametrización específica y la mejor de acuerdo con el criterio
# de GridSearch, acceder a esta y conocer su combinación.
results.iloc[8].params

# se selecciona el modelo candidato, y se procede a analizar su robustez a lo largo de cross validation.
res_1 = results[['split0_test_accuracy', 'split1_test_accuracy','split2_test_accuracy', 'split3_test_accuracy']].iloc[2]
res_2 = results[['split0_test_accuracy', 'split1_test_accuracy','split2_test_accuracy', 'split3_test_accuracy']].iloc[4]
res_3 = results[['split0_test_accuracy', 'split1_test_accuracy','split2_test_accuracy', 'split3_test_accuracy']].iloc[18]

print(res_1.values)

# Crear un boxplot para los cuatro valores de accuracy
plt.boxplot([res_1.values,res_2.values,res_3.values], label = ['res_1','res_2','res_3'])
plt.title('Boxplots de Accuracy para los 4 Splits')
plt.xlabel('Splits de Cross Validation')
plt.ylabel('Accuracy')
plt.show()
# Nótese en la solución que boxplots con gran amplitud no son deseables, ya que se caracterizan por poca robustez de la solución

##una vez decidio cual es mi mejor modelo segun todas las caracteristicas:  tenemos q volver a ejecutar el modelo para calcular als predicciones de netrenamiento y validacion
# Obtener el mejor modelo
best_model = grid_search.best_estimator_

# Ajustar el mejor modelo con todo el conjunto de entrenamiento
best_model.fit(X_train, y_train)

# Predicciones en conjunto de entrenamiento y prueba
y_train_pred = best_model.predict(X_train)
y_test_pred = best_model.predict(X_test)

## sacamos a matriz de confusion:
#medidas de bondad de ajuste en train

conf_matrix = confusion_matrix(y_train, y_train_pred)
print("Matriz de Confusión:")
print(conf_matrix)
print("\nMedidas de Desempeño:")
print(classification_report(y_train, y_train_pred))

y_train_auc = pd.get_dummies(y_train,drop_first=True)
# Calcular el área bajo la curva ROC (AUC)
y_prob_train = best_model.predict_proba(X_train)[:, 1]

fpr, tpr, thresholds = roc_curve(y_train_auc, y_prob_train)
roc_auc = auc(fpr, tpr)
print(f"\nÁrea bajo la curva ROC (AUC): {roc_auc:.2f}")
# Graficar la curva ROC
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'AUC = {roc_auc:.2f}')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlabel('Tasa de Falsos Positivos (FPR)')
plt.ylabel('Tasa de Verdaderos Positivos (TPR)')
plt.title('Curva ROC')
plt.legend(loc="lower right")
plt.show()

## obtenemos la curva roc: representa como se comporta entre snesibilidad y msensibilidad. cuandto mayor valor mejor lo ahce, cuanto menor valor, peor lo hace

#3 hacemos lo mismo para los datos de test:
# medidas de bondad de ajuste en test

conf_matrix = confusion_matrix(y_test, y_test_pred)
print("Matriz de Confusión:")
print(conf_matrix)
print("\nMedidas de Desempeño:")
print(classification_report(y_test, y_test_pred))

## no son valores muy diferenciados con loq  cual no parece que la diferencia sea muy grande

y_test_auc = pd.get_dummies(y_test,drop_first=True)
# Calcular el área bajo la curva ROC (AUC)
y_prob_test = best_model.predict_proba(X_test)[:, 1]

fpr, tpr, thresholds = roc_curve(y_test_auc, y_prob_test)
roc_auc_test = auc(fpr, tpr)
print(f"\nÁrea bajo la curva ROC (AUC): {roc_auc:.2f}")

# Graficar la curva ROC
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'AUC = {roc_auc:.2f}')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlabel('Tasa de Falsos Positivos (FPR)')
plt.ylabel('Tasa de Verdaderos Positivos (TPR)')
plt.title('Curva ROC')
plt.legend(loc="lower right")
plt.show()

## hacemos el modelo
plt.figure(figsize=(20, 15))
plot_tree(best_model, feature_names=X.columns.tolist(), filled=True,
         proportion = True)
plt.show()

###################################################################################
# ahora vemos con variables continuas
################################################################################
## en caso de variables continua, hace exactamente lo mismo. solo se tienen q cambiar los valores de criterios y como se hacen pero los passo son los mismos

## tuneo y evaluación predictiva del modelo para variable dependiente numérica.

params_c = {
    'max_depth': [2, 3, 5, 10, 20],
    'min_samples_split': [5, 10, 20, 50, 100],
    'criterion': ['squared_error', 'friedman_mse', 'absolute_error', 'poisson']
}
# Definir las métricas de evaluación que deseas utilizar
scoring_metrics_c = {
    'MAE': make_scorer(mean_absolute_error),
    'MSE': make_scorer(mean_squared_error),
    'RMSE': make_scorer(lambda y_true, y_pred: mean_squared_error(y_true, y_pred, squared=False))
}
# cv = crossvalidation
grid_search_c = GridSearchCV(estimator=arbol3, 
                           param_grid=params_c, 
                           cv=4, scoring = scoring_metrics_c, refit='MSE')
grid_search_c.fit(X_train_c, y_train_c)

# Obtener resultados del grid search
results_c = pd.DataFrame(grid_search_c.cv_results_)

# Mostrar resultados
print("Resultados de Grid Search:")
print(results_c)

# Obtener el mejor modelo
best_model_c = grid_search_c.best_estimator_
print(grid_search_c.best_estimator_)

# Ajustar el mejor modelo con todo el conjunto de entrenamiento
best_model_c.fit(X_train_c, y_train_c)

# Predicciones en conjunto de entrenamiento y prueba
y_train_pred_c = best_model_c.predict(X_train_c)
y_test_pred_c = best_model_c.predict(X_test_c)

# Medidas de bondad de ajuste en train
y_pred_train_c = best_model_c.predict(X_train_c)
# Suponiendo que tienes los valores reales en y_test_c y las predicciones en y_pred_test_c
errores = y_train_c - y_pred_train_c

# Convertir los errores a un DataFrame
errores_df = pd.DataFrame({'Errores': errores})
# Box Plot de los errores en el conjunto de prueba
sns.boxplot(errores_df)
plt.title('Box Plot de Errores en el Conjunto de Prueba')
plt.show()


# Calcular diferentes medidas de bondad de ajuste
mae = mean_absolute_error(y_train_c, y_pred_train_c)
mse = mean_squared_error(y_train_c, y_pred_train_c)
rmse = np.sqrt(mse)
r2 = r2_score(y_train_c, y_pred_train_c)

# Imprimir las métricas
print(f'MAE (Error Absoluto Medio): {mae:.2f}')
print(f'MSE (Error Cuadrático Medio): {mse:.2f}')
print(f'RMSE (Raíz del Error Cuadrático Medio): {rmse:.2f}')
print(f'R²: {r2:.2f}')

# Medidas de bondad de ajuste en test:

# Medidas de bondad de ajuste en train
y_pred_test_c = best_model_c.predict(X_test_c)
# Suponiendo que tienes los valores reales en y_test_c y las predicciones en y_pred_test_c
errores = y_test_c - y_pred_test_c

# Convertir los errores a un DataFrame
errores_df = pd.DataFrame({'Errores': errores})
# Box Plot de los errores en el conjunto de prueba
sns.boxplot(errores_df)
plt.title('Box Plot de Errores en el Conjunto de Prueba')
plt.show()

mae = mean_absolute_error(y_test_c, y_pred_test_c)
mse = mean_squared_error(y_test_c, y_pred_test_c)
rmse = np.sqrt(mse)
r2 = r2_score(y_test_c, y_pred_test_c)

# Imprimir las métricas
print(f'MAE (Error Absoluto Medio): {mae:.2f}')
print(f'MSE (Error Cuadrático Medio): {mse:.2f}')
print(f'RMSE (Raíz del Error Cuadrático Medio): {rmse:.2f}')
print(f'R²: {r2:.2f}')

plt.figure(figsize=(20, 15))
plot_tree(best_model_c, feature_names=X_c.columns.tolist(), filled=True,
         proportion = True)
plt.show()