import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

sns.set_style('darkgrid')
np.set_printoptions(precision=2) 
warnings.filterwarnings("ignore")


from sklearn.preprocessing import OneHotEncoder, LabelEncoder, PowerTransformer
from sklearn.impute import SimpleImputer, KNNImputer

from sklearn.feature_selection import SelectKBest, chi2, RFE
from sklearn.model_selection import train_test_split 
from sklearn.pipeline import make_pipeline, Pipeline 
from sklearn.decomposition import PCA

from sklearn.linear_model import LogisticRegression 
from sklearn.tree import DecisionTreeClassifier 
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.svm import SVC

from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, f1_score

from sklearn.model_selection import KFold, ShuffleSplit, LeaveOneOut, StratifiedKFold
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV 
""" Semilla """
seed = 99


## Primero cargamos la base de datos Saheart
# Obtén el directorio actual del script o cuaderno
# Define el nombre del archivo CSV
import os
os.chdir('C:/Users/gerar/Desktop/Master/Master/Machine learning - PART I/Data')


#df = pd.read_csv("c:/Users/dagom/Documents/docencia/DOCENCIA_FINAL_2023_PHYTON_ML_DANI/2_Introduccion_y_SVM/SAheart.csv", sep=",", decimal=".")
df = pd.read_csv("SAheart.csv", sep=",", decimal=".")
print(df.dtypes)
df.head()
df.describe()
df.quantile(np.arange(0, 1, 0.1), numeric_only=True)
variables = df.columns.values 
print(df)


## una pequeña visualizacion 
import seaborn as sns
# sns.pairplot(df, hue="chd",palette="bright")
# plt.show()


### Importante que el SVM no funciona bien ni con missing ni con valores no estandarizados

## Paso 1. vemos cuantos missing tenemos en cada variable ##
df.isnull().sum()

## Paso 2. estandarizar
from sklearn import preprocessing

col_cat = df[['famhist', 'chd']]
col_num = df[['sbp', 'tobacco', 'ldl', 'adiposity', 'typea', 'obesity', 'alcohol', 'age']]

### TIPIFICAMOS O COMO DICEN LOS MODERNOS STANDARIZAMOS.....
scaler = preprocessing.StandardScaler().fit(col_num)
col_num_standarizada = scaler.transform(col_num)

col_num_standarizada.mean(axis=0)
col_num_standarizada.std(axis=0)

col_num_standarizada = pd.DataFrame(col_num_standarizada)


df_depurada = pd.concat([col_num_standarizada, col_cat],  axis=1) ## aunque asi se pierden los nombres de las variables 

## recuperamos los nombres y tenemos  nuestra base de datos depurada  
df_depurada=df_depurada.set_axis(['sbp', 'tobacco', 'ldl', 'adiposity', 'typea', 'obesity', 'alcohol', 'age','famhist', 'chd'], axis=1)

# sns.pairplot(df_depurada, hue="chd",palette="bright")
## Paso 3. Variables categoricas las pasamos a dummies 

df_depurada_dummies = pd.get_dummies(df_depurada,columns=['famhist'], drop_first= True)
df_depurada_dummies.head()

## YA YENEMOS NUESTRO DATASET OK PARA APLICAR SVM: SIN MISSING, ESCALADA Y CON DUMMIES...
##cogemos todas las variables predictoras (X) aqqui hay q quitar la variable target y cogemos tmb la variabla target (y)
X = df_depurada_dummies.drop('chd', axis=1)
y = df_depurada_dummies["chd"]

### emepzamos con el SVM
from sklearn.model_selection import GridSearchCV

print("Feature Variables: ")
print(df_depurada_dummies.info())

[X_train, X_test, y_train, y_test] = train_test_split(X, y, test_size = 0.30, random_state = 101) ##dividimos train y test a un 30%

tabla_target=pd.DataFrame(y_test.value_counts())

# train the model on train set
model = SVC(kernel='linear')
model.fit(X_train, y_train)
  
# print prediction results
predictions = model.predict(X_test)
print(classification_report(y_test, predictions))


##calculamos la mactriz de confusion y la precision del modelo
cm = confusion_matrix(y_test, predictions)
print(cm)
accuracy=(cm[0,0]+cm[1,1])/(cm[0,1]+cm[1,1]+ cm[1,0]+cm[0,0])
print('accuracy' , accuracy)


### validacion cruzada ### sirve para verificar el correcto funcionamiento del modelo
from sklearn.model_selection import cross_val_score
results = cross_val_score(estimator=model, X=X, y=y, cv=5)
print(results)


########## ahora vasmo a buscar la mejor busqueda parametrica para obtener la mejor configracion parametrica esto se hace con el grid search

###################### busqueda parametrica 

########################################
## CASO 1. BUSQUEDA CON KERNEL LINEAL 
########################################

## busqueda de parametros para el caso lineal ###
from sklearn.model_selection import GridSearchCV
  
# definimos los rangos de los parametros 
param_grid_lineal = {'C': [0.1, 0.15, 0.19, 0.2, 0.21, 0.22, 0.25, 0.3, 0.4, 0.5, 1, 2, 5, 10, 100] }  #asignamos una serie de valores bajos y altos porqque vamos un pcoo ciegos sin  saber mucho como saldrán. Entonces asignamos a la variabl C todo tipo de valores
 
grid = GridSearchCV(SVC(kernel='linear'), param_grid_lineal, refit = True, cv=10, verbose = 3)
  
# ENTRENAMOS EN TRAIN Y BUSCAMOS EN TRAIN
resultados = grid.fit(X_train, y_train)

####### visualizar los resultados para decidir si debemos seguir buscando.
# Crear gráfico de dispersión
import matplotlib.pyplot as plt
import numpy as np

aux=pd.DataFrame(resultados.cv_results_)

plt.scatter(aux[['param_C']], aux[['mean_test_score']], color='b', alpha=0.9)

plt.xlabel('Parametro C')
plt.ylabel('Accuracy ')
plt.xlim(0, 1) ## modificar el parametro de la derecha para ver el valor de c la precision
# Añadir título al gráfico
plt.title('Precisión media SVM en función del parametro C ')

# Mostrar el gráfico
plt.show()

## segun vemos este grafico a partir de c valores grandes ya sigue la misma precision y n o se mueve mientras q valores chicos es mas variables. segun vemos en la parte de 0'.2 es mas grande estos valores

###AHORA VAMOS A VER EL VALOR OPRTIMO DE C:
# print best parameter after tuning
print(grid.best_params_) #-> 0.19 parece que es el valor optiomp
 
# print how our model looks after hyper-parameter tuning
print(grid.best_estimator_)#-> 0.19 parece que es el valor optiomp y kernel lienar

##############################################
### PREDECIMOS CON EL  MEJOR MODELO LINEAL ###
##############################################
grid_predictions = grid.predict(X_test)
  
# print classification report
print(classification_report(y_test, grid_predictions))

#### DIFERENCIAS ??? ## SE MEJORA

cm = confusion_matrix(y_test, grid_predictions)
print(cm)
accuracy=(cm[0,0]+cm[1,1])/(cm[0,1]+cm[1,1]+ cm[1,0]+cm[0,0])
print('accuracy' , accuracy)

### Cambiamos el kernel ###
########################################
## CASO 2. BUSQUEDA CON KERNEL GAUSIANO  
########################################

param_grid_gausiano = {'C': [0.1, 1, 2, 5, 10, 100], 
              'gamma': [1, 0.1, 0.01, 0.001, 0.0001],
              'kernel': ['rbf']}  

grid_gausiano = GridSearchCV(SVC(), param_grid_gausiano, refit = True, cv=5, verbose = 3)

# fitting the model for grid search
resultados = grid_gausiano.fit(X_train, y_train)

print(grid_gausiano.best_params_) ## como vemos el optimo se alcanza con gama 0.01 y kernel rbf
 
print(grid_gausiano.best_estimator_)

############################################
#### visualizamos los resultados  GAUSIANO
##############################################
aux = pd.DataFrame(resultados.cv_results_)

# discretizar la variable sigma en 5 categorías

# factorizar la variable sigma
categorias, valores_enteros = pd.factorize(aux['param_gamma'])


# crear el gráfico de dispersión con colores basados en las categorías de sigma


plt.scatter(aux[['param_C']], aux[['mean_test_score']], c=categorias , cmap='viridis')
plt.xlabel('Parametro C')
plt.ylabel('Accuracy ')
plt.xlim(0, 12)
# Añadir título al gráfico
plt.title('Precisión media SVM en función del parametro C ')

plt.show()

## como vemos este grafico a rangos largos podemos ver la suavidad de la curva, algunas mas suaves y otras con valores mas largos
## segun el gamma que escojamos, nos viene bien coger unos valores c u otros
##el mejro en teoria es gamma 0.01 con el c = 10 pero igual hay que bsucar entre 10 y 100 para ver si encontramos mas 

#######################otra posibilidad para hacer el grafico mas sencillo ##

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
sns.set(style="darkgrid")


sns.relplot(x="param_C", y="mean_test_score",  size='param_gamma' ,  data=aux)
plt.show()

 ##############################################
### PREDECIMOS CON EL  MEJOR MODELO GAUSIANO ENCONTRADO ###
##############################################
grid_predictions = grid_gausiano.predict(X_test)
  
# print classification report
print(classification_report(y_test, grid_predictions))

#### DIFERENCIAS ??? ## SE MEJORA

cm = confusion_matrix(y_test, grid_predictions)
print(cm)
accuracy=(cm[0,0]+cm[1,1])/(cm[0,1]+cm[1,1]+ cm[1,0]+cm[0,0])
print('accuracy' , accuracy)


###################################################
########################## MODELO POLINOMIAL SVM
##################################################

### aqui con el modelo polinomial tenemos 4 dimensiones que ver. primero se elige con el fgrado, luego con la escala y leugo con el C
# 
#  

param_grid_poli = {'C': [0.1, 0.2,.03, 0.5, 1, 2 ,3, 4,  5, 10], 'degree': [2, 3], 
                   'coef0': [0, 1, 2, 3, 4], 'kernel': ['poly']}  

grid_poli = GridSearchCV(SVC(), param_grid_poli, refit = True, cv=5, verbose = 3)


resultados = grid_poli.fit(X_train, y_train)
aux= pd.DataFrame(resultados.cv_results_)

######### visualizamos los resultados ###

sns.relplot(x="param_C", y="mean_test_score", palette="ch:r=-.5,l=.75", hue="param_degree", size="param_coef0", style='param_degree',  data=aux);

## se puede probar tambien col (interesante)
print(grid_poli.best_params_)
 
print(grid_poli.best_estimator_)
plt.show()

## primero aqui es mejor decidir si nos quedamos con los verdes o los negros (segun aqui son mejores los verdes) y luego centrarnos unica uy exclusivamente en los roels para hacer una visualizacion de 2 dimensiones

## aqui vemos que con el grado 2 obtendriamos mejores resultados y menos sobreajuste y quizas merece la pena analizar el coeficiente

##############################################
### PREDECIMOS CON EL  MEJOR MODELO POLINOMIAL ENCONTRADO ###
##############################################
grid_predictions = grid_poli.predict(X_test)
  
# print classification report
print(classification_report(y_test, grid_predictions))


#### CON CUAL DE LOS TRES NOS QUEDAMOS ???

cm = confusion_matrix(y_test, grid_predictions)
print(cm)
accuracy=(cm[0,0]+cm[1,1])/(cm[0,1]+cm[1,1]+ cm[1,0]+cm[0,0])
print('accuracy' , accuracy)

############################################
#### visualizamos los resultados  POlINOMIAL
##############################################
aux = pd.DataFrame(resultados.cv_results_)


######### visualizamos los resultados ###

sns.relplot(x="param_C", y="mean_test_score", palette="ch:r=-.5,l=.75", hue="param_degree", size="param_coef0", style='param_degree',  data=aux)

plt.show()

###########
# Como ultimo paso hay que comparar los 3 modelos que hemos estado estudiando y en principoio salvo que haya una diferencia significativa se suele aplcioar el principio de parsimonia donde si tengo el modelo sencillo yu no es significativamente peor que los modelos anteriores como parece q es este caso (0.7) ps nen este caso nos quedariakmos con el modelo lineal