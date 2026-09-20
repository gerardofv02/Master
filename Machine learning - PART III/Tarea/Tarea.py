
####################################### IMPORTS ################################################################
import os
import pandas as pd
###############################################################################################################3

######################################### DATOS ##########################################################
os.chdir('/home/jerry/Documents/master/Master/Machine learning - PART III/Tarea/Data')
file = 'BBDD_ML_TAREA.csv'
df = pd.read_csv(file)
print(df.head())
print(f'\nLa frecuencia de cada clase es: \n{df.Y.value_counts(normalize=True)}')

## procximos pasos: estudiar bien los datos leer que es cada columna y realizar un estudio de datos missing, categoricos,...
########################################################################################################33

