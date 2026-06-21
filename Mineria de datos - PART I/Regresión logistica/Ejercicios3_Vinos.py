## Regresion lineal sirve para predecir variables continua
## Regresion logistica sirve para predecir variables categoricas

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pickle
from sklearn.model_selection import train_test_split

from FuncionesMineria import *

## abrimos el fichero previamnete creado en el apartado que tiene todo slos datos binarios
#incluyendo las trasnformaciones  de las variables numericas respecto a la binaria

with open('../Data/todo_bin.pickle', 'rb') as f:
    todo = pickle.load(f)
    
## identificamos la variable objetivo (viene en el enuncidado) y la eliminamos del conjunto de datos

varObjBin = todo['Compra']
todo = todo.drop('Compra', axis = 1)

# Veo el reparto original. Compruebo que la variable objetivo tome valor 1 para el evento y 0 para el no evento
# print(pd.DataFrame({
#     'n': varObjBin.value_counts()
#     , '%': varObjBin.value_counts(normalize = True)
# }))
## 78% de los datos corresponden al valor 1 y el restante al 0

## nos piden hacer un primer modelo entre datos entrenamiento y datos test, 
## entonces empezamos probando el modelo solo con las variables originales del conjunto de datos
eliminar = ['xAcidez', 'xAcidoCitrico', 'xAzucar', 'xCloruroSodico', 'xDensidad', 'xpH', 
            'xSulfatos', 'xAlcohol', 'xPrecioBotella']
todo = todo.drop(eliminar, axis = 1)

# Obtengo la particion
x_train, x_test, y_train, y_test = train_test_split(todo, varObjBin, test_size = 0.2, random_state = 1234567)
# dejamos el 20% para test y recordamos que random state es la seed o semilla que sirve para usar los mismos datos
# # (si la cambiamos se usn otros)
# Indico que la variable respuesta es numérica (hay que introducirla en el algoritmo de phython tal y como la va a tratar)
y_train, y_test = y_train.astype(int), y_test.astype(int)
##3 harpa creamos el modelo de regresion logistica segun nos dice el apartado dos, 
#es decir, creamos el modelo para predecir el valor de compra con los datos originales
#  para ello primero separamos las variables continuas y categoricas
var_cont1 = ['Acidez', 'AcidoCitrico', 'Azucar', 'CloruroSodico', 'Densidad', 'pH', 'Sulfatos', 
             'Alcohol', 'PrecioBotella']
var_categ1 = ['Etiqueta', 'CalifProductor', 'Clasificacion', 'Region', 'prop_missings']

# Creo el modelo inicial
modeloInicial = glm(y_train, x_train, var_cont1, var_categ1)
# Visualizamos los resultado del modelo
print(summary_glm(modeloInicial['Modelo'], y_train, modeloInicial['X']))
# En esta salida vemos los paretros asociados a cadauna de las variabales y su p valor.
# Con esto se puede ver con el p valor que el azucor y demas no son significativos (> 0.05) mientras q hay otros muchos q si lo son


# Calculamos la medida de ajuste R^2 para los datos de entrenamiento para ver si tiene una buena bondad de ajuste   
print(pseudoR2(modeloInicial['Modelo'], modeloInicial['X'], y_train))

# Preparamos los datos test para usar en el modelo
x_test_modeloInicial = crear_data_modelo(x_test, var_cont1, var_categ1)

# Calculamos la medida de ajuste R^2 para los datos test
print(pseudoR2(modeloInicial['Modelo'], x_test_modeloInicial, y_test))

## como podemos ver este modelo se puede estudiar ya que no tiene una gran diferencia entre r cuadrados 

# Calculamos el número de parámetros utilizados en el modelo.
len(modeloInicial['Modelo'].coef_[0])

## interpretacion a variable continua
# por ejemplo el acido que teine un valor estimado de -0,1 .
# como dijimos en la teoria se tiene que calcular la exponencial del valor del parametro
# este valor es 0,902
# hay q determinar si el valor de la exponencial del parametro es mayor o menor q 1, en este caso es menor q 1 por tanto para 
# realizar la interpretacion del parametro hay q calcular la inversa de este exponencial por lo tanto obtenemos un valor de 1,109

# Por tanto la interpretazicón sería: la ODD de que se haga pedido del vino sin añadir una unidad a la variable acided es 1,109 
# veces mayor que la odd de que se haga el pedido sin añadir esta unidad


#ahora interpretamos una variable categorica
# cpogemos valor M de la variable etiqueta. El aprametro estimado es de 0,9314. La exponencial de este parametro 2,538
# coMO Este valor es maytor q 1, tenemos q realizar la siguiente interpretacion
# la ODD de que se haga pedido del vino si la catergoría de la vraible etiqueta es M es 2,5358 veces mayor que la odd
# de que se haga el pedido del vino sin la categoría M
# Fijandome en la significacion de las variables, el modelo con las variables mas significativas queda

## Finjadonos en los valores que hemos obtenido antes, creamos un segundo modelo para que tenga mejor bondad con menos varibales

# apra ello escogemos las siguientes variables:

var_cont2 = ['Acidez', 'Sulfatos', 'pH']
var_categ2 = ['Etiqueta', 'CalifProductor', 'Clasificacion', 'prop_missings']


