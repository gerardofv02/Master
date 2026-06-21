

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pickle

from FuncionesMineria import *

data = pd.read_excel('../Data/VentaViviendas.xlsx')
# print(data)
# print(data.dtypes)

numericasAcategoricas  = ['Luxury', 'bathrooms','basement', 'floors','waterfront','view','year','month']

for variable in numericasAcategoricas:
    data[variable] = data[variable].astype(str)

# print(data.dtypes)

variables = list(data.columns)

# print(variables)

numericas = data.select_dtypes(include=['int','int16','int64','float','float16', 'float32', 'float64']).columns

categoricas = [variable for variable in variables if variable not in numericas]

## Analisis descripctivo

# print(numericas,'\n' ,categoricas)

# print(data.dtypes)

# print(analizar_variables_categoricas(data))
# print(data['yr_renovated'])

# print(cuentaDistintos(data))

descriptivos_num = data.describe().T
for num in numericas:
    descriptivos_num.loc[num, 'Asimetria'] = data[num].skew()
    descriptivos_num.loc[num, 'Kurtosis'] = data[num].kurtosis()
    descriptivos_num.loc[num, 'Rango'] = np.ptp(data[num].dropna().values)

# print(descriptivos_num)

#vemos valores perdidos
# print(data[variables].isna().sum()) ##NO HYA NINGUN SOLO VALOR FALTANTE EN ESTE DATASET solo los que tienen ? o -1

## Arreglamos los errores detectados
#al ser valores chicos de valores faltantes, no necesitamos recategorizar

data['condition'] = data['condition'].replace('?',np.nan)
data['waterfront'] = data['waterfront'].replace('-1',np.nan)

#Tenemos que camiar el yr_renovated para que tome valor 0 cuando la variableno haya sido renovada y 1 en otro caso.
data['yr_renovated'] = data['yr_renovated'].astype(str)
data['yr_renovated'] = ['1' if x!= '0' else '0' for x in data['yr_renovated']]
# print(numericas,'\n' ,categoricas)

# print(data.dtypes)

# print(analizar_variables_categoricas(data))
# print(data['yr_renovated'])

# print(cuentaDistintos(data))

#vamos a coger ahora las variables objetivo binaria y la continua que son importantes para poder seguir
#Price seria la variable continua mientras que luxury seria la binaria (lo pone el ejercicio)
varObtCont = data['price']
varObjBin = data['Luxury']
datos_input = data.drop(['price','Luxury'],axis=1)
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
# print(prop_missing)

## como se puede observar, tampoco hay tantos valores atipicos
#  el peor es el de sqft_lot, que tiene solo 0.04 (un 4%). Al ser todas muy bajas, realizamos imputaciones en todas (aletorias)

datos_input['prop_missings'] = datos_input.isna().mean(axis=1)
datos_input['prop_missings'] = datos_input['prop_missings'].astype(str)
variables_input.append('prop_missings')
categoricas_input.append('prop_missings')

for x in numericas_input:
    datos_input[x] = ImputacionCuant(var=datos_input[x],tipo='aleatorio')

for x in categoricas_input:
    datos_input[x] = ImputacionCuali(datos_input[x], 'aleatorio')

#una vez hehco esto, revisamos que no quedan ningun valor nan
print(datos_input.isna().sum())

datosVivienda = pd.concat([varObjBin, varObtCont, datos_input], axis =1)
with open('../Data/datosVivienda.pickle','wb') as archivo:
    pickle.dump(datosVivienda, archivo)  