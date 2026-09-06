############################IMPORTAMOS LIBRERIAS##############################
#importar las librerías necesarias
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
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, roc_curve, auc
from sklearn.metrics import make_scorer, mean_absolute_error, mean_squared_error, r2_score
########################################################################################################
import os 
os.chdir('C:/Users/gerar/Desktop/Master/Master/Machine learning - PART I/Data')
seed=12345 #fijamos la semilla de aleatorización para que sea la misma en todo el proceso
#Reemplaza con la ruta correcta y nombre de tu archivo
file_path = 'SAheart.csv' 
#convertir a data frame el archivo
df = pd.read_csv(file_path)
#La variable de interés es chd, binaria Si/No
#analizamos la frecuencia de cada clase
print(f'\n Instancias: {df.shape[0]}; Variables: {df.shape[1]}')
print(f'\nLa frecuencia de cada clase es: \n{df.chd.value_counts()}')

# Si se quiere categorizar la variable de respuesta (útil cuando tiene 1/0)
#df['chd'] = df['chd'].apply(lambda x: 'Yes' if x == 1 else 'No')
#en nuestro caso, cambiamos Si por Yes
df['chd'] = df['chd'].apply(lambda x: 'Yes' if x == 'Si' else 'No')
# hay valores perdidos?
df.isna().sum()

# organiza las variables según su rol y naturaleza
# determina variable objetivo
target = "chd"
#hacer una lista con las variables input numericas
num_cols = ['sbp', 'tobacco', 'ldl', 'adiposity', 'typea', 'obesity', 'alcohol', 'age']
#hacer una lista con las variables input categóricas
cat_cols = ['famhist']

#Convertir a dummies las categóricas
#solo hay una variable categórica, transformación fácil
df[['famhist']] = pd.get_dummies(df[['famhist']],drop_first=True)
#otra opción
cat_cols = ColumnTransformer(transformers=[ ('ohe', OneHotEncoder(drop='first'), cat_cols)], 
                                                  remainder='passthrough')

#####aqui vamos a probar la funcion de gridsearch

# Tuneo y evaluación predictiva del modelo para variable dependiente continua
# El grupo de variables predictoras se define y se fija
X = df[['famhist','tobacco','alcohol']] #en X las variables ya están normalizadas y con dummies
y = df['chd']

# 1. División de dato
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=seed)

## 2. Transformación de variables
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
transformador = ColumnTransformer([('OHE',OneHotEncoder(drop='first'),['famhist']), 
                                   ('MinMax',MinMaxScaler(),['tobacco','alcohol'])]) ## definimoos lista de tuplas, cada tupla va a ser una transformacion, le ponemos nombre, decimos que transformacion aplicar y a que lista aplicarla
##antes aplicambamos asi: transform = StandardScaler()
# ahora aplciamos dos tipos de cambio debido a que tenemos dos variables pero el proceso es identifco
X_train=transformador.fit_transform(X_train)
X_test=transformador.transform(X_test)

#3. Definio el modelo base
red = MLPClassifier(random_state=1234)
#definimos los parámetros que queremos tunear
params = {
    'max_iter': [900], #cantidad de iteraciones que se le permiten al algoritmo de optimizacion
    'hidden_layer_sizes': [5,7,9],#redes con una sola capa oculta, con un tamaño distinto en cada arquitectura
    'activation': ['tanh','relu'], #función de activación usada
    'alpha': [0.001,0.0001] #regularización L2, valor alto puede resultar en un modelo más sesgado pero con menor varianza. 
    #valor más bajo permite que el modelo se ajuste más a los datos de tr, aunque con un mayor riesgo de sobreajuste
}
scoring_metrics = ['accuracy', 'precision_macro', 'recall_macro', 'f1_macro']
# cv = crossvalidation con n folds con todas las combinaciones de parámetros
# GridSearchCV utiliza la función .predict como método subyacente, por lo tanto, clasifica
#en la clase con probabilidad más alta, lo que es equivalente a usar 0.5 como threshold
grid_search = GridSearchCV(estimator=red, 
                           param_grid=params, 
                           cv=4, scoring = scoring_metrics, refit='accuracy')

#ajusta en entrenamiento con todas las combinaciones
grid_search.fit(X_train, y_train) ### esto se debe ejecutrar mejor en jupìter

# Obtener resultados del grid search
results = pd.DataFrame(grid_search.cv_results_)
# Mostrar resultados
print("Resultados de Grid Search:")
print(results[['params', 'mean_test_accuracy', 'mean_test_precision_macro', 'mean_test_recall_macro', 'mean_test_f1_macro']])
#print(results) #para ver todos los atributos obtenidos y entender cómo usarlos

# Obtener el mejor modelo (en cuanto a optimización del criterio)
best_model = grid_search.best_estimator_
print(grid_search.best_estimator_)

print(results)
## tenemos el valor en test para cada una de las varibales definidas previuamente
## tenemos tmbv cada uno de los splits / cortes que hemos dicho (en este caso 4)
# se seleccionan los modelos candidatos, y analiza su robustez a lo largo de cross validation.
ac_1 = results[['split0_test_accuracy', 'split1_test_accuracy','split2_test_accuracy', 'split3_test_accuracy']].iloc[4]
ac_2 = results[['split0_test_accuracy', 'split1_test_accuracy','split2_test_accuracy', 'split3_test_accuracy']].iloc[5]
ac_3 = results[['split0_test_accuracy', 'split1_test_accuracy','split2_test_accuracy', 'split3_test_accuracy']].iloc[8]
# Crear un boxplot para los cuatro valores de accuracy
plt.boxplot([ac_1.values,ac_2.values,ac_3.values], tick_labels = ['Red4','Red5','Red8'])
plt.title('Boxplots de Accuracy para los 4 Splits')
plt.xlabel('Splits de Cross Validation')
plt.ylabel('Accuracy')
plt.show()

#########ahora vasmo a ver otra form nominal de convertir la variable objetivonominal a 0/1 siu hace falta en algun momento

#analizar y reentrenar redes candidatas AUC
from sklearn.preprocessing import LabelBinarizer
X = df[['famhist','tobacco','alcohol']] #en X las variables ya están normalizadas y con dummies
y = df['chd']
lb = LabelBinarizer()
y_bin = lb.fit_transform(y).ravel()   # produce 0/1#para calcular el AUC, y debe ser numérica

X_train, X_test, y_train, y_test = train_test_split(X, y_bin, test_size=0.2, random_state=seed)


red4 = MLPClassifier(**results.iloc[4].params,random_state=seed)
red5 = MLPClassifier(**results.iloc[5].params,random_state=seed)
red8 = MLPClassifier(**results.iloc[8].params,random_state=seed)

# Ajustamos
red4.fit(X_train, y_train)
red5.fit(X_train, y_train)
red8.fit(X_train, y_train)


# Calculamos las predicciones en test, en términos de probabilidad para poder dibujar el AUC
y_pred4 = red4.predict_proba(X_test)[:,1]
y_pred5 = red5.predict_proba(X_test)[:,1]
y_pred8 = red8.predict_proba(X_test)[:,1]

fpr, tpr, thresholds = roc_curve(y_test, y_pred4)
roc_auc = auc(fpr, tpr)
print(f"\nÁrea bajo la curva ROC (AUC) para la red 4 en test: {roc_auc:.2f}")

# Graficar la curva ROC
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'AUC = {roc_auc:.2f}')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlabel('Tasa de Falsos Positivos (FPR)')
plt.ylabel('Tasa de Verdaderos Positivos (TPR)')
plt.title('Curva ROC red4')
plt.legend(loc="lower right")
plt.show()

########## ahora vamos al apso final
# medidas de bondad de ajuste en test: ojo, necesitamos la clasificación continua
X = df[['famhist','tobacco','alcohol']] #en X las variables ya están normalizadas y con dummies
y = df['chd']

# 1. División de dato
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=seed)

## 2. Transformación de variables
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
transformador = ColumnTransformer([('OHE',OneHotEncoder(drop='first'),['famhist']), 
                                   ('MinMax',MinMaxScaler(),['tobacco','alcohol'])])
X_train=transformador.fit_transform(X_train)
X_test=transformador.transform(X_test)

# Definimos el modelo
red4 = MLPClassifier(**results.iloc[4].params,random_state=seed)

#Ajustamos
red4.fit(X_train, y_train)


#calculamos las predicciones en test, en términos de probabilidad para poder dibujar el AUC
y_pred4 = red4.predict(X_test)
conf_matrix = confusion_matrix(y_test, y_pred4)
print("Matriz de Confusión:")
print(conf_matrix)
print("\nMedidas de Desempeño:")
print(classification_report(y_test, y_pred4))
##viendo esta matriz vemos que no lo estamos ahciendo bien que nos da piosta que nos indica que tenemos 10 falsos positivos. Entonces tenemos que volver al inicio, corregir ty vcambiar la arquitectura, y volver a probar