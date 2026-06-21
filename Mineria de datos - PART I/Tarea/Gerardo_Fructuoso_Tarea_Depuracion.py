# Importamos librerias 

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pickle
from sklearn.model_selection import train_test_split

from FuncionesMineria import *

data = pd.read_excel('DatosEleccionesEspaña.xlsx')

# print("Cantidad columnas antes:" ,len(data.columns))
data = data.drop(['Izda_Pct','Otros_Pct', 'AbstencionAlta','AbstentionPtge', 'Izquierda', 'Unnamed: 41'],axis=1)

# print('Cantidad columnas despues:' ,len(data.columns))
# print(data.dtypes)
numericasAcategoricas  = ['CodigoProvincia', 'Derecha']

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

# print(data[variables].isna().sum())
data['Densidad'] = data['Densidad'].replace('?',np.nan)
varObtCont = data['Derecha']
varObjBin = data['Dcha_Pct']
datos_input = data.drop(['Derecha','Dcha_Pct'],axis=1)

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
datos_input['prop_missings'] = datos_input['prop_missings'].astype(str)

variables_input.append('prop_missings')
categoricas_input.append('prop_missings')

for x in numericas_input:
    datos_input[x] = ImputacionCuant(var=datos_input[x],tipo='aleatorio')

for x in categoricas_input:
    datos_input[x] = ImputacionCuali(datos_input[x], 'aleatorio')

print(datos_input.isna().sum())

datosEspana = pd.concat([varObjBin, varObtCont, datos_input], axis =1)
with open('datosEspana.pickle','wb') as archivo:
    pickle.dump(datosEspana, archivo)  