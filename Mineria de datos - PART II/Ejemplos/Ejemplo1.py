## librerias necesarias a importar
import numpy as np
import pandas as pd
import os
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns

directorio = 'C:/Users/gerar/Desktop/Master/Master/Mineria de datos - PART II/Ejemplos/Data'

os.chdir(directorio)

data = pd.read_excel('Defunciones.xlsx')
# print(data.dtypes)
## covertimos la fecha que nos viene en int a fecha de dt
data['Año'] = pd.to_datetime(data['Año'], format='%Y')
# print(data.dtypes)
#asignamos la fecha al id ya que es unica
s_defun = data.set_index('Año')[['Mujeres', 'Hombres']]
# print(s_defun)

# ahora representamos las dos series:
# s_defun.plot()
# plt.title('Defunciones anuales')
# plt.xlabel('Fecha')
# plt.ylabel('Defunciones')
# plt.show()

##las funciones de modelos predictivos trabajn sobre el tipo de dato llamado series, esto es cuando es un vector con un 
#unico valor. por ejemplo, si quitarmos los hombres de df y nos quedamos con las mujeres, seria un tipo series:
defun_m = s_defun['Mujeres']
# print(type(defun_m)) ## Series

## video 1 de suavizado 
# vamos a realizar la funcion de suiavizado a estos datos ya que en este primer ejemplo de suavizado los datos de nodeben
#tener valores estacionales (q por ejemplo no sean valores q sean por dia para divir entre 24 h ...)

# modulos:
from statsmodels.tsa.api import ExponentialSmoothing,SimpleExpSmoothing,Holt

## tenemos que dividir la series en 2 variables de ficheros . en train y en test.
# apra ello en train nos llevaremos un 90% mientras q a teste un 10% . en este ejemplo dejaremos para test los ultimos 5 años

train = defun_m[:42]
test = defun_m[42:]

# vamos a represetnarlos en train y test:
plt.figure(figsize=(12,8))

plt.plot(train,label='Train',color='gray')
plt.plot(test,label='Test_real',color='yellow')
plt.legend()
plt.xlabel('Fecha')
plt.ylabel('Defun')

plt.show()

# aplicando el suavizado exponencial simple
model = SimpleExpSmoothing(train,initialization_method='estimated').fit()
fcast = model.forecast(5) ## 5 años reservados para el test

##representamos las predicciones:
plt.figure(figsize=(12,8))
plt.plot(train,label='Train',color='gray')
plt.plot(test,label='Test_real',color='yellow')
plt.plot(model.fittedvalues,label='suavizado',color='blue')
plt.plot(fcast,color='red') ## estas son las predciones
plt.legend()
plt.xlabel('Fecha')
plt.ylabel('Defun')

plt.show()

# este modelo no da muy buenos resultados. revisamos:
print(model.params_formatted)
##### ESTE MODELO NO SE UTILIZA CASI NUNCA YA QUE AUNQ NO TENGA ESTACIONALIDAD, SUELE TENER CAMBIOS EN LA TENDENCIA.

## POR ESTA RAZON SE EMPLEA EL MODELO AISLODA DOBLE DE HOLT CON LOS Q NO TIENEN ESTACIONALIDAD

model1 = Holt(train, initialization_method='estimated').fit()

fcast1 = model1.forecast(5)
print(model1.params_formatted)

plt.figure(figsize=(12,8))
plt.plot(train,label='Train',color='gray')
plt.plot(test,label='Test_real',color='yellow')
plt.plot(model.fittedvalues,label='suavizado_simple',color='blue')
plt.plot(model1.fittedvalues,label='suavizado_host',color='green')
plt.plot(fcast,label='predict_simple',color='red') ## estas son las predciones
plt.plot(fcast1,label='predict_host',color='purple') ## estas son las predciones
plt.legend()
plt.xlabel('Fecha')
plt.ylabel('Defun')

plt.show()

# este modelo como se observa viene con mejor prediccion pero al haber tenido valores atipicos por el covid,
# es normal q no lo haya hecho al 100% correcto

# vemos predicciones

print(fcast1)

##ahora vamos a ahcer una variacion del modelo holt dandole una curva para predecir los picos
model2 = Holt(train, damped_trend=True,initialization_method='estimated').fit() #funcion damped_trend=true para hacer el giro

fcast2 = model2.forecast(5)
plt.figure(figsize=(12,8))
plt.plot(train,label='Train',color='gray')
plt.plot(test,label='Test_real',color='yellow')
plt.plot(model2.fittedvalues,label='suavizado_host',color='green')
plt.plot(fcast2,label='predict_host',color='purple') ## estas son las predciones
plt.legend()
plt.xlabel('Fecha')
plt.ylabel('Defun')

plt.show()