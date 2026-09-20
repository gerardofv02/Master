###########3 EJEMPLO PARA VD: CATEGORICA con una sola variable



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
# Construir el modelo de árbol de decisiones
arbol1.fit(X_train, y_train)

# ES IMPORTANTE QUE LA DISTRIBUCIÓN DE LAS CLASES SEA 'SIMILAR' EN TRAIN Y TEST.
print(f'La frecuencia de cada clase en train es: \n{y_train.value_counts(normalize=True)}')
print(f'\nLa frecuencia de cada clase en test es: \n{y_test.value_counts(normalize=True)}')

# Conocer los niveles de la variable a predecir
print(arbol1.classes_)
# Conocer el nombre de las variables predictoras
print(arbol1.feature_names_in_)
# Obtener información detallada de cada nodo y las reglas de decisión
tree_rules = export_text(arbol1, feature_names=list(X.columns),show_weights=True)
print(tree_rules)
## AQUI EN ESTE ARBOL SE VE COMO SE HA FORMADO entonces donde pone weights: ['cantidad de iondividuos q no','cantidad de individuos que si'] basandose en esto, los pone en una clase u en otra

# se puede ver graficamnete tmb<>:
plt.figure(figsize=(10, 6))
plot_tree(arbol1, feature_names=X.columns.tolist(), class_names=['No', 'Yes'], filled=True,
         proportion = True)
plt.show()

 