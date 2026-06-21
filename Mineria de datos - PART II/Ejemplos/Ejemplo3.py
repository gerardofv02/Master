## librerias necesarias a importar
import numpy as np
import pandas as pd
import os
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose

directorio = 'C:/Users/gerar/Desktop/Master/Master/Mineria de datos - PART II/Ejemplos/Data'

os.chdir(directorio)

data = pd.read_excel('Compra Online.xlsx')
# print(data.dtypes)

# paso previo para remplazar M por un guion para posteriormente poder convertirlo a fecha
data['Tiempo'] = data['Tiempo'].str.replace('T','-').str.strip()
## covertimos la fecha que nos viene en int a fecha de dt
data['Tiempo'] = pd.to_datetime(data['Tiempo'], format='%Y-%m-%d-%H')
# print(data.dtypes)

s_online = data.set_index('Tiempo')[['carrefour','corte_ingles','dia','mercadona' ]]
s_dia = data.set_index('Tiempo')['dia']

# s_online.plot()
# plt.show()

# para verlo con mas profundidad, vemos las ultimas 24 horas
ultimodia = s_online[-24:]
ultimodia.plot()
plt.show()

## video 2: modelo multiplicativo descomposcion temporal
additive_descompose = seasonal_decompose(s_dia, model='miltiplicative',period=24) ## 24 porq son 24 horas por dia
plt.rc('figure',figsize=(16,12))
plt.rc('font',size=13)
fig = additive_descompose.plot()
plt.show()
# aqui se puede ver q no hya negativo ya q es multiplicativo 