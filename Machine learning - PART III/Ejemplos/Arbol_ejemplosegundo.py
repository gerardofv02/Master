###########3 EJEMPLO PARA VD: CATEGORICA con mas de una variable



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

## en este ejemplo que hemos generado, se ha generado uin arbol mas grande debido a que hay mas cantidad de nodos y mas cantidad  de variables que usamos. Pero esta claro que hemos overextendido ya que vemos nodos en los q hya muy pocas muestras (0.8% por ejemplo)    
## aqui hay overfitting y habria qu hacer poda o cambiar las variables de entrada para que uedara mejor