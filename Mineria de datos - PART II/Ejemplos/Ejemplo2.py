## librerias necesarias a importar
import numpy as np
import pandas as pd
import os
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.api import ExponentialSmoothing,SimpleExpSmoothing,Holt

directorio = 'C:/Users/gerar/Desktop/Master/Master/Mineria de datos - PART II/Ejemplos/Data'

os.chdir(directorio)

data = pd.read_excel('Cordoba.xlsx')
# print(data.dtypes)

# paso previo para remplazar M por un guion para posteriormente poder convertirlo a fecha
data['Fecha'] = data['Fecha'].str.replace('M','-').str.strip()
## covertimos la fecha que nos viene en int a fecha de dt
data['Fecha'] = pd.to_datetime(data['Fecha'], format='%Y-%m')
# print(data.dtypes)

# creamos ahora los dos series y el df
V_ESP =  data.set_index('Fecha')['R_España']
V_EXT = data.set_index('Fecha')['R_Extranjero']
s_cordoba = data.set_index('Fecha')[['R_España','R_Extranjero' ]]

# s_cordoba.plot()
# plt.show()

# si queremos representar solo 1 serie:
# V_ESP.plot()
# plt.show()

#VIDEO 2, EJEMPLO SOBRE DESCOMPOSICION TEMPORAL. Al tener valores 0 en la pandemia, usamos el modelo aditivo
# para el ejemplo 3 se va a usar el multiplicativo
additive_descompose = seasonal_decompose(V_ESP, model='additive',period=12)
# en este atributo nos hemos guardado mucha informacion
# print(additive_descompose)
# representamos graficamente
# plt.rc('figure', figsize=(16,12))
# plt.rc('font',size = 13)
# fig = additive_descompose.plot()

# plt.show()

# si dela tributo creoado antes nos queremos obtener los coeficientes de estacionalidad, se hace de la siguiente manera
print(additive_descompose.seasonal[:12]) ## son 12 los meses en un año y vemos llos primeros q trenemos
## aqui se observa q el mayor es 8642 que corresponde al mes de mayo. esto significa q en cordoba en este mes hay 8642 
# más viajeros que la media

#mientras que en enero hay 11800 viajeros menos q la media.

#ahora representamos la serie graficamente con la tendencia y la serie ajustada estacionalmente

s_ajustada = V_ESP-additive_descompose.seasonal

plt.figure(figsize=(12,8))
#serie original
plt.plot(V_ESP,label='Datos',color='gray')
#ahora añadimos tendencia
plt.plot(additive_descompose.trend,label='Tendencia',color='blue')

#Ahora estacianalmente ajustada
plt.plot(s_ajustada,label='Estacionalmente ajustada',color='red')

#ahora nombres y cosas de figura
plt.xlabel('Fecha')
plt.ylabel('Viajeros españoles')
plt.title('Viajerps')
plt.legend()
plt.show()

##añadimos otro graico que puede ser interesante
## extrameos los años de cada fecha
s_cordoba['Año'] = s_cordoba.index.year

#creamos un graficocon distintos colores para cada año

plt.figure(figsize=(12,8))
sns.lineplot(x=s_cordoba.index.month,y=s_cordoba.R_España,hue=s_cordoba['Año'])
plt.xlabel('Mes')
plt.ylabel('Estacionalidad')
plt.title('Grafico por año')
plt.legend(title='Año',loc='upper left',bbox_to_anchor=(1,1))
plt.show()

## VAMOS A UTILIZAR EL MODELO PREDICTIVO DE SUAVIZADO (DE FORMA ADITIVA) DE HOLT-WINTERS
train = V_ESP[:283]
test = V_ESP[283:] #reservamos el ultimo año

plt.figure(figsize=(12,8))
plt.plot(train,label='train',color='green')
plt.plot(test,label='Test',color='yellow')
plt.xlabel('Mes')
plt.ylabel('Estacionalidad')
plt.title('Grafico por año')
plt.legend()
plt.show()
# mostramos los valores originales diviidos por train y test

model1 = ExponentialSmoothing(train,seasonal_periods=12,trend='add',
                              seasonal='add', initialization_method='estimated'
                              ).fit() # aditiva devido a que hay 0 y no se puede usar multiplicativa

fcast1 = model1.forecast(12) # el ultimo año que hemos dejado de test

plt.figure(figsize=(12,8))
plt.plot(train,label='train',color='green')
plt.plot(test,label='Test',color='yellow')
plt.plot(model1.fittedvalues,label='suavidazo',color='blue')
plt.plot(fcast1,label='predict',color='red')
plt.xlabel('Mes')
plt.ylabel('Estacionalidad')
plt.title('Grafico por año')
plt.legend()
plt.show()

## predicciones:

print(fcast1)
# podemos hacer una tabla donde vengan todos los valores estso tmb el alpha beta,..., valores inidicels, gamma,...
from tabulate import tabulate
headers = ['Name','Param','value','optimized']
table_str = tabulate(model1.params_formatted,headers,tablefmt='fancy_grid')
print(table_str)

## level -> m sub t
## seaon -> coeficiente de estacionalidad

print(model1.level)
print(model1.trend)

## TEMA 2 -> PARA MODELIZACIÓN ARIMA
# ahora en este ejemplo vamos a calcular las autocorrelaciones
## para importanralas:
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf


figure,(ax1,ax2) = plt.subplots(2,1,figsize=(12,8))
plot_acf(train, lags=30, ax=ax1) ## aqui calculamos las simples
ax1.set_title('Funcion autocorrelacion ACF de defunciones')

plot_pacf(train,lags=30,ax=ax2) ## aqui calculamos las parciales
ax2.set_title('Funcion autocorrelacion PACF de defunciones')
plt.tight_layout()
plt.show()


## aqui se puede ver que la autocrrelacion simple se ve que tiene comportamiento periodico ya que se puede ver
## que se repite el patrón mientras que en el parcial
## vemos que tenemos en el retardo 12 que es muy importante ya que para retardos periodicos, los valores influyen mucho
## como estamos viendo los viajeros en un año (12 meses) al ser 12 meses el retardo que encontramos en la posción 12
## es muy grande

## TEMA 2: Procesos integrados
## vemos ahora el modelo arima con datos estacionarios

## realizamos la diferencia estacional ya que tenemos muchas diferencias entre los meses de enero y meses de mayo

diferencias = train.diff(12)# calculamos las diferencias

# grafica
plt.figure(figsize=(12,6))
plt.plot(diferencias)
plt.show()

## vemos que la media cambia mucho solo hay un poco distinto en los valores de la pandemia como es nomral
## pero se puede obsrevar q es una media muy cosntante

## ahora representamos los valores de autocorrelacion simple yu la parcial ¡
diferencias = diferencias.dropna()
figure1,(ax11,ax22) = plt.subplots(2,1,figsize=(12,8))
plot_acf(diferencias, lags=30, ax=ax11) ## aqui calculamos las simples
ax11.set_title('Funcion autocorrelacion ACF de defunciones (diferenciada)')

plot_pacf(diferencias,lags=30,ax=ax22) ## aqui calculamos las parciales
ax22.set_title('Funcion autocorrelacion PACF de defunciones(diferenciada)')
plt.tight_layout()
plt.show()

## ya nos tenemos curvas tan grandes debido a que hemos eliminado la estacionalidad tan fuerte
## decrece de forma rapida pero mejor, y tenemos la 1 y la 12 muy fuertes
## entonces visto esto el modelo que ajustariamos seria difrernciacion estacional (no regular) y el primer 1 viene para modelizar
## los valores posteriors del 1 y el segundo 1 viene del 12 para modelizar las siguientes