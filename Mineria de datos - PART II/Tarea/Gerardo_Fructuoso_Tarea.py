## librerias necesarias a importar
import numpy as np
import pandas as pd
import os
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.api import ExponentialSmoothing,SimpleExpSmoothing,Holt
from tabulate import tabulate
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import statsmodels.api as sm
import pmdarima as pm

## una vez tenemos los imports hechos, tenemos que realizar el import y el tratamiento de los datos

directorio = 'C:/Users/gerar/Desktop/Master/Master/Mineria de datos - PART II/Tarea/Data'
os.chdir(directorio)
data = pd.read_excel('Media Temperaturas 2012-2024 Madrid.xlsx',header=None)
# print(data)
# ahora con estos datos vamos a darle formato fecha a estas dos primeras ccolumnas conviertiendolo en una única columna
meses = {
    'Enero': '01',
    'Febrero':'02',
    'Marzo':'03',
    'Abril':'04',
    'Mayo':'05',
    'Junio':'06',
    'Julio':'07',
    'Agosto':'08',
    'Septiembre':'09',
    'Octubre':'10',
    'Noviembre':'11',
    'Diciembre':'12'
}
data['Fecha'] = (data[0].astype(str) + '-' + data[1].map(meses))
# print(data)
data['Fecha'] = pd.to_datetime(data['Fecha'], format='%Y-%m')
data['Temp. Media'] = data[2].str.replace(',', '.').astype(float)
data = data.drop([0,1,2], axis=1)
data = data.set_index('Fecha')
print(data)

data.plot()
plt.show()

# vamos a representar un único año apra ver el comportamiento
data_anno = data[-12:]
data_anno.plot()
plt.show()

multiplicative_descompose = seasonal_decompose(data, model='multiplicative',period=12) # ponemos periodo de 12 ya que son los meses
# print(multiplicative_descompose)
plt.rc('figure', figsize=(16,12))
plt.rc('font',size = 13)
fig = multiplicative_descompose.plot()
plt.show()

print(multiplicative_descompose.seasonal[-12:])
 
train = data[:-12]
test = data[-12:]
print(train, test)

## procedemos con los modelos suavizados

model_simple = SimpleExpSmoothing(train,initialization_method='estimated').fit() ## simple
print(model_simple.summary())

model_holt = Holt(train, initialization_method='estimated').fit()
print(model_holt.summary())
model_holt_winters = ExponentialSmoothing(train,seasonal_periods=12,trend='mul',
                              seasonal='mul', initialization_method='estimated'
                              ).fit() ## multiplicativo -> holt_winters
print(model_holt_winters.summary())

f_cast = model_holt_winters.forecast(12)

plt.figure(figsize=(12,8))
plt.plot(train,label='train',color='green')
plt.plot(test,label='Test',color='yellow')
plt.plot(model_holt_winters.fittedvalues,label='suavidazo',color='blue')
plt.plot(f_cast,label='predict',color='red')
plt.xlabel('Mes')
plt.ylabel('Temp. Media')
plt.title('Grafico por año')
plt.legend()
plt.show()

print(f_cast)

## Ahora vamos a calcular los correlogramas

figure,(ax1,ax2) = plt.subplots(2,1,figsize=(12,8))
plot_acf(train, lags=30, ax=ax1) ## aqui calculamos las simples
ax1.set_title('Funcion autocorrelacion ACF de temperaturas')

plot_pacf(train,lags=30,ax=ax2) ## aqui calculamos las parciales
ax2.set_title('Funcion autocorrelacion PACF de temperaturas')
plt.tight_layout()
plt.show() 


diferencias = train.diff(12)# calculamos las diferencias

# grafica
plt.figure(figsize=(12,6))
plt.plot(diferencias)
plt.show()

diferencias = diferencias.dropna()
figure1,(ax11,ax22) = plt.subplots(2,1,figsize=(12,8))
plot_acf(diferencias, lags=30, ax=ax11) ## aqui calculamos las simples
ax11.set_title('Funcion autocorrelacion ACF de temperaturas (diferenciada)')

plot_pacf(diferencias,lags=30,ax=ax22) ## aqui calculamos las parciales
ax22.set_title('Funcion autocorrelacion PACF de temperaturas(diferenciada)')
plt.tight_layout()
plt.show()

modelo_arima = sm.tsa.ARIMA(train, order= (1,0,0), seasonal_order=(0,1,1,12))
resultados = modelo_arima.fit()
print(resultados.summary())

resultados.plot_diagnostics(figsize=(12,8))
plt.show()

modelo_auto = pm.auto_arima(train,start_p=1,start_q=1,max_p=3,max_1=3,m=12,start_P=0,seasonal=True,d=0,D=1,
                            trace=True,error_action='ignore',suppress_warnings=True,stepwise=True)

best_arima = sm.tsa.ARIMA(train,order=(1,0,0),seasonal_order=(0,1,2,12),trend='t')
restultados_best = best_arima.fit()

prediciones_A = restultados_best.get_forecast(steps=12)
predi_test = prediciones_A.predicted_mean
intervalos_confianza_A = prediciones_A.conf_int()
print(restultados_best.summary())

plt.figure(figsize=(12,8))
plt.plot(intervalos_confianza_A['lower Temp. Media'],label='UCL',color ='gray')
plt.plot(intervalos_confianza_A['upper Temp. Media'],label='DCL',color ='gray')
plt.plot(prediciones_A.predicted_mean, label='Predicciones',color='blue') #datos de prediccion
plt.plot(test,label='TEST', color= 'yellow') # datos reales

plt.legend()
plt.show()

plt.figure(figsize=(12,8))
plt.plot(train,label='train',color='green')
plt.plot(test,label='Test',color='yellow')
plt.plot(prediciones_A.predicted_mean,label='predict',color='red')
plt.xlabel('Mes')
plt.ylabel('Temp. Media')
plt.title('Grafico por año')
plt.legend()
plt.show()

plt.figure(figsize=(12,8))
plt.plot(train,label='train',color='green')
plt.plot(test,label='Test',color='yellow')
plt.plot(prediciones_A.predicted_mean,label='predict_arima',color='red')
plt.plot(f_cast,label='predict_holt_winters',color='pink')
plt.xlabel('Mes')
plt.ylabel('Temp. Media')
plt.title('Grafico por año')
plt.legend()
plt.show()