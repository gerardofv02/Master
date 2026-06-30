## en este ejemplo usamos el modelo de datos serie_energetica para hacer un modelo autoarima
import pmdarima as pm
import numpy as np
import pandas as pd
import os
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.api import ExponentialSmoothing,SimpleExpSmoothing,Holt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import statsmodels.api as sm


directorio = 'C:/Users/gerar/Desktop/Master/Master/Mineria de datos - PART II/Ejemplos/Data'

os.chdir(directorio)

data = pd.read_excel('serie_energia.xlsx')
print(data.info())
data['Periodo'] = data['Periodo'].str.replace('M','-').str.strip()
data['Periodo'] = pd.to_datetime(data['Periodo'],format='%Y-%m')
S_data = data.set_index('Periodo')[['GWh']]
S_data = S_data['GWh']
print(S_data)

# representamos graficamente
S_data.plot()
plt.show()

## obsdervamos que tiene comportamiento periodico claro, enm verano es mayor.
# ppero tmb vemos que tiene una subida a partir de 202 por los costes de las placas fotovoltaicas y tmb existen subvenciones

#vamos a predecir la produccion:

train = S_data[:147]
test=S_data[147:]
plt.figure(figsize=(12,8))
plt.plot(train, label='Train',color='green')
plt.plot(test, label='test',color='yellow')
plt.legend()
plt.show()

#aumenmto significativo a ver si vemos que el modelo lo refeleje

#primero ajuste manual apra compararlo con el automatico

figure,(ax1,ax2) = plt.subplots(2,1,figsize=(12,8))
plot_acf(train, lags=30, ax=ax1) ## aqui calculamos las simples
ax1.set_title('Funcion autocorrelacion ACF de defunciones')

plot_pacf(train,lags=30,ax=ax2) ## aqui calculamos las parciales
ax2.set_title('Funcion autocorrelacion PACF de defunciones')
plt.tight_layout()
plt.show() 

#bviendo el autocorrelograma de arriba, acf, indica que existe una fuerte compojnmente estacionalm por eso vamos a hacer una diferencia de orden estacional

diferencias = train.diff(12)

## creamos autocorrelogramas de esta diferencias para hacer el modelo arima manual
# viendo el de arriba decrece de forma bastante significativa mientras que el de bajao vemos 2 puntos significativos al inciio y uno en la serie 12 y 13
# por lo tanto el modelo arima seria el siguiente: ARIMA(2,0,0)(0,1,1)

modelo_arima = sm.tsa.ARIMA(train,order=(2,0,0),seasonal_order=(0,1,1,12))
restultados = modelo_arima.fit()
print(restultados.summary())

# viendo los resultados vemos que los coeficientes del modelo son todos significativos (p valor = 0) y ademas el contraste de jungbos nos dice
# con este p valor que los residuos estan incorrelados con lo que parece un modelo adecuado
# sianalizamos los residuos:
restultados.plot_diagnostics(figsize=(12,8))
plt.show()

# vemops gráfica de abajo a al izquierda y arriba a la drecfha que tiene un comportamiento normal
# en la de abajo a la derechacemos que etán todas dentro de la banda
# en la superor izq estan todas al rededor de 0

#vemos quie el modelo es adecuado cojn lo que calculamos prediciones
prediciones = restultados.get_forecast(steps=12)
predi_test = prediciones.predicted_mean
intervalos_confianza = prediciones.conf_int()

plt.figure(figsize=(12,8))
plt.plot(intervalos_confianza['lower GWh'],label='UCL',color ='gray')
plt.plot(intervalos_confianza['upper GWh'],label='UCL',color ='gray')
plt.plot(prediciones.predicted_mean, label='Predicciones',color='blue') #datos de prediccion
plt.plot(test,label='TEST', color= 'yellow') # datos reales

plt.legend()
plt.show()

## se ven qq el garan aumento que ha habido se sale de los intervalos de confianza

## ahora probamos a ahcerlo automatico con autoarima a ver si nos da uin modelo mejor:
modelo_auto = pm.auto_arima(train,start_p=1,start_q=1,max_p=3,max_1=3,m=12,start_P=0,seasonal=True,d=0,D=1,trace=True,error_action='ignore',suppress_warnings=True,stepwise=True)
# le edicmos que nos enseñe el AIC para ver los modelos que ha probado:

# ARIMA(1,0,1)(0,1,1)[12] intercept   : AIC=1858.635, Time=0.23 sec -> El mejor es el que aparece arriba y tiene un AIC mas bajo que el resto
#  ARIMA(0,0,0)(0,1,0)[12] intercept   : AIC=1922.520, Time=0.01 sec
#  ARIMA(1,0,0)(1,1,0)[12] intercept   : AIC=1867.025, Time=0.20 sec
#  ARIMA(0,0,1)(0,1,1)[12] intercept   : AIC=1901.971, Time=0.11 sec
#  ARIMA(0,0,0)(0,1,0)[12]             : AIC=1951.928, Time=0.01 sec
#  ARIMA(1,0,1)(0,1,0)[12] intercept   : AIC=1881.703, Time=0.08 sec
#  ARIMA(1,0,1)(1,1,1)[12] intercept   : AIC=1859.859, Time=0.32 sec
#  ARIMA(1,0,1)(0,1,2)[12] intercept   : AIC=1860.301, Time=0.48 sec
#  ARIMA(1,0,1)(1,1,0)[12] intercept   : AIC=1858.721, Time=0.21 sec _> Este tmb es muy similare
#  ARIMA(1,0,1)(1,1,2)[12] intercept   : AIC=1860.853, Time=0.75 sec
#  ARIMA(1,0,0)(0,1,1)[12] intercept   : AIC=1865.897, Time=0.16 sec
#  ARIMA(2,0,1)(0,1,1)[12] intercept   : AIC=1860.151, Time=0.32 sec
#  ARIMA(1,0,2)(0,1,1)[12] intercept   : AIC=1859.897, Time=0.20 sec
#  ARIMA(0,0,0)(0,1,1)[12] intercept   : AIC=1924.336, Time=0.04 sec
#  ARIMA(0,0,2)(0,1,1)[12] intercept   : AIC=1886.294, Time=0.17 sec
#  ARIMA(2,0,0)(0,1,1)[12] intercept   : AIC=1858.676, Time=0.23 sec -> Este modelo es el nuestro manual, que las diferencias son unas centesimas con el mejor con lo q no ibamos mal encaminados
#  ARIMA(2,0,2)(0,1,1)[12] intercept   : AIC=inf, Time=0.35 sec
#  ARIMA(1,0,1)(0,1,1)[12]             : AIC=1860.531, Time=0.15 sec

print(modelo_auto.summary())

##viendo este modelo, vemos los caoficientes y es un modelo con constante y el pvalor es muy bajo tmb de los coeficientes del modelo q son todos significativos
# segun vemos el contraste de   jung-box para ver si son incorrelados vemos que tenemos un constraste altisimo del 90 con lo q los residuos estan incorrelados

best_arima = sm.tsa.ARIMA(train,order=(2,0,0),seasonal_order=(0,1,1,12))
restultados_best = best_arima.fit()
print(restultados_best.summary())
restultados_best.plot_diagnostics(figsize=(12,8))
plt.show()

## representandolo graficamente vemos lo mismo q lo anterior

## viendo las predciiones vemos que son muy similiaes alk anterior modeloy vemos que no hya casi diferencia

prediciones_A = restultados_best.get_forecast(steps=12)
predi_test = prediciones_A.predicted_mean
intervalos_confianza_A = prediciones_A.conf_int()

plt.figure(figsize=(12,8))
plt.plot(intervalos_confianza_A['lower GWh'],label='UCL',color ='gray')
plt.plot(intervalos_confianza_A['upper GWh'],label='UCL',color ='gray')
plt.plot(prediciones_A.predicted_mean, label='Predicciones',color='blue') #datos de prediccion
plt.plot(test,label='TEST', color= 'yellow') # datos reales

plt.legend()
plt.show()