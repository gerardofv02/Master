import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pickle
from sklearn.model_selection import train_test_split

from FuncionesMineria import *

with open('datosEspana.pickle','rb') as f:
    datos = pickle.load(f)

varObjCont = datos['Dcha_Pct']
varObjBin = datos['Derecha']
datos_input = datos.drop(['Derecha', 'Dcha_Pct'], axis =1)
variables = list(datos_input)

# graficoVcramer(datos_input,varObjBin)
# graficoVcramer(datos_input,varObjCont)

VCramer = pd.DataFrame(columns=['Variable', 'Objetivo', 'Vcramer'])

for variable in variables:
    v_cramer = Vcramer(datos_input[variable], varObjCont)
    VCramer = VCramer.append({'Variable': variable, 'Objetivo': varObjCont.name, 'Vcramer': v_cramer},
                             ignore_index=True)
    
for variable in variables:
    v_cramer = Vcramer(datos_input[variable], varObjBin)
    VCramer = VCramer.append({'Variable': variable, 'Objetivo': varObjBin.name, 'Vcramer': v_cramer},
                             ignore_index=True)
    
# mosaico_targetbinaria(datos_input['Densidad'], varObjBin, 'Densidad')  

#vemos graficamente el efecto de dos variables cuantitativas sobre la binaria
# boxplot_targetbinaria(datos_input['Age_under19_Ptge'], varObjBin,nombre_ejeX='target', nombre_ejeY='Age_under19_Ptge') #como no hya mucha diferencias entre las distribuiciones, no tiene mucha influencia sobre la variable respuesta
# boxplot_targetbinaria(datos_input['Age_19_65_pct'], varObjBin,nombre_ejeX='target', nombre_ejeY='Age_19_65_pct') #igual que el anterior

numericas = datos_input.select_dtypes(include=['int','float']).columns

matriz_corr = pd.concat([varObjCont,datos_input[numericas]], axis=1).corr(method = 'pearson')

mask = np.triu(np.ones_like(matriz_corr,dtype=bool))

# plt.figure(figsize=(8,6))

# sns.heatmap(matriz_corr, annot=True,cmap='coolwarm',fmt='.2f',cbar=True, mask=mask)
# plt.title('Matriz de correlacion')

# plt.show()

input_cont = pd.concat([datos_input, Transf_Auto(datos_input[numericas], varObjCont)], axis = 1)
input_bin = pd.concat([datos_input, Transf_Auto(datos_input[numericas], varObjBin)], axis = 1)

todo_cont = pd.concat([input_cont, varObjCont], axis=1)
todo_bin = pd.concat([input_bin, varObjBin], axis=1)
with open('todo_bin.pickle', 'wb') as archivo:
    pickle.dump(todo_bin,archivo)

with open('todo_cont.pickle', 'wb') as archivo:
    pickle.dump(todo_cont, archivo)

x_train, x_test, y_train, y_test = train_test_split(datos_input, np.ravel(varObjCont), test_size = 0.2, random_state = 123456)


var_cont1 = ['Population', 'TotalCensus', 'Age_0-4_Ptge', 'Age_under19_Ptge', 'Age_19_65_pct', 'Age_over65_pct', 'WomanPopulationPtge', 
             'ForeignersPtge', 'SameComAutonPtge', 'SameComAutonDiffProvPtge','DifComAutonPtge','UnemployLess25_Ptge','Unemploy25_40_Ptge','UnemployMore40_Ptge','AgricultureUnemploymentPtge','IndustryUnemploymentPtge','ConstructionUnemploymentPtge','ServicesUnemploymentPtge','totalEmpresas','Industria','Construccion','ComercTTEHosteleria','Servicios','inmuebles','Pob2010','SUPERFICIE','PobChange_pct','PersonasInmueble','Explotaciones']
var_categ1 = ['Name', 'CCAA', 'CodigoProvincia', 'ActividadPpal', 'Densidad']

## Creamos el modelo
modelo1 = lm(y_train, x_train, var_cont1, var_categ1)
print(modelo1['Modelo'].summary())