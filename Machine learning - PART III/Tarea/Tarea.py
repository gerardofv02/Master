
####################################### IMPORTS ################################################################
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
###############################################################################################################3

######################################### DATOS ##########################################################
os.chdir('/home/jerry/Documents/master/Master/Machine learning - PART III/Tarea/Data')
file = 'BBDD_ML_TAREA.csv'
df = pd.read_csv(file)
print(df.head())
print(f'\nLa frecuencia de cada clase de la variable objetivo es: \n{df.Y.value_counts(normalize=True)}')

## procximos pasos: estudiar bien los datos leer que es cada columna y realizar un estudio de datos missing, categoricos,...
# vamos a renombrar las variables para que tengan mas sentido en lugar de un id
nuevos_nombres = ['estado_clie','duracion_cuen','cod_area_tel','tel_clie','plan_inter','plan_buzon','count_buzon','mins_tot_diurnas','count_diurnas','coste_tot_diurnas','mins_tot_vespertinas','count_vespertinas','coste_tot_vespertinas','mins_tot_noc','count_noc','coste_tot_noc','mins_tot_inter','count_inter','coste_tot_inter', 'count_svc','Y']
df.columns = nuevos_nombres
print("\nDataFrame con columnas renombradas:")
print(df)

## vamos ahora a hacer analitica de la base de datos

#vamos a seguir analizando las distintas variables
# vemoas ahora la cantidad de registros que tenemos
print(f"Filas: {df.shape[0]}")

# vemos ahora un poco de informacion general
print(f"Tipos: {df.dtypes}")

# vemos tmb estadisticos descriptivos
print(f"EStadisticos: {df.describe().T}")

## vamos a ver ahora datos unicos por varibales para ver cuales serian binarias
print(df.nunique().sort_values())
## aqui vemos una cosa rara y es que vemos 9200 registros mientras que solo estamos viendo 3536 telefonos cde clientes distintos (no sabemos si debria ser unico o no)
## segun se ve las binarias serian los distintos planes y la variable a predecir mientra que tmb hay optra variable con muy pocas clases distintas y esta es el codigo de area telefonica

# vemos campos que pueden llegar a ser binarios que son: plan_inter y plan_buzon:
# vemos las frecuencias:
print(f'\nLa frecuencia de cada clase del plan internacional es: \n{df.plan_inter.value_counts(normalize=True)}')
print(f'\nLa frecuencia de cada clase del plan buzon es: \n{df.plan_buzon.value_counts(normalize=True)}')
# vemos que para el plan internacional no lo tiene un 82% de la gente mientras que para el plan de buzon no lo tienen un 78% de la gente. con lo que poca gente tiene estos planes.

## ahora vamos a ver los valores missing:
print(df.isna().sum())

# vemos que como el telefono del cliente parece ser un id unico, vamos a estudiarlo mejor ya que pueden ser datos faltantes:
telefonos_repetidos = (
    df['tel_clie']
    .value_counts()
    .loc[lambda x: x > 1]
)

print(telefonos_repetidos)
########################################################################################################33

