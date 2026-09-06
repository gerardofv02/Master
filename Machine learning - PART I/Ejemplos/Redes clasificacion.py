############################IMPORTAMOS LIBRERIAS##############################
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
from sklearn.metrics import ConfusionMatrixDisplay
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
print(df.head())
#La variable de interés es chd, binaria Si/No
#analizamos la frecuencia de cada clase
print(f'\n Instancias: {df.shape[0]}; Variables: {df.shape[1]}')
print(f'\nLa frecuencia de cada clase es: \n{df.chd.value_counts()}')

## queremos ver el reigso de obtener una enferemdad coronaria

################VEMOS EL DIAGRAMA DE DISPERSION###################
#representamos la relación enre la variable de interés y las variables input
df['chd_numeric'] = df['chd'].apply(lambda x: 1 if x == 'Si' else 0)
# Crear el diagrama de dispersión con regresión
sns.regplot(x=df['age'], y=df['chd_numeric'], ci=None,fit_reg=False)
plt.xlabel('age ')
plt.ylabel('chd')
plt.title('Diagrama de Dispersión')
plt.show()
# Crear el diagrama de dispersión con regresión
sns.regplot(x=df['tobacco'], y=df['chd_numeric'], ci=None,fit_reg=False)
plt.xlabel('tobacco')
plt.ylabel('chd')
plt.title('Diagrama de Dispersión')
plt.show()
###############################################################################

################## VEMOS LA VAIRABLE DE INTERES ##################################
import pandas as pd

y_series = pd.Series(df['chd_numeric'])
print(y_series.value_counts(normalize=True))

##En este caso estamos vbiendo que tenemos un 65% de tasa 1 en la variable de interes pero no es extrema la diferencia con lo que vamos a trabajar con 0 y 1
##################################################################################

#### si quisiesemos categorizar la variable de respuesta: ######################################
# Si se quiere categorizar la variable de respuesta (útil cuando tiene 1/0)
#df['chd'] = df['chd'].apply(lambda x: 'Yes' if x == 1 else 'No')
#en nuestro caso, cambiamos Si por Yes
df['chd'] = df['chd'].apply(lambda x: 'Yes' if x == 'Si' else 'No')
print(df.head())
##########################################################
#############################Revisamos si tenemos datos faltantes, ya que es MUY IMPORTANTE no tener estos datos faltantes################
# hay valores perdidos?
df.isna().sum()
#######################################################################################################################################

######## es importante que las variables no tengan datos faltantes, esten los datos estandarizados y convetir a dummies las variables categóricas
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
# drop_first en la función get_dummies de pandas se utiliza para controlar si se debe eliminar 
#la primera columna de las variables dummy que se generan. 
#Cuando drop_first se establece en True, se elimina la primera columna de cada conjunto de variables dummy, lo que ayuda a evitar la multicolinealidad en modelos lineales
#otra opción
cat_cols = ColumnTransformer(transformers=[ ('ohe', OneHotEncoder(drop='first'), cat_cols)], 
                                                  remainder='passthrough')
#########################################################################################################################

############################ahora vemos paso a paso toda la transformacion#########################
#Normalizar variables numericas###############
#Si se quisieran estandarizar, scaler=StandardScaler()
scaler = MinMaxScaler() #selecciona el transformador
X = df[num_cols] #selecciona las variables numéricas que se quieren transformar y las guarda en un nuevo dataframe
X_scale = pd.DataFrame(scaler.fit_transform(X)) #guarda el resultado de la transformación de las variables de X en X_scale ## ES IMPORTANTE QUE ANTES DE HACER EL FIT DEBERIAMOS HABER REALIZADO LA PARTICION DE TRAIN Y TEST
X_scale.columns = X.columns #para simplificar los nombres, asigna a las columnas de X_scale los nombres de las variables de X_num
df[num_cols] = X_scale
print(df.head())
##### OTRAS FORMAS DE NORMALIZACIÓN VER SCRIPT 

#########################
### iNTRODUCIR PARTICIONES DE TEST Y TRAIN APLICANDO PRIMER ALGORITMO DE MACHINE LEARNIUNG#############
# Separar las variables predictoras y la variable de respuesta.
# El grupo de variables predictoras se define y se fija
X = df[['tobacco','ldl','famhist']] #en X las variables ya están normalizadas y con dummies
y = df['chd']
#primer approach a red neuronal: definimos la estructura
red1 = MLPClassifier(random_state=seed, hidden_layer_sizes=(5),activation='tanh', 
                     alpha=0.001,solver='adam',max_iter=1000) # EL APRAMETRO DE HIFDDEN LAYER SIZES INDICAMOS LOS NODOS ARTIFICIALES (SI TRABAJAMOS CON UNA CAPA OCULTA ( SE MUESTRAN 5 NODOS ARTIFICIALES DENTRO DE ESA CAPA OCULTA)
##ACTIVATION: FUNCION DE ACTIVACION QUE USAREMOS PARA EL ML
##ALPHA: REGULARIZACION L2 , VALORES ALTOS MUCHA REGULARIZACIÓN Y VICEVERSA
## SOLVER NO ES MUY RELEVANTE
 # MAX_ITER LA CANTIDAD DE ITERACIONES DEL MODELO ML -> POR DEFECTO, SON 100
#Dividir los datos en entrenamiento y test (20% de los datos para test)
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y,test_size=0.2, random_state=seed) ## STRATIFY: Para garantizar que la parte de test sea representativa de la aprte de entranimento se ppuede estratificar por la variable objetivo (en este caso y) aqui estamos pieidneo que mantenga una propoción similiar de 1 en una y otra
# Construir el modelo de red ajustando los pesos a datos de train
red1.fit(X_train, y_train)
########################################################
#############################################################################################
# Niveles de la variable a predecir
print(red1.classes_)
# Nombre de las variables predictoras
print(red1.feature_names_in_)
# Cantidad de iteraciones necesarias para la convergencia, 
#así se puede volver a entrenar el modelo ajustando este parámetro para tener menos coste computacional
print(red1.n_iter_) #no ha hecho falta iterar tanto
#ver los coeficientes de cada enlace
# Acceder a los coeficientes (pesos) de cada capa
print(red1.coefs_)
#si se quiere ver qué atributos podemos analizar en el modelo
#dir(red1)
# ES IMPORTANTE QUE LA DISTRIBUCIÓN DE LAS CLASES SEA 'SIMILAR' EN TRAIN Y TEST.
print(f'La frecuencia de cada clase en train es: \n{y_train.value_counts(normalize=True)}')
print(f'\nLa frecuencia de cada clase en test es: \n{y_test.value_counts(normalize=True)}')

###una vez tenemos el modelo y está entrenado, pasamos a obtener predicciones con los datos de test#############################
#una vez ajustado el modelo en datos de train, lo evaluamos en datos de test
# Realizar predicciones en el conjunto de prueba
y_pred = red1.predict(X_test)

## metricas de bondad de ajuste
# Calcular la precisión del modelo
precision = accuracy_score(y_test, y_pred)
print(f"Precisión del modelo en test: {precision:.4f}")

# Mostrar la matriz de confusión
matriz_confusion = confusion_matrix(y_test, y_pred)
print("Matriz de confusión:")
print(matriz_confusion)

# Mostrar el informe de clasificación
informe_clasificacion = classification_report(y_test, y_pred)
print("Informe de clasificación:")
print(informe_clasificacion)
#################################################################################################

#########otras cosas qu epodemos hacer, representar matriz de donfusiion
import pandas as pd

y_series = pd.Series(y)
print(y_series.value_counts(normalize=True))
#otra forma de mostrar la matriz de confusión
#ConfusionMatrixDisplay, que espera etiquetas binarias

## OJO: ajustamos el label encoder con test y se lo aplicamos a pred. En este caso da un poco igual pero para mantener la forma de aplicación
label_encoder = LabelEncoder()
y_test_encoded = label_encoder.fit_transform(y_test) 
y_pred_encoded = label_encoder.fit_transform(y_pred)

cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=label_encoder.classes_)
disp.plot(cmap=plt.cm.Blues)
plt.title('Matriz de Confusión')
plt.show()
#########################################################
########## vamos a ver una forma para detectar si hay sobreajuste
#una forma de analizar el overfitting es comparando la medida de bondad en train/test
#si hay mucha diferencia, es porque el modelo está sobreajustado
#si ambas son muy malas, es porque el modelo está poco ajustado
# Realizar predicciones en el conjunto de prueba
y_pred_tr = red1.predict(X_train)

# Calcular la precisión del modelo
precision_tr = accuracy_score(y_train, y_pred_tr)
print(f"Precisión del modelo en train: {precision_tr:.4f}")
print(f"Precisión del modelo en test: {precision:.4f}")
#este es un ejemplo de modelo sobreajustado
#####################################################################
####################### ahora vamos a ver la robustez del modelo########################
# esto sirve para ver como de robostu es el modelo
#validación cruzada para una evaluación más robusta del modelo
#importante cambiar el tipo ed scoring atendiendo al tipo de problema
cv_scores = cross_val_score(red1, X, y, cv=5, scoring='accuracy')
cv_precision_mean = np.mean(cv_scores)

print(f'Precisión promedio mediante validación cruzada: {cv_precision_mean:.4f}')
######################################################################################

################### Podemos dividir tmb los datos en 3 modos (test, train y validation)############## (ver ejemploo en script)
################## Ejemplo con etiquetas numericas######################################
from sklearn.datasets import make_classification

# Crear un conjunto de datos de ejemplo
X, y = make_classification(n_samples=1000, n_features=20, n_classes=2, random_state=42)

# Dividir en conjunto de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crear el modelo MLPClassifier
mlp = MLPClassifier(random_state=42)

# Entrenar el modelo
mlp.fit(X_train, y_train)

# Evaluar el modelo
print(mlp.score(X_test, y_test))

#################### ahroa que tenemos las ideas vamos a realizar el proceso completo de prediccion

seed=12345 #fijamos la semilla de aleatorización para que sea la misma en todo el proceso
#Reemplaza con la ruta correcta y nombre de tu archivo
file_path = 'SAheart.csv' 
#convertir a data frame el archivo
df = pd.read_csv(file_path)
print(df.head())
#La variable de interés es chd, binaria Si/No
#analizamos la frecuencia de cada clase
print(f'\n Instancias: {df.shape[0]}; Variables: {df.shape[1]}')
print(f'\nLa frecuencia de cada clase es: \n{df.chd.value_counts()}')

df['chd'] = df['chd'].apply(lambda x: 1 if x == 'Si' else 0)
print(df.head())

df.isnull().sum()

#Definimos qué variables habrá en X: cogemos todas las explicativas cuantitativas

X = df[['sbp','tobacco','ldl','adiposity','typea','obesity','alcohol','age',]] 
y = df['chd']
#1. Defino la partición tr/ts
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y,test_size=0.2, random_state=seed)

#2. No hay variables categóricas, no hay missing, estandarizo las continuas.
scaler= StandardScaler()
X_train=scaler.fit_transform(X_train) #busco la media y desviación típica en train, después transformo train
X_test=scaler.transform(X_test) #con la media y desviación típica que calculé en train, transformo test

#3. Ya estoy en disposición de aplicar una red. Defino su arquitectura
red1 = MLPClassifier(random_state=seed, hidden_layer_sizes=(5),activation='tanh',
                     alpha=0.001,solver='adam',max_iter=1000)

#4. Entreno el modelo en datos de entrenamiento (Ya transformados)
red1.fit(X_train, y_train)


#5. Obtengo predicciones en datos de test (transformados)
y_pred=red1.predict(X_test)

#6. Evalúo en datos de test
accuracy = accuracy_score(y_test,y_pred)
print(f'accuracy en test: {accuracy}')

#Definimos qué variables habrá en X: cogemos todas las explicativas cuantitativas
from sklearn.feature_selection import SelectKBest,f_classif
from sklearn.preprocessing import MinMaxScaler
X = df[['sbp','tobacco','ldl','adiposity','typea','obesity','alcohol','age',]] 
y = df['chd']
#1. Defino la partición tr/ts
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y,test_size=0.2, random_state=seed)

#2.a) No hay variables categóricas, no hay missing, estandarizo las continuas.
scaler= MinMaxScaler()
X_train=scaler.fit_transform(X_train) #busco min y max en train, después transformo train
X_test=scaler.transform(X_test) #con el min y el max que calculé en train, transformo test

#2.b). Selección de variables: con SelectKBest necesito variables no negativas, por eso aplico MinMax
selector = SelectKBest(f_classif,k=4)
X_train = selector.fit_transform(X_train, y_train) #busco las 4 variables propuestas por el selector, y las tomo de train
X_test = selector.transform(X_test) #selector ya sabe qué variables tiene que tomar (lo ha aprendido en train); las toma de test

#3. Ya estoy en disposición de aplicar una red. Defino su arquitectura
red1 = MLPClassifier(random_state=seed, hidden_layer_sizes=(5),activation='tanh',
                     alpha=0.001,solver='adam',max_iter=1000)

#4. Entreno el modelo en datos de entrenamiento (Ya transformados y con las variables seleccionadas)
red1.fit(X_train, y_train)


#5. Obtengo predicciones en datos de test (transformados y con las variables seleccionadas)
y_pred=red1.predict(X_test)

#6. Evalúo en datos de test
accuracy = accuracy_score(y_test,y_pred)
print(f'accuracy en test: {accuracy}')
