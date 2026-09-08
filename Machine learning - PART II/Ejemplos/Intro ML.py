## empezamos con el ejemplo del titanic modificado 

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

sns.set_style('darkgrid')
np.set_printoptions(precision=2) 
warnings.filterwarnings("ignore")

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
import os
os.chdir('C:/Users/gerar/Desktop/Master/Master/Machine learning - PART I/Data')
""" Semilla """
seed = 99

## ALGUNAS UTILIDADES SOBRE EL MANEJO DE DATOS SEGURAMENTE SEA REDUNDANTE CON LO VISTO ANTERIORMENTE POR VOSOTROS

data = pd.read_excel("titanic.xlsx")
#data = pd.read_excel("titanic.xlsm")

## se quiere predecir si se sobrevive o no al titanic (desde el resto de variables)

##comenzamos el analiss
data = data.drop(data.columns[0], axis=1) # eliminamos la primera columna que no tiene sentido

 ## data.shape me da un vector (tuple) de dos dimensiones con las filas y las columnas del dataframe

print(f'Número de filas: {data.shape[0]}, Número de columnas:{data.shape[1]}') 
print(data.head())
print(data.dtypes)
####
####
# Crear un histograma utilizando Seaborn
plt.figure(figsize=(10, 6))
sns.histplot(data=data, x='Fare', hue='Embarked', bins=30, kde=True)

# Añadir etiquetas y título
plt.xlabel('Tarifa (Fare)')
plt.ylabel('Frecuencia')
plt.title('Histograma de Tarifas según el Puerto de Embarque')

# Mostrar el gráfico
plt.show()

# Crear el boxplot
plt.figure(figsize=(10, 6))
sns.boxplot(x='Survived', y='Fare', data=data)
plt.title('Boxplot de Fare según la supervivencia')
plt.xlabel('Survived')
plt.ylabel('Fare')
plt.show()


# Crear el boxplot
plt.figure(figsize=(12, 8))
sns.boxplot(x='Survived', y='Fare', hue='Sex', data=data)
plt.title('Boxplot de Fare según la supervivencia y el género')
plt.xlabel('Survived')
plt.ylabel('Fare')
plt.legend(title='Sex', loc='upper right')
plt.show()

##vemos cantidad de nulos
###########################################################################
## Paso 1 ## Missing
## Paso 1. vemos cuantos missing tenemos en cada variable ##
data.isnull().sum() 
## como tenemos la variable cabina con muchos datos eprdidos, se tendria que eliminar. P0ero en lugar de ello,vamos a usarla como si es dato perdido o no, entonces modificamos la variable

import seaborn as sns
# Identificamos los missing values visualmente
sns.heatmap(data.isnull(), cbar=False)
## vemos que edad, cabin y Embarked tienen valores perdidos. Cabin tiene muchos valores perdidos
## df.fillna(df.mean(), inplace=True)

###########################################################################
## Paso 2 Codificacion, Imputación, o eliminacion de datos perdidos
## en ocasiones la información relevante es si se ha perdido un dato o no
## en otros casos merece la pena imputar su valor mientras que otras veces merece la pena eliminarlo

###############################################
## 2.1 Modificacion de la variable Cabin. Porque Hacemos esto?

#Se llenan los valores nulos (NaN) de la columna 'Cabin' de data con el valor 0.
data['Cabin'] = data['Cabin'].fillna(0)
#Nueva columna hasCabin, que toma valores binarios 0 y 1, en función de si el pasajero tiene o no un número de cabina.
# La función lambda define que si el valor de "Cabin" es 0 el valor de la columna hasCabin toma valor 0, 
# en caso contrario toma  valor 1.
data['hasCabin'] = data['Cabin'].apply(lambda x: 0 if x==0 else 1)

# tabla_frecuencias = pd.crosstab(data['hasCabin'], data['Survived'])