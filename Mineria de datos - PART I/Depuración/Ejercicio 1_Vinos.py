## Apartado 1

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pickle
 
from FuncionesMineria import *

data = pd.read_csv('../Data/DatosVino.csv')

# print(data.dtypes)

numericasAcategoricas  = ['Compra', 'CalifProductor', 'Region']

for variable in numericasAcategoricas:
    data[variable] = data[variable].astype(str)

#print(data.dtypes)

variables = list(data.columns)

# print(variables)

numericas = data.select_dtypes(include=['int','int16','int64','float','float16', 'float32', 'float64']).columns

categoricas = [variable for variable in variables if variable not in numericas]

# print(numericas,'\n' ,categoricas)

# print(data.dtypes)

# print(analizar_variables_categoricas(data))

# print(cuentaDistintos(data))

descriptivos_num = data.describe().T
for num in numericas:
    descriptivos_num.loc[num, 'Asimetria'] = data[num].skew()
    descriptivos_num.loc[num, 'Kurtosis'] = data[num].kurtosis()
    descriptivos_num.loc[num, 'Rango'] = np.ptp(data[num].dropna().values)

# print(descriptivos_num)

#vemos valores perdidos
# print(data[variables].isna().sum())

## Arreglamos los errores detectados

data['Clasificacion'] = data['Clasificacion'].replace('?',np.nan)

data['Azucar'] = data['Azucar'].replace(99999,np.nan)

data['Alcohol'] = [x if 0<=x<=100 else np.nan for x in data['Alcohol']]

data['Etiqueta'] = data['Etiqueta'].replace({'b': 'B',
                                             'm':'M',
                                             'mb':'MB',
                                             'mm':'MM',
                                             'r': 'R'})

data['CalifProductor'] = data['CalifProductor'].replace({'0': '0-1', '1':'0-1',
                                                         '2': '2', 
                                                         '3':'3',
                                                         '4':'4',
                                                         '5':'5-12',
                                                         '6':'5-12',
                                                         '7':'5-12',
                                                         '8':'5-12',
                                                         '9':'5-12',
                                                         '10':'5-12',
                                                         '11':'5-12',
                                                         '12':'5-12',})

## falta corregir uno no?
print(data)
data = data.set_index(data['ID']).drop('ID', axis=1)
varObtCont = data['Beneficio']
varObjBin = data['Compra']
datos_input = data.drop(['Beneficio','Compra'],axis=1)
print(datos_input)

variables_input = list(datos_input.columns)

numericas_input = datos_input.select_dtypes(include=['int','int16','int64','float','float16', 'float32', 'float64']).columns

categoricas_input = [variable for variable in variables_input if variable not in numericas_input]

##ATIPICOS

resultados = {x:atipicosAmissing(datos_input[x])[1] / len(datos_input) for x in numericas_input}

# print(resultados)

for x in numericas_input:
    datos_input[x] = atipicosAmissing(datos_input[x])[0]

# patron_perdidos(datos_input)
# print(datos_input[variables_input].isna().sum())

prop_missing = datos_input.isna().sum()/len(datos_input)
print(prop_missing)

datos_input['prop_missings'] = datos_input.isna().mean(axis=1)
# print(datos_input)
# print(datos_input['prop_missings'].describe())
# print(len(datos_input['prop_missings'].unique()))

datos_input['prop_missings'] = datos_input['prop_missings'].astype(str)

##Eliminacion de variables con mas del 50% de varables perdias (no es este caso pero la añado comentada)
# eliminar = datos_input['prop_missings'] > 0.5
# datos_input = datos_input[~eliminar]
# varObjBin = varObjBin[~eliminar]
# varObtCont = varObtCont[~eliminar]

variables_input.append('prop_missings')
categoricas_input.append('prop_missings')

## añadimos mas opciones aunque no la tenemos que tener encuenta en este ejercicio ya que no se trata de este caso porq 
##no hya variables con mas de un 50% de variables perdidas

# eliminar = [prop_missing.index[x] for x in range(len(prop_missing)) if prop_missing[x] > 0.5]
# datos_input = datos_input.drop(eliminar, axis=1)

##RECATEGORIZACION (variables categóricas es mejor) la usamos para clasificacion porq tiene un 26% de valores perdidos

datos_input['Clasificacion'] = datos_input['Clasificacion'].fillna('Desconocido')
# print(datos_input['Clasificacion'].unique())
##imputacioness!!! tenemos opcion de rellenar estos datos, aleatorio, media y mediana
for x in numericas_input:
    datos_input[x] = ImputacionCuant(var=datos_input[x],tipo='aleatorio')

for x in categoricas_input:
    datos_input[x] = ImputacionCuali(datos_input[x], 'aleatorio')


#una vez hehco esto, revisamos que no quedan ningun valor nan
print(datos_input.isna().sum())

datosVinoDep = pd.concat([varObjBin, varObtCont, datos_input], axis =1)
with open('../Data/datosVinoDep.pickle','wb') as archivo:
    pickle.dump(datosVinoDep, archivo)  