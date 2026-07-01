## librerias necesarias a importar
import numpy as np
import pandas as pd
import os
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.api import ExponentialSmoothing,SimpleExpSmoothing,Holt
# import statsmodels as sm

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
s_cordoba = data.set_index('Fecha')[['R_España','R_Extranjero']]

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
plt.rc('figure', figsize=(16,12))
plt.rc('font',size = 13)
fig = additive_descompose.plot()

plt.show()

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

## tema 2 video 4 modelo autoregresivo
# generaliza la idea de regresion para re0presentar  la relacion entre una variable de la serie y las anteriores. Este seria el modelo AR y tiene q venir con el valor p
# es un modelo general y con constante 
## Modelo de medias moviles sirve para representar series qque tienen una memoria larga ya que su funcioin ACF decrece de forma exponencial. Este sería el modelo
# MA y tiene como valor q

## tema 2 video 5 modelo arima estacional
# generaliza la idea de regresion para re0presentar  la relacion entre una variable de la serie y las anteriores.
## Se tiene qque convertir una serie con estacionalidad en estacionaria mediante las diferencias de orden s siendo s el periodo de la serie
# El modelo arima se presenta de la siguiente forma ARIMA(p,d,q)(P,D,Q)
##Los modelos arima de tipo estacional, por un lado esta la parte regular (dependencias no estacionales) (p,d,q)
##d = diferenciacion a nivel 1 para que sea estacionaria
##p = diferencias que queden para un modelo autoregresivo
##q = diferencias que queden para un modelo de medias moviles
##Luego tenemos la parte de comportamiento periódico (P,D,Q)
##D = Diferencia de orden 12 (este sera igual a 1 pero estará multiplicado por s)
##P= Diferenciar con la parte autoregresiva estacional
## Q = Diferenciar con la parte de medias moviles
# eSTOS MODELOS ARIMA TIENEN QUE SER SUPER SENCILLOS PORQUE SI NO SE CONVERTIRIA EN ALGO MUY COMPPLEJO.
## EJEmplo: ARIMA(1,1,0)(1,0,0)12
# esto es un modelo arima de ejemplo. Aqui podemos ver que hemos hecho diferenciacion de nivel 1 en la parte regular, no en la estacional ()en d pero no en D)
# Esto significa que puede estar cambiando mucho en el tiempo en periodos muy grandes de tiempo, entonces para hallar la meida constante nos sirve solo con la diferenciacion
# en la parte regular

# Luego este modelo tiene un 1 en AR reguilar (p) y uno tmb en la aprte estacional (P)
# en la imagen dentro de la carpeta se puede observar como está creada la formula


# Por ejemplo en este ejemplode cordoba hariamos asi el modelo ARIMA:
#vamos a obnnservar antes de anda   los correlogramas de la serie sin diferenciar:

# en este caso el modelo arima seria: ARIMA()()

figure,(ax1,ax2) = plt.subplots(2,1,figsize=(12,8))
plot_acf(train, lags=30, ax=ax1) ## aqui calculamos las simples
ax1.set_title('Funcion autocorrelacion ACF de defunciones')

plot_pacf(train,lags=30,ax=ax2) ## aqui calculamos las parciales
ax2.set_title('Funcion autocorrelacion PACF de defunciones')
plt.tight_layout()
plt.show() 

## aqui en la grafica de arribna de acf se puede ver que cada 12 tiene una subida con lo que podemos ver que es una serie estacional
## tambien se puede ver en la rafica de abajo de pacf yu se ve mas claro porque tiene de retardo que va hacia abajo esto se debe a que los que fueron en el mes de mayo
## se parece mucho a los que fueron en el mes de mayo del año anterior y esta relacion de tippo periodico es muy impornate para modelizarla e incluirlo

## ahora vamos a ver que ocurre si se diferencia de forma de orden 12:
diferencias = train.diff(12)# calculamos las diferencias
plt.figure(figsize=(12,6))
plt.plot(diferencias)
plt.show() 

# se puede ver que es una serie que tiene una media constante alrededor del 0 salvo la parte del covid

#para ajustar el modelo adirma lo primero que tenemos que hacer e ajustar las autocorrelaciones de la serie diferenciarda
#seria de la sigueitne fdorma:
diferencias = diferencias.dropna()
figure1,(ax11,ax22) = plt.subplots(2,1,figsize=(12,8))
plot_acf(diferencias, lags=30, ax=ax11) ## aqui calculamos las simples
ax11.set_title('Funcion autocorrelacion ACF de defunciones (diferenciada)')

plot_pacf(diferencias,lags=30,ax=ax22) ## aqui calculamos las parciales
ax22.set_title('Funcion autocorrelacion PACF de defunciones(diferenciada)')
plt.tight_layout()
plt.show()

## aqui se puede ver que ha camvbiado sobretodo el acf, pero siguen habiendo muchas autorcorrelaciones distintas de 0
# en el parcial no hya tantsos cambios

##AQUI PARA EL MODELO VEMOS LOS IGUEITEN. tenemos que ajustar el siguiente modelo: tiene qqque tener un p = 1 o un q = 1. pero normalmente en la aprte regfular suele mejor los
# autoregresivos IMPORTANT.  y en la aprte estacional un P = 1 o un Q = 1  Por eso el primer modelo que hacemos como modelo poasible seria el sigueinte:
# ARIMA(1,0,0)(0,1,1)12 aunque tenemos que ajustar yu ver si es mas correcto que otros

## TEMA 2 EP 6/7: Box-jenkins (para hacer autoarima manual)
# sirve para seguir unos pasos para tener un modelo ajustado y para que así nos sea mas facil hacer el modelo arima
#pasos:
# Paso1: identificaciojn del modelo
# Paso2: Estimación
# Paso3: Pruebas del modelo -> SI no son adecuadas, habriua que volver al paso 1
# Paso4:Predicción


#vamos a ver el autocorrelograma de la serie diferencia (lo q hemos ehchoa ntes)
#  se puede ver en el acf que decrece de una forma bastatnte rapida
# y se puede ver en el pacf que tenemos una autocorrelacion de orden 12 y una de orden 1. el modelo se tiene que ahcer de la forma mas simple incluyuyenbdo las dependencias

# entonces el mocelo seria ARIMA(1,0,0)(0,1,1)12. El 1 del medio de la parte estacional es porque hemos hechomuna diferenciacion estacional
# elñ ultimo 1 es por el valor de autorrelacion de pacf de la posi 12 (estya hacia abajo) y le 1 de la iozquierda es por el valor 1 de la aprte del valor 1

# ahora para ajustarlo en python se hace asi:
import statsmodels.api as sm
modelo_arima = sm.tsa.ARIMA(train, order= (1,0,0), seasonal_order=(0,1,1,12))
resultados = modelo_arima.fit()
print(resultados.summary())

## de aqui podemos sacar los acoeficientes. de la parte de AR es 0.86 mientras que de la MA es de -0.77
## para hacer los calculos y sacar Xt con la funcion. se tiene que ahcer como la imagen qque se enceutnra en la carpeta
## como podemos ver que el p valor es muy pequeño, rechazamos que sean 0 con lo que son significativos

## TEMA 2 PARTE 8 DIAGNOSIS

# REQUISITTOS: INCORRELADOS Y DE PEQUEÑO TAMAÑO

##para calcular los residuos del modelo:
resultados.plot_diagnostics(figsize=(12,8))
plt.show()

# viendo la grafica de abajo derecha:
#estos sin los limites de autoconfianza que aparecen en la grafica de autocrrelacion. las limities superior e infereior. si todas estan significa que las autocorrelaciones son 0
# hay alguna que szale un poco, pero depende estas bandas mucho del tamaño muestral, si tengo una serie con 200 valores, las bandas serian muy exstrechas.

# entonces con q salgan alguna un poco no pasa nada

## tambien se puede ver que la media esta alrededor de 0 (como se ve en la esquina superior izquierda de la grafica)

## también se tiene que ver que tienen que tener distribuicion normal en las otras dos gráficas, en lak de abajo a al izquierda, se ve que se ajusta bastante a una recta salvo
# un apr de valores (pandemia)
# en la grafica de arriaba  ala derecha el histograma, se puede ver que la nroamlkk esta en verde y lo naranja se ajusta tmb bastante bien a esta verde

# ahroa vemos el contrsate:
#en lka tablak que hemos printado eantes , se puede ver el contraste de JQ (en este caso 0,93 con un pvalor de 0.34 y es muy alto (mayor de 0.05)) con lo que 
# estasmos aceptando que los residuoios estan incorrelados con lo que no podriamos rechazarlo, pero seguimos con el ejemplo


## en esta tabla tmb se pueden ver los valores AIC y BIC (se tiene que coger el modelo con menor AIC)
# en esta tabla ademas de tener la L (log de la insimuilitud), tenemos el AIC y el BIC

# cuanto menor sea el AIC y menor sea el BIC, mejor sera el modelo. todos tienen un valor muy similar

#entonces se hace lo siguiente:

# PRimer termino de la definicion del AIC es el que realmente mide el desajuste, su valor aumenta cuando peor es el ajuste
# El AIC sigue siendo principiop de parsimonia por lo que hay q coger el modelo con menor AIC (pero este valor aumenta si el numero de parametros k aument tmb)


## TEMA 2 EP 9: PREDICCION
# SERIE DE TIPO PERIDICOS -> SE SUELE PREDECIR UN POCO MAS
# para la cantidad de predicciones se indica de la siguiente forma:
prediciones = resultados.get_forecast(steps=12) # aqui en resutlados estan los datos del modelo #calculamos un año siguietne al ultimo mes
predi_test = prediciones.predicted_mean 
print(predi_test)
## aqui nos salen los valores de las predicciones que nos salen desde agosto hasta julio
# vamos a verlo graficamente:
plt.plot(train,label='Train', color = 'gray')
plt.plot(test,label='TEST', color= 'yellow')
plt.plot(prediciones.predicted_mean, label='Predicciones',color='blue')
plt.xlabel('fecha')
plt.ylabel('viajeros')
plt.title('MODELO ARIMA')
plt.legend()
plt.show()
## se ve que se ajusta muy bien pero para verlo mejor vamos a ahcer un grafico solo de la parte test:
intervalos_confianza = prediciones.conf_int() ### aqui obtenermos los intervalos de confianza son interesantes ya que nos dicen
#con un probabvilidad del 95% que los valores estan entre ellos

plt.figure(figsize=(12,8))
plt.plot(intervalos_confianza['lower R_España'],label='UCL',color ='gray')
plt.plot(intervalos_confianza['upper R_España'],label='UCL',color ='gray')
plt.plot(prediciones.predicted_mean, label='Predicciones',color='blue') #datos de prediccion
plt.plot(test,label='TEST', color= 'yellow') # datos reales
plt.xlabel('fecha')
plt.ylabel('viajeros')
plt.title('MODELO ARIMA')
plt.legend()
plt.show()


## TEMA 2 VIDEO 10: AUTOARIMA
# PODEMOS CREAR UN MODELO ARIMA AJUSTANDOLO DE FORMA AUTOMATICA CON UNA FUNCION DE LA LIBREIRA PMDARIMA
import pmdarima as pm


## PÒR ULTIMO EN EL ULTIMO VIDEO PARA VER TRANSFORMACIONES PARA ESTABILIZAR LA VARIANZA SE PUEDEN USAR LOS LOGARTIMOS:

log_serie = np.log(V_EXT.dropna()) # eliminamos los valores missiong para q no hyaa probslemas

# vemos subgraficos

fig3,(ax13,ax23) = plt.subplots(2,1,figsize=(12,8))
ax13.plot(V_EXT,color='blue')
ax13.set_title('original')
ax23.plot(log_serie,color='red')
ax23.set_title('log')
plt.tight_layout()
plt.show()

## apra ver si hay cambios es muy dificil, si fuese onstante la amplitud deberia ser mas o menos igual en lka amplitud en el eje y de la grafica
# en la zona de la rderecha hay menos cambio con lo q hay menos variabilidad y ahora toda la serie esta en un intervalo casi autentico

##IMPORTANTE: ESTO NO SE DEBE APLICAR A NO SER QUE SEA ESTRICATEMNTE NECESARIO CON LO Q SOLO SE DEBE APLICAR CUANDO NO CONSIGAMOS NINGUN MODELO ARIMA CON RESIDUALES INCORRELADOS

