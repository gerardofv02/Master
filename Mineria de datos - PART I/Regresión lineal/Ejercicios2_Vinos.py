## Regresion lineal sirve para predecir variables continua
## Regresion logistica sirve para predecir variables categoricas

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pickle
from sklearn.model_selection import train_test_split

from FuncionesMineria import *
 
#abriimos fichero depurado previamente

with open('../Data/datosVinoDep.pickle','rb') as f:
    datos = pickle.load(f)

varObjCont = datos['Beneficio']
varObjBin = datos['Compra']
datos_input = datos.drop(['Beneficio', 'Compra'], axis =1)

variables = list(datos_input)

graficoVcramer(datos_input,varObjBin)
graficoVcramer(datos_input,varObjCont)

VCramer = pd.DataFrame(columns=['Variable', 'Objetivo', 'Vcramer'])

for variable in variables:
    v_cramer = Vcramer(datos_input[variable], varObjCont)
    VCramer = VCramer.append({'Variable': variable, 'Objetivo': varObjCont.name, 'Vcramer': v_cramer},
                             ignore_index=True)
    
for variable in variables:
    v_cramer = Vcramer(datos_input[variable], varObjBin)
    VCramer = VCramer.append({'Variable': variable, 'Objetivo': varObjBin.name, 'Vcramer': v_cramer},
                             ignore_index=True)

#graficamente el efecto de dos variables cualitativas sobre la binaria
#tomo las variavbles con mas y menos relacion con la variable objetivo binaria
# mosaico_targetbinaria(datos_input['Region'], varObjBin, 'Region') #podemos decir que no tiene relacion ya que no aporta inofrmacion porque todas se ven iguales
# mosaico_targetbinaria(datos_input['Clasificacion'], varObjBin, 'Clasificacion') #Podemos decir que si que influye ya que son distintas por cada una de las variables posibles

#vemos graficamente el efecto de dos variables cuantitativas sobre la binaria
# boxplot_targetbinaria(datos_input['Alcohol'], varObjBin,nombre_ejeX='target', nombre_ejeY='Alcohol') #como no hya mucha diferencias entre las distribuiciones, no tiene mucha influencia sobre la variable respuesta
# boxplot_targetbinaria(datos_input['CloruroSodico'], varObjBin,nombre_ejeX='target', nombre_ejeY='CloruroSodico') #igual que el anterior

#ahora pogrbamos con el histograma
# hist_targetbinaria(datos_input['Alcohol'], varObjBin,'Alcohol') #vemos que tampovo hay mucha diferencia, con lo que igual que antes
# hist_targetbinaria(datos_input['CloruroSodico'], varObjBin,'CloruroSodico') #Como podemos ver que para el cloruro sodico, la 1 tiene un poco mas que la del 0 con lo que podemos decir que si tiene algo de relacion

#Ahora tenemos que calcularlo con las variables continuas para ello:
#Correlacion entre todas las variables numericas dos a dos con las variables objetivo
#obtenemos columnas
numericas = datos_input.select_dtypes(include=['int','float']).columns
# print(numericas)

# calculamos la matriz de correlacion de pearson entre variable objetivo y el resto de variables
matriz_corr = pd.concat([varObjCont,datos_input[numericas]], axis=1).corr(method = 'pearson')
#creamos mascara para ocultar mitrad superior de la matriz
mask = np.triu(np.ones_like(matriz_corr,dtype=bool))
#creamos una figura con el grafico como mapa de calor con la matriz de correlacion
# plt.figure(figsize=(8,6))

# sns.heatmap(matriz_corr, annot=True,cmap='coolwarm',fmt='.2f',cbar=True, mask=mask)
# plt.title('Matriz de correlacion')

# plt.show()
##Esto nos da el coficiente de correlacion entre las variables explicativas 2 a 2  tenierndo en cuenta la correlacion de la variable objetivo
#pero son muy chicas, la que mas tenemos es la del alcohol con el beneficio que tiene relacion con la variable objetivo

#apartado 2 del objetivo
#transformamos las variables numericas con respesto a los dos tipos de variables
input_cont = pd.concat([datos_input, Transf_Auto(datos_input[numericas], varObjCont)], axis = 1)
input_bin = pd.concat([datos_input, Transf_Auto(datos_input[numericas], varObjBin)], axis = 1)

todo_cont = pd.concat([input_cont, varObjCont], axis=1)
todo_bin = pd.concat([input_bin, varObjBin], axis=1)
with open('../Data/todo_bin.pickle', 'wb') as archivo:
    pickle.dump(todo_bin,archivo)

with open('../Data/todo_cont.pickle', 'wb') as archivo:
    pickle.dump(todo_cont, archivo)

##Comenzamos regresion lineal
#obtenemos la particion spliteada/ test_size la cantidad de datos para el test y luego el random_state para que tenga siempre los mismos (si cambia es disinto)
x_train, x_test, y_train, y_test = train_test_split(datos_input, np.ravel(varObjCont), test_size = 0.2, random_state = 123456)
# print(x_train, x_test, y_train, y_test)

# Construyo un modelo preliminar con todas las variables (originales)
# Indico la tipología de las variables (numéricas o categóricas)
var_cont1 = ['Acidez', 'AcidoCitrico', 'Azucar', 'CloruroSodico', 'Densidad', 'pH', 'Sulfatos', 
             'Alcohol', 'PrecioBotella']
var_categ1 = ['Etiqueta', 'CalifProductor', 'Clasificacion', 'Region', 'prop_missings']

## Creamos el modelo
modelo1 = lm(y_train, x_train, var_cont1, var_categ1)

#visualizamos los resultados
# print(modelo1['Modelo'].summary())

##Aqui nos imprime una gran tabla donde viene informacion imporatene:
# tenemos aqui las medidas de ajust que son: r-cuadrado y r-cuadrado ajustado
#tmb tenemos los valores de AIC y BIC ue no estan acotados y nos sirven para comparar modelos 
# tenemos la probabilidad asociada al estadistico F que es el que media el contraste global de la regresion
# hipotesis nula: todos los parametros del modelo serian 0, como pvalor es menor que 0.05, no podemos rechazar hipotesis nula con lo
# almentos una de las variables en el modelo, ayuda a explicar la varaible respuesta
# debajo tenemos el coeficiente estimados para cada una de las variables de los datos y el p valor asociado.
# hay que ver la significacion de los parmatros de acuerdo al p valor. la hipotesis nula es cuando el parametro es = 0, si es menor de 0.05, 
# se puede rechazar la hipotesis nula al 95% de prob, lo q puede decir, q el parametro si es significativos
# Aqui vienen tmb las categoricas, pero hay una categoria menos ya que una la tomamos como referencia pero podemos saber cual es 
# su valor, con el valor del restoS
## para interpretar las variable continuas:
# por ejemplo, el clorurosodico tiene -18 de coef, con lo que nos quiere decir que por cada incremento unitario de esta variable
# el beneficio del vino disminuye 18 unidades.
## interpretar las variables categoricas:
# etiqueta MB, como el coef es 78 entonces el beneficio es 78 veces mayor que si fuese otra cateogria (q tiene negativo porejemplo)

# para medir calidad del modelo construido tenemos que observar que el constraste de significacion global de regresion,
# me indique que es mejor este modelo que el no modelo lo cual indica que al menos una de las variables en el modelo, tiene
# influencia sobre la variable respuesta
# tambien tenemos que ver la significacion de los parametros con lo que se tiene que ver el contraste individaual de los paramtros asociados a cada una de las variables explicativas
#debemos observar los valores de rcuadrad y adj r cuadrado, que lo que queremos es que sea similar a la variable de rcuadrado test
# esto indicara que cuando se hagan con otros datos distintos a los estiamdos, no s ehayan perdido nada en la bondad de ajuste
# mediante otros test, tambien podemos observar como se comparten los residios y como se distribuyen (durbin watson, jarque-bera)

# en este caso el test de JB, con el p-valor asociado que nos dice que toma un valor muymuy pequeño,
# con lo q rechazamos la hipotesis nula con lo q nos dice que los residios no se distribuyen noramlemnete

#calculamos la medida de ajuste r cuadrado
print(Rsq(modelo1['Modelo'], y_train, modelo1['X']))

# Preparamos los datos test para usar en el modelo para verificar el correcto modelo
x_test_modelo1 = crear_data_modelo(x_test, var_cont1, var_categ1) # para convertir en variables dummy
#tenemosque trabajar con las variables dummy para asegurarmnos de la correcta implementacion del modelo
# Calculamos la medida de ajuste R^2 para los datos test
print(Rsq(modelo1['Modelo'], y_test, x_test_modelo1))
# nos fijamos en la importancia de las variables

print(modelEffectSizes(modelo1, y_train, x_train, var_cont1, var_categ1))
# aui podemos observar que si eliminamos la variable (densidad por ejemplo) vemos que bajaria en el modelo el valor del r cuadrado un
#          Densidad  0.000018 con lo que no se modificaria practicamente este valor por lo tanto esta variable no tiene influencia
## sin embargo, clasificacion si q influeria mucho y endria influiencia sobre vairble respuesta u objetivo Clasificacion  0.212332

##Como se nos pide en un apartado  uscar el modelo que mejor rrespuesta tenga, tenemos q reduciar las variables introducidas en 
#el modelo, con lo que volviendo a ver el grafico de cramer, podremos observar 

# #para ello pillamos las variables q tengan mas de 0,1 de cramer:
# graficoVcramer(datos_input, varObjCont) # Pruebo con las mas importantes

#Construimos el segundo modelo
var_cont2 = []
var_categ2 = ['Etiqueta', 'CalifProductor', 'Clasificacion','prop_missings']
modelo2 = lm(y_train, x_train, var_cont2, var_categ2)
modelEffectSizes(modelo2, y_train, x_train, var_cont2, var_categ2)
modelo2['Modelo'].summary()
print(Rsq(modelo2['Modelo'], y_train, modelo2['X']))
x_test_modelo2 = crear_data_modelo(x_test, var_cont2, var_categ2)
print(Rsq(modelo2['Modelo'], y_test, x_test_modelo2))
# segun vemos en este modelo, los r2 del train y del test se asemejan mucho como en el modelo 1 pero como tiene muchas menos variables
#por el principio de parsimonia, es mejor el modelo 2
# Como el p valor de las categorias de prop_missings es muy alto (> 0.05), quitamos esta variable se podria descartar

#para el siguiente modelo, pide en el enunciado usar las que tengan un R cuadrado con los valores mas altos, y eso son clasificacion, etiqueta y califprodructo:

var_cont3 = []
var_categ3 = ['Etiqueta', 'CalifProductor', 'Clasificacion']
modelo3 = lm(y_train, x_train, var_cont3, var_categ3)
modelo3['Modelo'].summary()
print(Rsq(modelo3['Modelo'], y_train, modelo3['X']))
x_test_modelo3 = crear_data_modelo(x_test, var_cont3, var_categ3)
print(Rsq(modelo3['Modelo'], y_test, x_test_modelo3))
# se peude observar que no hay mucha diferencia en el modelo de r cuadrado ni con los modelos anteriores
# este modelo tiene menos parametros y sus parametros son mas significativos, con lo que por ahora es el mejor modelo

# para el siguiente apartado se nos pide que para el mejor modelo construido, introducir interaciones
# en las variables que pueden tener mas influencia en la variable opbjetivo. Aqui podemos irla probando dos a dos

var_cont4 = []
var_categ4 = ['Etiqueta', 'CalifProductor', 'Clasificacion']
var_interac4 = [('Clasificacion', 'Etiqueta')]
modelo4 = lm(y_train, x_train, var_cont4, var_categ4, var_interac4)
modelo4['Modelo'].summary()
print('Modelo con interaciones entrenamiento: ' ,Rsq(modelo4['Modelo'], y_train, modelo4['X']))
x_test_modelo4 = crear_data_modelo(x_test, var_cont4, var_categ4, var_interac4)
print('Modelo con interaciones test: ' ,Rsq(modelo4['Modelo'], y_test, x_test_modelo4))
#vemos que han aumentado mucho el valor de R cuadrado (no tanto pero bastante) y ademas son muy similares, pero tmb al añadir iteraciones
# hemos aumentado mucho la cantidad de variables que le metemos al modelo. Hemos aumentado 16 variables (al ser categoricas,
#se añaden la cantidad de distintas categorias por variable que hay)

## ahora tenemos que realizar validacion cruzada para ver cual es el mejro modelo

# Crea un DataFrame vacío para almacenar resultados
results = pd.DataFrame({
    'Rsquared': [],
    'Resample': [],
    'Modelo': []
})

# Realiza el siguiente proceso 20 veces (representado por el bucle `for rep in range(20)`) (es lo q se pide en el eneunciado 
# #la cantidad de veces) por lo que vamos a tener para cada uno de los modelos, 100 valores de r cuadrado (5 *20 = 100)
# esto se debe a que nos piden dividir el subconjunto de datos en 5 muestras
# esto sirve para detectar el modelo que menor R cuadrado tenga de media para cada una de las 100 repeticiones que se ahan realizado
# el modelo que menos variabilidad tenga en el r2, es el que se considerará mas robusto
for rep in range(20):
    # Realiza validación cruzada en cuatro modelos diferentes y almacena sus R-squared en listas separadas
    modelo1VC = validacion_cruzada_lm(5, x_train, y_train, var_cont1, var_categ1)
    modelo2VC = validacion_cruzada_lm(5, x_train, y_train, var_cont2, var_categ2)
    modelo3VC = validacion_cruzada_lm(5, x_train, y_train, var_cont3, var_categ3)
    modelo4VC = validacion_cruzada_lm(5, x_train, y_train, var_cont4, var_categ4, var_interac4)
    
    # Crea un DataFrame con los resultados de validación cruzada para esta repetición
    results_rep = pd.DataFrame({
        'Rsquared': modelo1VC + modelo2VC + modelo3VC + modelo4VC,
        'Resample': ['Rep' + str((rep + 1))] * 5 * 4,  # Etiqueta de repetición
        'Modelo': [1] * 5 + [2] * 5 + [3] * 5 + [4] * 5  # Etiqueta de modelo (1, 2, 3 o 4)
    })
    
    # Concatena los resultados de esta repetición al DataFrame principal 'results'
    results = pd.concat([results, results_rep], axis=0)

# print(results)

# en resutlados hemos guardado los valores de cada una de las submuestras que se han lanzado

#ahora representamos graficamente el vlaor de r cuadrado para cada uno de los modelos.
# Boxplot de la validación cruzada
plt.figure(figsize=(10, 6))  # Crea una figura de tamaño 10x6
plt.grid(True)  # Activa la cuadrícula en el gráfico
# Agrupa los valores de R-squared por modelo
grupo_metrica = results.groupby('Modelo')['Rsquared']
# Organiza los valores de R-squared por grupo en una lista
boxplot_data = [grupo_metrica.get_group(grupo).tolist() for grupo in grupo_metrica.groups]
# Crea un boxplot con los datos organizados
plt.boxplot(boxplot_data, labels=grupo_metrica.groups.keys())  # Etiqueta los grupos en el boxplot
# Etiqueta los ejes del gráfico
plt.xlabel('Modelo')  # Etiqueta del eje x
plt.ylabel('Rsquared')  # Etiqueta del eje y
plt.show()  # Muestra el gráfico 

# como vemos el modelo 4 es el quemayor valor de r cuadrado tiene por lo tanto mayor bondad de ajuste
# y la variabilidad mas pequeña (caja mas chica)
# los otros 3 son mas o menos similares

# visto esto se podria decir que el modelo 4 es el mejor, pero vamos a calcularlo de forma nukerica y verlo mas claro

# Calcular la media de las métricas R-squared por modelo
media_r2 = results.groupby('Modelo')['Rsquared'].mean()
print('meida r cuadrado',media_r2)
# Calcular la desviación estándar de las métricas R-squared por modelo
std_r2 = results.groupby('Modelo')['Rsquared'].std()
print('desviacion tipica',std_r2)
# Contar el número de parámetros en cada modelo yua que es un factor importante
num_params = [len(modelo1['Modelo'].params), len(modelo2['Modelo'].params), 
             len(modelo3['Modelo'].params), len(modelo4['Modelo'].params)]

# Teniendo en cuenta el R2, la estabilidad y el numero de parametros, nos quedamos con el modelo3 ya que la diferencia de r cuadrado
# no es tan grande, pero sin embargo es muy grande la diferencia de parametros (el 4 tiene 29 mienstras que el 3 tiene 13)
# Vemos los coeficientes del modelo ganador
modelo3['Modelo'].summary()

# Evaluamos la estabilidad del modelo a partir de las diferencias en train y test:
print('Entrenamiento modelo 3', Rsq(modelo3['Modelo'], y_train, modelo3['X']))
print('Modelo 3 testeo',Rsq(modelo3['Modelo'], y_test, x_test_modelo3))

# Vemos las variables mas importantes del modelo ganador

modelEffectSizes(modelo3, y_train, x_train, var_cont3, var_categ3)
