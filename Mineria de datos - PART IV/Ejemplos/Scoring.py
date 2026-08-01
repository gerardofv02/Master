## Fases de los datos

## Fase de analisis
# 1 -  Seleccion  de datos de clientes de sus caracteristicas y de si resultaron impagados o no
        ## - Depuracion de datos
        ## - Definicion de la vairable objetivo
        ## - Seleccion y transformacion de variables explicativas
# 2 - Estimación de modelos de probabilidad multivariante y construcciond e tarjetas de puntuacion (regresion logistica) para interpretar los resultados
# 3 - Sesgo - Omision de variables relevantes relacionadas con otras variables explicativas. Errores de medida. Inferencia de denegados (sesgo de autoseleccion)
# 4 - VBalidación del modelo. La muestra se suele dividir en dos (train (80%) y test (20%)) para verificar que se ha ehcho correctamente
# 5 - Obtención del modelo final - Elgir cual ha sido el mej0or modelo

## Seleccion de vairbales explicativas

# Basicamnete quitar variables que no nos sirvan de nada



import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency, f_oneway
from optbinning import Scorecard, BinningProcess, OptimalBinning
from optbinning.scorecard import plot_auc_roc, plot_cap, plot_ks, ScorecardMonitoring

import sklearn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, balanced_accuracy_score
import os

## cargamos datos: 

os.chdir('C:/Users/gerar/Desktop/Master/Master/Mineria de datos - PART IV/Ejemplos/Data')

aceptados = pd.read_csv('Aceptados.csv')

rechazados = pd.read_csv('Rechazados.csv')

nuevos = pd.read_csv('Nuevos.csv')

#analizamos variables.
print(aceptados.info())

print(aceptados['y'].value_counts())
# aqui vemos que unos 630 han sido con valor 0 que son buenos clientes mientras que 156 son malos, ahora los popnjemos en modo porcentajke:
print(aceptados['y'].value_counts(normalize=True))

# guardamos los valores en distintos variables de 0 y 1 para dsps:

y_0 = aceptados['y'].value_counts(normalize=True)[0]
y_1 = aceptados['y'].value_counts(normalize=True)[1]

# comenzamos variables con variables discretas:

aceptados.describe(include='object')