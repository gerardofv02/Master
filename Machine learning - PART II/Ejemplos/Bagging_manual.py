## comenzamos con imports y demas
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

sns.set_style('darkgrid')
np.set_printoptions(precision=2)
warnings.filterwarnings("ignore")

import sklearn
from sklearn.preprocessing import MinMaxScaler, StandardScaler, Normalizer, Binarizer, RobustScaler
from sklearn.compose import ColumnTransformer
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

## DATOS ##
import os
os.chdir('/home/jerry/Documents/master/Master/Machine learning - PART II/Data')

data = pd.read_csv("SAheartbis.csv", sep=",", decimal=".")

y=pd.DataFrame(data["chd"]) # variable target
X=data.drop(columns="chd") # variables para calcualr

# train y test
[X_train, X_test, y_train, y_test] = train_test_split(X, y, test_size = 0.30, random_state = 101)

## 4 baggings por ejemplo
### numero de baggings  4
#s1= muestreo con reemplazamiento
import random
n= len(X_train)
s_size=0.45 # tamaño de cada muestra del bagging
n = s_size*n # tamaño de la muestra del bagging
# X_train # lista de datos de la cual queremos hacer la muestra
random.seed(2020)
s1 = random.choices(range(len(X_train)), k=int(n))
X_train_s1 = X_train.iloc[s1] 
y_train_s1 = y_train.iloc[s1] 
s2 = random.choices(range(len(X_train)), k=int(n))
X_train_s2 = X_train.iloc[s2] 
y_train_s2 = y_train.iloc[s2] 
s3 = random.choices(range(len(X_train)), k=int(n))
X_train_s3 = X_train.iloc[s3] 
y_train_s3 = y_train.iloc[s3] 
s4 = random.choices(range(len(X_train)), k=int(n))
X_train_s4 = X_train.iloc[s4] 
y_train_s4 = y_train.iloc[s4] 

## primero comenzamos con le primer paso hacer el modelo sin el bagging
## modelo de ML sobre el que queremos hacer el bagging
## Paso 1 sin bagging
prediciones = [] ## aqui voy a meter todas las predicciones de los modelos 1+ 4 
prediciones_t = [] ## aqui voy a meter todas las predicciones de los modelos 4  en train

model=LogisticRegression(random_state=1) # modelo de regresion logistica
model.fit(X_train,y_train)
prediction=model.predict_proba(X_test)[:,1] ## me quedo con la probabilidad del si
prediction=pd.DataFrame(prediction, columns=['LR'])
prediciones.append(prediction)

accuracy=model.score(X_test, y_test)

# ahora entrenar sobre s1 y ese modelo con el bagging

# Paso 2 hacemos el entrenamiento y prediccion  de los 4 muestras en test y train
model.fit(X_train_s1,y_train_s1)
prediction=model.predict_proba(X_test)[:,1] ## me quedo con la probabilidad del si
prediction=pd.DataFrame(prediction, columns=['LR_s1'])
prediciones.append(prediction)

# ahora lo hacemos sobre s2

model.fit(X_train_s2,y_train_s2)
prediction=model.predict_proba(X_test)[:,1] ## me quedo con la probabilidad del si
prediction=pd.DataFrame(prediction, columns=['LR_s2'])
prediciones.append(prediction)

# ahora lo hacemos sobre s3

model.fit(X_train_s3,y_train_s3)
prediction=model.predict_proba(X_test)[:,1] ## me quedo con la probabilidad del si
prediction=pd.DataFrame(prediction, columns=['LR_s3'])
prediciones.append(prediction)

#ahora lo hacemos sobre s4

model.fit(X_train_s4,y_train_s4)
prediction=model.predict_proba(X_test)[:,1] ## me quedo con la probabilidad del si
prediction=pd.DataFrame(prediction, columns=['LR_s4'])
prediciones.append(prediction)

## aqui ya tenemos el modeloensemblers y ahcemos la media sobre los 4 baggings y tendriamos las prediciones medias que  me dacada una de los 4 modelos bagging

### ahora viene el momento de agregar las 4 predicciones

prediccion_bagging= pd.DataFrame((prediciones[1]["LR_s1"] +  prediciones[2]["LR_s2"]
                                  + prediciones[3]["LR_s3"] + prediciones[4]["LR_s4"] )/4)

#accuracy_score(y_test, prediccion_bagging) # aqui da error porque la predciocion que tengo es continua pero la de y_test es bionaria entonces tendramos que poner un punto de corte que seria > 0.5 = 1 y < 0.5 sea 0
## entonces vamos a binarizarlo:

from sklearn.preprocessing import Binarizer

# transformer= Binarizer(threshold=0.5).fit(prediccion_bagging)  # fit does nothing. # aqui lo que hace es transaformarlo en binario con el threshold de 0.5
# prediccion_bagging_binaria=pd.DataFrame(transformer.transform(prediccion_bagging))
# y_test.replace(('Si', 'No'), (1, 0), inplace=True)
# cm = confusion_matrix(y_test, prediccion_bagging_binaria) # creamos matriz de confusion (a traves de la binaria)
transformer = Binarizer(threshold=0.5).fit(prediccion_bagging)
prediccion_bagging_binaria = pd.DataFrame(
    transformer.transform(prediccion_bagging)
)

y_test.replace(('Si', 'No'), (1, 0), inplace=True)

cm = confusion_matrix(
    y_test["chd"].astype(int),
    prediccion_bagging_binaria.iloc[:, 0].astype(int)
)
accuracy_bagging=(cm[0,0]+cm[1,1])/(cm[0,1]+cm[1,1]+ cm[1,0]+cm[0,0]) # aqui vemos la prediccion 
print(accuracy_bagging) ## 0.7338, signidica que va mejor con 4 modelos

#######################################################################################
# ahroa es lo mismo que antes pero solo que hecho con bucle para asi poder aumentar el numero de baggings que hacer
#####################################################################################################
######################### bagging general con blucle !!!!!

import random
from sklearn.linear_model import LogisticRegression
import pandas as pd

# Supongamos que ya has dividido tus datos en conjuntos de entrenamiento y prueba
# X_train, X_test, y_train, y_test

# Numero de baggings
num_baggings = 100
s_size = 0.45  # Tamaño de cada muestra del bagging

# Inicializar listas para almacenar las predicciones de cada bagging
predicciones_baggings = []

for i in range(num_baggings):
    # Generar muestra aleatoria con reemplazo
    random.seed(2020 + i)  # Cambiando la semilla para cada iteración
    n = s_size * len(X_train)
    s = random.choices(range(len(X_train)), k=int(n))
    X_train_s = X_train.iloc[s]
    y_train_s = y_train.iloc[s]

    # Inicializar y ajustar el modelo de regresión logística
    model = LogisticRegression(random_state=1)
    model.fit(X_train_s, y_train_s)

    # Realizar predicciones en el conjunto de prueba
    prediction = model.predict_proba(X_test)[:, 1]
    prediction = pd.DataFrame(prediction, columns=[f'LR_s{i + 1}'])  # Cambiar el nombre de la columna para cada bagging
    predicciones_baggings.append(prediction)

# Calcular la predicción del bagging promediando todas las predicciones
prediccion_bagging = pd.DataFrame(sum(pred[f'LR_s{i + 1}'] for i, pred in enumerate(predicciones_baggings)) / num_baggings, columns=['Bagging'])

from sklearn.preprocessing import Binarizer

# transformer= Binarizer(threshold=0.5).fit(prediccion_bagging)  # fit does nothing.
# prediccion_bagging_binaria=pd.DataFrame(transformer.transform(prediccion_bagging))
# y_test.replace(('Si', 'No'), (1, 0), inplace=True)
# cm = confusion_matrix(y_test, prediccion_bagging_binaria)
transformer = Binarizer(threshold=0.5).fit(prediccion_bagging)
prediccion_bagging_binaria = pd.DataFrame(
    transformer.transform(prediccion_bagging)
)

y_test.replace(('Si', 'No'), (1, 0), inplace=True)

cm = confusion_matrix(
    y_test["chd"].astype(int),
    prediccion_bagging_binaria.iloc[:, 0].astype(int)
)
accuracy_bagging=(cm[0,0]+cm[1,1])/(cm[0,1]+cm[1,1]+ cm[1,0]+cm[0,0]) 
## aqui la prediccion con 50 baggings es peor que cuanod hemos tirado con 4
print(accuracy_bagging) ### 0.719 significa que va peor que copn  muchos mas mpdelosmodelos