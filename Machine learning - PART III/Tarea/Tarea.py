
####################################### IMPORTS ################################################################
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import make_scorer, mean_absolute_error, mean_squared_error, r2_score
###############################################################################################################3

#################################################################################################33
# Funcion obgeniada de mineria de datos para realiar imputacion de datos cuantitativos:
def ImputacionCuant(var, tipo):
    """
    Esta función realiza la imputación de valores faltantes en una variable cuantitativa.

    Datos de entrada:
    - var: Serie de datos cuantitativos con valores faltantes a imputar.
    - tipo: Tipo de imputación ('media', 'mediana' o 'aleatorio').

    Datos de salida:
    - Una nueva serie con valores faltantes imputados.
    """

    # Realiza una copia de la variable para evitar modificar la original
    vv = var.copy()

    if tipo == 'media':
        # Imputa los valores faltantes con la media de la variable
        vv[np.isnan(vv)] = round(np.nanmean(vv), 4)
    elif tipo == 'mediana':
        # Imputa los valores faltantes con la mediana de la variable
        vv[np.isnan(vv)] = round(np.nanmedian(vv), 4)
    elif tipo == 'aleatorio':
        # Imputa los valores faltantes de manera aleatoria basada en la distribución de valores existentes
        x = vv[~np.isnan(vv)]
        frec = x.value_counts(normalize=True).reset_index()
        frec.columns = ['Valor', 'Frec']
        frec = frec.sort_values(by='Valor')
        frec['FrecAcum'] = frec['Frec'].cumsum()
        random_values = np.random.uniform(min(frec['FrecAcum']), 1, np.sum(np.isnan(vv)))
        imputed_values = list(map(lambda x: list(frec['Valor'][frec['FrecAcum'] <= x])[-1], random_values))
        vv[np.isnan(vv)] = [round(x, 4) for x in imputed_values]

    return vv
3#######################################################################################################

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

# vemos que como el telefono del cliente parece ser un id unico, vamos a estudiarlo mejor:
telefonos_repetidos = (
    df['tel_clie']
    .value_counts()
    .loc[lambda x: x > 1]
)

print(telefonos_repetidos)

# vemos que puede ser una variable que no es unica, pero raro me parece pero estan anonimizados los datos, por ahora la dejamos


## 1. ahora vamos a ver los valores missing:
print(df.isna().sum())



# como tenemos pocas variables missing, vamos a agregarlas con la imputacion de la mediana.

columns_missing = ['cod_area_tel','coste_tot_diurnas', 'mins_tot_noc', 'count_noc','coste_tot_inter']

for x in columns_missing:
    df[x] = ImputacionCuant(var=df[x],tipo='mediana')

# comprobamos que ya no hay datos faltantes
print(df.isna().sum()) # ya no hya

## 2. estandarizar los datos
# buscamos solo las numericas continuas para estandarizarlas (las binarias o las que son mas cualitativas aunque sean numeros vamos a dejarlas como estan)

numericas_continuas = ['duracion_cuen','count_buzon','mins_tot_diurnas','count_diurnas','coste_tot_diurnas', 'mins_tot_vespertinas', 'count_vespertinas', 'coste_tot_vespertinas','mins_tot_noc','count_noc', 'coste_tot_noc', 'mins_tot_inter', 'count_inter','coste_tot_inter', 'count_svc']

scaler = StandardScaler()

for x in numericas_continuas:
    df[x] = scaler.fit_transform(df[[x]])

print(df.head()) # datos ya estandarizados

# 3. cpomnvertir las categoricas a numericas -> como no tenemos categoricas, se deja asi


## pasamos a construir el arbol de decision (en este caso de clasficiacion)
# 1. separamos la variable objetivo de las variables input
x = df.drop(['Y'],axis=1)
y = df['Y']

# 2. divirmos los datos en train y test
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42) # dejamos un 20% para el conjunto test

# 3. creamos el arbol de clasficiacion (usamos gini por ejemplo como criteria)
arbol = DecisionTreeClassifier(min_samples_split=30, criterion='gini')

# 4. Entrenamos el modelo
arbol.fit(X_train,y_train)

# 5. Vemos el resutlado de como quedaría el modelo usando las metricas

## para esto primero empezamos viendo por ejemplo la importancia de las variables input
df_importancia = pd.DataFrame({'Variable': arbol.feature_names_in_, 'Importancia': arbol.feature_importances_}).sort_values(by='Importancia', ascending=False)

# Crear un gráfico de barras
plt.bar(df_importancia['Variable'], df_importancia['Importancia'], color='skyblue')
plt.xlabel('Variable')
plt.ylabel('Importancia')
plt.title('Importancia de las características')
plt.xticks(rotation=45, ha='right')  # Rotar los nombres en el eje x para mayor legibilidad
plt.tight_layout()
plt.show()


# Predicciones en conjunto de entrenamiento y prueba
y_train_pred = arbol.predict(X_train)
y_test_pred = arbol.predict(X_test)

# Medidas de bondad de ajuste en train
y_pred_train = arbol.predict(X_train)

# Calcular diferentes medidas de bondad de ajuste
mae = mean_absolute_error(y_train, y_pred_train)
mse = mean_squared_error(y_train, y_pred_train)
rmse = np.sqrt(mse)
r2 = r2_score(y_train, y_pred_train)

# Imprimir las métricas
print(f'MAE (Error Absoluto Medio): {mae:.2f}')
print(f'MSE (Error Cuadrático Medio): {mse:.2f}')
print(f'RMSE (Raíz del Error Cuadrático Medio): {rmse:.2f}')
print(f'R²: {r2:.2f}')



########################################################################################################33

