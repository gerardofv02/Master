import os
os.chdir('/home/jerry/Documents/master/Master/Machine learning - PART III/Data')

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import GradientBoostingClassifier,GradientBoostingRegressor
from sklearn.tree import plot_tree
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, roc_curve, auc
from sklearn.metrics import make_scorer, mean_absolute_error, mean_squared_error, r2_score
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns  

file_path = 'arboles.csv'  # Reemplaza con la ruta correcta de tu archivo
file_path_2 = 'arboles.csv'
file_path_3 = 'arboles.csv'
df = pd.read_csv(file_path_3)
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

# loss: {‘log_loss’, ‘exponential’}, default=’log_loss’ Función de pérdida para optimizar.
# learning_rate: float, default=0.1 Parámetro shrink de ratio de aprendizaje.
# n_estimators: int, default=100
# Subsample: float, default=1.0 Proporción de la muestra para entrenar cada uno de los modelos base.
# Criterion: {‘friedman_mse’, ‘squared_error’}, default=’friedman_mse’
# random_state
# warm_startbool, default=False
# validation_fraction: Proporción de training para validación en early stopping.
# n_iter_no_change: Número de iteracones en la que parar si no se encuentran mejoras en la función de validación.
# tol: Parámetro para la tolerancia al earlystopping. Entre 0 e inf. Cuando la función de pérdida no mejora en n_iter_no_change, se para.
# ccp_Alpha: Parámetro de complejidad

# NOTA: pruébese a no utilizar n_iter_no_change y comprobar la diferencia en accuracy.

gb_classifier = GradientBoostingClassifier(n_estimators = 450, subsample = 1, random_state = 123,n_iter_no_change = 10)
gb_classifier.fit(X_train, y_train)
y_pred_base = gb_classifier.predict(X_test)
# Evaluar el rendimiento del modelo
accuracy_a = accuracy_score(y_test, y_pred_base)
print(f'Precisión de gradient boosting: {accuracy_a}')

# se procede a observar el posible sobreajuste comparando predicciones en train y test.
# predicciones significativamente mayores en train que en test puede indicar sobreajuste.
# Predicciones en conjunto de entrenamiento y prueba
y_train_pred = gb_classifier.predict(X_train)
y_test_pred = gb_classifier.predict(X_test)
print(f'Se tiene un accuracy para train de: {accuracy_score(y_train,y_train_pred)}')
print(f'Se tiene un accuracy para test de: {accuracy_score(y_test,y_test_pred)}')
print('Nótese la diferencia en accuracy para ambos conjuntos de datos y el posible sobreajuste.')

# Se puede seleccionar un grill extenso y meditado sobre los distintos parámetros con los que jugar.
#params = {
#    'loss': ["log_loss", "exponential"],
#    'n_estimators': [200,400,600],
#    'n_iter_no_change': [None,5,10,20],
#    'criterion': ["friedman_mse", "squared_error"],
#    'max_depth': [2, 3, 5, 10, 20],
#    'min_samples_leaf' : [3,10,30],
#    'min_samples_split': [5, 10, 50, 100],
#}
params = {
    'n_estimators': [400,600],
    'n_iter_no_change': [None,5,10],
    'max_depth': [5, 10],
    'min_samples_leaf' : [30],
    'min_samples_split': [5, 10, 50],
}

scoring_metrics = ['accuracy', 'precision_macro', 'recall_macro', 'f1_macro']
#recordar que arbol2 es el árbol cuyas VI son todas las variables.
# cv = crossvalidation
grid_search_GB = GridSearchCV(estimator=gb_classifier, 
                           param_grid=params, 
                           cv=4, scoring = scoring_metrics, refit='accuracy')
grid_search_GB.fit(X_train, y_train)

print(grid_search_GB.best_estimator_.get_params)

# Obtener resultados del grid search
results = pd.DataFrame(grid_search_GB.cv_results_)
print(results.head())

# Ordenar el DataFrame por la métrica de interés (por ejemplo, accuracy)
sorted_results = results.sort_values(by='mean_test_accuracy', ascending=True).head(5)
# se selecciona el modelo candidato, y se procede a analizar su robustez a lo largo de cross validation.
res_1 = sorted_results[['split0_test_accuracy', 'split1_test_accuracy','split2_test_accuracy', 'split3_test_accuracy']].iloc[0]
res_2 = sorted_results[['split0_test_accuracy', 'split1_test_accuracy','split2_test_accuracy', 'split3_test_accuracy']].iloc[1]
res_3 = sorted_results[['split0_test_accuracy', 'split1_test_accuracy','split2_test_accuracy', 'split3_test_accuracy']].iloc[2]
res_4 = sorted_results[['split0_test_accuracy', 'split1_test_accuracy','split2_test_accuracy', 'split3_test_accuracy']].iloc[3]
res_5 = sorted_results[['split0_test_accuracy', 'split1_test_accuracy','split2_test_accuracy', 'split3_test_accuracy']].iloc[4]

# Crear un boxplot para los cuatro valores de accuracy
plt.boxplot([res_1.values,res_2.values,res_3.values,res_4.values,res_5.values], label = ['res_1','res_2','res_3','res_4','res_5'])
plt.title('Boxplots de Accuracy para los 4 Splits')
plt.xlabel('Splits de Cross Validation')
plt.ylabel('Accuracy')
plt.show()

# modelo_GB = RandomForestClassifier(**sorted_results['params'].iloc[N],random_state=123) para el modelo N deseado
modelo_GB = grid_search_GB.best_estimator_

y_train_pred_gb = modelo_GB.predict(X_train)
y_test_pred_gb = modelo_GB.predict(X_test)
print(f'Se tiene un accuracy para train de: {accuracy_score(y_train,y_train_pred_gb)}')
print(f'Se tiene un accuracy para test de: {accuracy_score(y_test,y_test_pred_gb)}')
print('Nótese la diferencia en accuracy para ambos conjuntos de datos se ha reducido en gran medida.')

# Crear un gráfico de dispersión para comparar las predicciones
plt.figure(figsize=(10, 6))

plt.scatter(np.arange(len(y_test)), y_test, color='green', label='True Values', marker='o', s=100)
plt.scatter(np.arange(len(y_test)), y_pred_base, color='orange', label=f'GB: basen (Acc: {accuracy_a:.2f})', marker='x', s=70)
plt.scatter(np.arange(len(y_test)), y_test_pred_gb, color='blue', label=f'GB: GridSearch (Acc: {accuracy_score(y_test,y_test_pred_gb):.2f})', marker='x', s=70)

plt.title('Predicciones Gradient Boosting')
plt.xlabel('Índice de la Muestra')
plt.ylabel('Etiqueta de Clase')
plt.legend()
plt.show()

print('Resultados para Modelo')
print(classification_report(y_test, y_test_pred_gb))

############################################################################
# ahroa vemos para regresion
##########################################################################333
file_path = 'compress.csv'  # Reemplaza con la ruta correcta de tu archivo
file_path_3 = 'compress.csv'  # Reemplaza con la ruta correcta de tu archivo
file_path_4 = 'compress.csv'

compress = pd.read_csv(file_path_4)
compress.head()

# Separar las variables predictoras y la variable de respuesta.
X_c = compress.drop('cstrength', axis=1)
y_c = compress['cstrength']
gb_regressor = GradientBoostingRegressor(n_estimators = 450, subsample = 1, random_state = 123,n_iter_no_change = 10)
# Crear un conjunto de entrenamiento y uno de prueba
X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X_c, y_c, test_size=0.2, random_state=123)
# Construir el modelo de árbol de decisiones
gb_regressor.fit(X_train_c, y_train_c)

#se valora el posible sobreajuste
pred_gb_c_train = gb_regressor.predict(X_train_c)
pred_gb_c_test = gb_regressor.predict(X_test_c)
print(f'MAE del modelo en train:{mean_absolute_error(y_train_c,pred_gb_c_train)}')
print(f'MAE del modelo en test:{mean_absolute_error(y_test_c,pred_gb_c_test)}')

# En caso de necesitar probar diferentes parametrizaciones. En este caso, iremos directamente a la validación cruzada.
params_c = {
    'max_depth': [2, 3, 5, 10, 20],
    'min_samples_split': [5, 10, 20, 50, 100],
    'criterion': ['squared_error', 'friedman_mse', 'absolute_error', 'poisson']
}
# Definir las métricas de evaluación que deseas utilizar

scoring_metrics_c = {
    'MAE': make_scorer(mean_absolute_error),
    'MSE': make_scorer(mean_squared_error)
}
# los parámetros necesitan presentar formato lista.
params = {
    'criterion': ['friedman_mse'], 
    'learning_rate': [0.1,0.3],
    'max_depth': [3,5,10], 
    'min_samples_leaf': [1,5], 
    'min_samples_split': [2,4],
    'n_estimators': [50,100,150],
    'random_state': [123]
}
grid_search_gb_c = GridSearchCV(estimator=gb_regressor, 
                           param_grid=params, 
                           cv=4, scoring = scoring_metrics_c, refit='MAE')
grid_search_gb_c.fit(X_train_c, y_train_c)

pd.DataFrame(grid_search_gb_c.cv_results_).columns

# Ordenar el DataFrame por la métrica de interés (por ejemplo, accuracy)
sorted_results_c = pd.DataFrame(grid_search_gb_c.cv_results_).sort_values(by='mean_test_MAE', ascending=True).head(5)

res_1_c = sorted_results_c[['split0_test_MAE', 'split1_test_MAE','split2_test_MAE','split3_test_MAE']].iloc[0]
res_2_c = sorted_results_c[['split0_test_MAE', 'split1_test_MAE','split2_test_MAE','split3_test_MAE']].iloc[1]
res_3_c = sorted_results_c[['split0_test_MAE', 'split1_test_MAE','split2_test_MAE','split3_test_MAE']].iloc[2]

# Crear un boxplot para los cuatro valores de accuracy
plt.boxplot([res_1_c.values,res_2_c.values,res_3_c.values], label = ['res_1','res_2','res_3'])
plt.title('Boxplots de la robustez en MAE')
plt.xlabel('Splits de Cross Validation')
plt.ylabel('MAE')
plt.show()

# seleccionemos el segundo modelo dada su mayor robustez con respecto al propuesto por GridSearch
# nótese que "**" es para desempaquetar una lista de valores.
grid_search_gb_c_fin = GradientBoostingRegressor(**sorted_results_c['params'].iloc[1])
grid_search_gb_c_fin.fit(X_train_c, y_train_c)

#se valora el posible sobreajuste
pred_gb_c_train_fin = grid_search_gb_c_fin.predict(X_train_c)
pred_gb_c_test_fin = grid_search_gb_c_fin.predict(X_test_c)
print(f'MAE del modelo en train:{mean_absolute_error(y_train_c,pred_gb_c_train_fin)}')
print(f'MAE del modelo en test:{mean_absolute_error(y_test_c,pred_gb_c_test_fin)}')

indices = np.arange(1, len(y_test_c) + 1)

plt.figure(figsize=(8, 6))
plt.scatter(indices, y_test_c, color='darkgreen', label='reales')  # Puedes ajustar el color según tus preferencias

plt.scatter(indices, pred_gb_c_test_fin, color='red', alpha=0.5, label='GradientBoosting_fin')  # Puedes ajustar el color y la transparencia según tus preferencias

plt.title('Scatter Plot de valores reales vs gradient boosting')
plt.xlabel('Observaciones')
plt.ylabel('Valores')
plt.legend()  # Agregar leyenda
plt.grid(True)
plt.show()

# Calcular diferentes medidas de bondad de ajuste
mae = mean_absolute_error(y_test_c, pred_gb_c_test_fin)
mse = mean_squared_error(y_test_c, pred_gb_c_test_fin)
rmse = np.sqrt(mse)
r2 = r2_score(y_test_c, pred_gb_c_test_fin)

# Imprimir las métricas
print(f'MAE (Error Absoluto Medio): {mae:.2f}')
print(f'MSE (Error Cuadrático Medio): {mse:.2f}')
print(f'RMSE (Raíz del Error Cuadrático Medio): {rmse:.2f}')
print(f'R2: {r2}')