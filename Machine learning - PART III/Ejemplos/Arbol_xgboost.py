import os
os.chdir('/home/jerry/Documents/master/Master/Machine learning - PART III/Data')

from sklearn.model_selection import train_test_split, GridSearchCV
from xgboost import XGBClassifier, XGBRegressor
from sklearn.tree import plot_tree
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, roc_curve, auc
from sklearn.metrics import make_scorer, mean_absolute_error, mean_squared_error, r2_score
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns
from sklearn.model_selection import learning_curve

file_path = 'arboles.csv'  # Reemplaza con la ruta correcta de tu archivo
file_path_2 = 'arboles.csv'
file_path_3 = 'arboles.csv'
df = pd.read_csv(file_path_3)
print(df.head())
print(f'\nLa frecuencia de cada clase es: \n{df.chd.value_counts(normalize=True)}')

# Categorizar la variable de respuesta
#df['chd'] = df['chd'].apply(lambda x: 'Yes' if x == 1 else 'No')
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

xgb_classifier = XGBClassifier(booster = 'gbtree', n_estimators = 200, 
                               eta = 0.1, gamma = 1, random_state=123, max_depth = 15, tree_method = 'hist')
xgb_classifier.fit(X_train, y_train)
y_pred_base = xgb_classifier.predict(X_test)
# Evaluar el rendimiento del modelo
accuracy_a = accuracy_score(y_test, y_pred_base)
print(f'Precisión de gradient boosting: {accuracy_a}')

# se procede a observar el posible sobreajuste comparando predicciones en train y test.
# predicciones significativamente mayores en train que en test puede indicar sobreajuste.
# Predicciones en conjunto de entrenamiento y prueba
y_train_pred = xgb_classifier.predict(X_train)
y_test_pred = xgb_classifier.predict(X_test)
print(f'Se tiene un accuracy para train de: {accuracy_score(y_train,y_train_pred)}')
print(f'Se tiene un accuracy para test de: {accuracy_score(y_test,y_test_pred)}')
print('Nótese la diferencia en accuracy para ambos conjuntos de datos y el posible sobreajuste.')

params = {
    'n_estimators': [100,200,300],
    'eta' : [0.1,0.4,0.7],
    'gamma' : [0.1,0.5,1],
    'max_depth': [5, 10]
}

scoring_metrics = ['accuracy', 'precision_macro', 'recall_macro', 'f1_macro']
#recordar que arbol2 es el árbol cuyas VI son todas las variables.
# cv = crossvalidation
grid_search_XGB = GridSearchCV(estimator=xgb_classifier, 
                           param_grid=params, 
                           cv=4, scoring = scoring_metrics, refit='accuracy')
grid_search_XGB.fit(X_train, y_train)

print(grid_search_XGB.best_estimator_.get_params)



# Obtener resultados del grid search
results = pd.DataFrame(grid_search_XGB.cv_results_)
results.head()

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

print(sorted_results['params'].iloc[3])

modelo_XGB = grid_search_XGB.best_estimator_

y_train_pred_xgb = modelo_XGB.predict(X_train)
y_test_pred_xgb = modelo_XGB.predict(X_test)
print(f'Se tiene un accuracy para train de: {accuracy_score(y_train,y_train_pred_xgb)}')
print(f'Se tiene un accuracy para test de: {accuracy_score(y_test,y_test_pred_xgb)}')
print('Nótese la diferencia en accuracy para ambos conjuntos de datos sigue alta con estos parámetros.')

# Crear un gráfico de dispersión para comparar las predicciones
plt.figure(figsize=(10, 6))

plt.scatter(np.arange(len(y_test)), y_test, color='green', label='True Values', marker='o', s=100)
plt.scatter(np.arange(len(y_test)), y_test_pred_xgb, color='blue', label=f'GB: GridSearch (Acc: {accuracy_score(y_test,y_test_pred_xgb):.2f})', marker='x', s=70)

plt.title('Predicciones Gradient Boosting')
plt.xlabel('Índice de la Muestra')
plt.ylabel('Etiqueta de Clase')
plt.legend()
plt.show()

print('Resultados para Modelo')
print(classification_report(y_test, y_test_pred_xgb))

file_path = 'compress.csv'  # Reemplaza con la ruta correcta de tu archivo
file_path_3 = 'compress.csv'  # Reemplaza con la ruta correcta de tu archivo
file_path_4 = 'compress.csv'

compress = pd.read_csv(file_path_4)
compress.head()

# Separar las variables predictoras y la variable de respuesta.
X_c = compress.drop('cstrength', axis=1)
y_c = compress['cstrength']
xgb_regressor = XGBRegressor(booster = 'gbtree', n_estimators = 200, 
                               eta = 0.1, gamma = 1, random_state=123, max_depth = 15, tree_method = 'hist')
# Crear un conjunto de entrenamiento y uno de prueba
X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X_c, y_c, test_size=0.2, random_state=123)
# Construir el modelo de árbol de decisiones
xgb_regressor.fit(X_train_c, y_train_c)

#se valora el posible sobreajuste
pred_xgb_c_train = xgb_regressor.predict(X_train_c)
pred_xgb_c_test = xgb_regressor.predict(X_test_c)
print(f'MAE del modelo en train:{mean_absolute_error(y_train_c,pred_xgb_c_train)}')
print(f'MAE del modelo en test:{mean_absolute_error(y_test_c,pred_xgb_c_test)}')
## esta clarisimo que tenemos un problema de overfitting (el mae de test es mucho mas grande que el de train)

# En caso de necesitar probar diferentes parametrizaciones. En este caso, iremos directamente a la validación cruzada.
params = {
    'n_estimators': [100,200,300],
    'eta' : [0.1,0.4,0.7],
    'gamma' : [0.1,0.5,1],
    'max_depth': [5, 10]
}
# Definir las métricas de evaluación que deseas utilizar

scoring_metrics_c = {
    'MAE': make_scorer(mean_absolute_error),
    'MSE': make_scorer(mean_squared_error)
}
# los parámetros necesitan presentar formato lista.
params = {
    'n_estimators': [100,200,300],
    'eta' : [0.1,0.4,0.7],
    'gamma' : [0.1,0.5,1],
    'max_depth': [5, 10]
}
grid_search_xgb_c = GridSearchCV(estimator=xgb_regressor, 
                           param_grid=params, 
                           cv=4, scoring = scoring_metrics_c, refit='MAE')
grid_search_xgb_c.fit(X_train_c, y_train_c)
pd.DataFrame(grid_search_xgb_c.cv_results_).columns

# Ordenar el DataFrame por la métrica de interés (por ejemplo, accuracy)
sorted_results_c = pd.DataFrame(grid_search_xgb_c.cv_results_).sort_values(by='mean_test_MAE', ascending=True).head(5)


res_1_c = sorted_results_c[['split0_test_MAE', 'split1_test_MAE','split2_test_MAE','split3_test_MAE']].iloc[0]
res_2_c = sorted_results_c[['split0_test_MAE', 'split1_test_MAE','split2_test_MAE','split3_test_MAE']].iloc[1]
res_3_c = sorted_results_c[['split0_test_MAE', 'split1_test_MAE','split2_test_MAE','split3_test_MAE']].iloc[2]

# Crear un boxplot para los cuatro valores de accuracy
plt.boxplot([res_1_c.values,res_2_c.values,res_3_c.values], label = ['res_1','res_2','res_3'])
plt.title('Boxplots de la robustez en MAE')
plt.xlabel('Splits de Cross Validation')
plt.ylabel('MAE')
plt.show()

# seleccionemos el mejor modelo propuesto por GridSearch
# nótese que "**" es para desempaquetar una lista de valores.
grid_search_xgb_c_fin = XGBRegressor(**sorted_results_c['params'].iloc[0])
grid_search_xgb_c_fin.fit(X_train_c, y_train_c)

#se valora el posible sobreajuste
pred_xgb_c_train_fin = grid_search_xgb_c_fin.predict(X_train_c)
pred_xgb_c_test_fin = grid_search_xgb_c_fin.predict(X_test_c)
print(f'MAE del modelo en train:{mean_absolute_error(y_train_c,pred_xgb_c_train_fin)}')
print(f'MAE del modelo en test:{mean_absolute_error(y_test_c,pred_xgb_c_test_fin)}')

indices = np.arange(1, len(y_test_c) + 1)

plt.figure(figsize=(8, 6))
plt.scatter(indices, y_test_c, color='darkgreen', label='reales')  # Puedes ajustar el color según tus preferencias

plt.scatter(indices, pred_xgb_c_test_fin, color='red', alpha=0.5, label='XGBoost')  # Puedes ajustar el color y la transparencia según tus preferencias

plt.title('Scatter Plot de valores reales vs gradient boosting')
plt.xlabel('Observaciones')
plt.ylabel('Valores')
plt.legend()  # Agregar leyenda
plt.grid(True)
plt.show()

# Calcular diferentes medidas de bondad de ajuste
mae = mean_absolute_error(y_test_c, pred_xgb_c_test_fin)
mse = mean_squared_error(y_test_c, pred_xgb_c_test_fin)
rmse = np.sqrt(mse)
r2 = r2_score(y_test_c, pred_xgb_c_test_fin)

# Imprimir las métricas
print(f'MAE (Error Absoluto Medio): {mae:.2f}')
print(f'MSE (Error Cuadrático Medio): {mse:.2f}')
print(f'RMSE (Raíz del Error Cuadrático Medio): {rmse:.2f}')
print(f'R2: {r2}')
print('\nTéngase en cuenta que, dado el ejemplo propuesto, el sobreajuste es muy alto como para determinar que el \najuste del modelo es óptimo')

results = pd.DataFrame(grid_search_xgb_c.cv_results_)

pd.DataFrame(grid_search_xgb_c.cv_results_).columns

results['param_eta'] = results['param_eta'].astype(float)
results['mean_test_MAE'] = results['mean_test_MAE'].astype(float)

# Crear el lineplot
plt.figure(figsize=(10, 6))
sns.lineplot(x='param_eta', y='mean_test_MAE', data=results, marker='o')
# Personalizar el gráfico
plt.title('Mean Test MAE vs Param Eta')
plt.xlabel('Param Eta')
plt.ylabel('Mean Test MAE')
plt.grid(True)
plt.show()

results['param_n_estimators'] = results['param_n_estimators'].astype(float)
# Crear el lineplot
plt.figure(figsize=(10, 6))
sns.lineplot(x='param_n_estimators', y='mean_test_MAE', data=results, marker='o')
# Personalizar el gráfico
plt.title('Mean Test MAE vs n_estimators')
plt.xlabel('n_estimators')
plt.ylabel('Mean Test MAE')
plt.grid(True)
plt.show()

results['param_eta'] = results['param_eta'].astype(float)
results['param_n_estimators'] = results['param_n_estimators'].astype(float)
results['mean_test_MAE'] = results['mean_test_MAE'].astype(float)

# Crear el lineplot con diferentes líneas para cada valor de 'param_n_estimators'
plt.figure(figsize=(10, 6))
sns.lineplot(x='param_n_estimators', y='mean_test_MAE', hue='param_eta', data=results, marker='o')

# Personalizar el gráfico
plt.title('Mean Test MAE vs n_estimators (colored by eta)')
plt.xlabel('Param n_estimators')
plt.ylabel('Mean Test MAE')
plt.legend(title='Param eta')
plt.grid(True)
plt.show()