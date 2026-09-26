
####################################### IMPORTS ################################################################
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import make_scorer, mean_absolute_error, mean_squared_error, r2_score,f1_score, recall_score, precision_score, accuracy_score, confusion_matrix, roc_curve, auc
from sklearn.tree import plot_tree
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from xgboost import XGBClassifier, XGBRegressor
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
seed =123
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
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=seed) # dejamos un 20% para el conjunto test

#####################################################################################################################33
















###################################### arbol de decision #############################################################3

# 3. creamos el arbol de clasficiacion (usamos gini por ejemplo como criteria)
arbol = DecisionTreeClassifier(min_samples_split=30, criterion='gini',random_state=seed)

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
y_train_pred = arbol.predict_proba(X_train)[:,1]
y_train_pred_2 = arbol.predict(X_train)
y_test_pred = arbol.predict_proba(X_test)[:,1]
y_test_pred_2 = arbol.predict(X_test)



########## vamos con el accuracy score#
accuracy = accuracy_score(y_train, y_train_pred_2)
accuracy_test = accuracy_score(y_test, y_test_pred_2)
print(f"Accuracy train: {accuracy}")
print(f"Accuracy test: {accuracy_test}")

##############3 vamos con la precicsion socre
precision=precision_score(y_train, y_train_pred_2)
precision_test=precision_score(y_test,y_test_pred_2)
print(f"Precisión train: {precision}")
print(f"Precisión test: {precision_test}")

################ vamos con la recall score

## aqui hablamos de la sensibilidad
recall = recall_score(y_train, y_train_pred_2)
recall_test = recall_score(y_test,y_test_pred_2)
print(f"Recall/sensibilidad train: {recall}")
print(f"Recall/sensibilidad test: {recall_test}")
###3 vamos con el f1 score
f1=f1_score(y_train, y_train_pred_2)
f1_test=f1_score(y_test, y_test_pred_2)
print(f"F1_score train: {f1}")
print(f"F1_score test: {f1_test}")

## ahora vamos a ver gráficamente algunas de estas métricas
## matriz de confusion
cm = confusion_matrix(y_train, y_train_pred_2)
clases = ['Cliente no deja (0)', 'Cliente deja (1)']
# Crear un mapa de calor para mejorar la visualización
plt.figure(figsize=(2, 2))
sns.heatmap(cm, annot=True, cmap='Greens', fmt='g', xticklabels=clases, yticklabels=clases)
plt.xlabel('Valores predichos')
plt.ylabel('Valores reales')
plt.title('Matriz de confusión')
plt.show()
plt.close()



# vamos a ver ahora graficamente la curva roc
fpr, tpr, thresholds = roc_curve(y_train, y_train_pred)
print(f"Tasa de falsos positivos: {fpr}")
print(f"Tasa de verdaderos positivos: {tpr}")
print(f"Puntos de corte (thresholds): {thresholds}")
roc_auc = auc(fpr, tpr)
print(f"AUC: {roc_auc}")
print('El valor del AUC nos dice que el modelo ha hecho una clasificación aleatoria')

plt.figure()
plt.plot(fpr, tpr, color='darkorange',
         label='ROC curve')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--') 
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('FPR=1-especifidad')
plt.ylabel('TPR=recall')
plt.title('Curva ROC')
plt.legend(loc="lower right")
plt.show()

## SEgun vemos en las metricas esta muy bien, pero no podemos asegurar que sea el mejor modelo, por ello vamos a ahcer uso del gridsearch para ver cual es el mejor (al ser un conjunto de datos muy chico, vamos a poner como max_depth siempre 5):

params = {
    'max_depth': [2, 3, 5, 10, 20],
    'min_samples_split': [5, 10, 20, 50, 100],
    'criterion': ["gini", "entropy"]
}
params2 = {
    'max_depth': [2, 3],
    'min_samples_split': [3,4,5,6,7,10, 20],
    'criterion': ["gini", "entropy"]
}
scoring_metrics = ['accuracy', 'precision_macro', 'recall_macro', 'f1_macro']
#recordar que arbol2 es el árbol cuyas VI son todas las variables.
# cv = crossvalidation
grid_search = GridSearchCV(estimator=arbol, 
                           param_grid=params2, 
                           cv=4, scoring = scoring_metrics, refit='accuracy')
grid_search.fit(X_train, y_train)
# Obtener resultados del grid search
results = pd.DataFrame(grid_search.cv_results_)
sorted_results = results.sort_values(by='mean_test_accuracy', ascending=False)
pd.set_option('display.max_colwidth', None)
# Mostrar resultados
print("Resultados de Grid Search:")
print(sorted_results[['params', 'mean_test_accuracy', 'mean_test_precision_macro', 'mean_test_recall_macro', 'mean_test_f1_macro']])
# print(results[['params']])

## segun vemos estos resultados el mejor criteria es gini pero entropy no se queda corto, el mejor max_depth es 20 , parece tmb que cuanto menos min_sample_split mejor, entonces voy a porar a reducir estos parametros para volver a lanzarlo y probar de neuvo con nuevos aprametros eso si, no voy a ponerle mas max_dpeth para no hacer un overfit del modelo

## finalmente con estos nuevos parametros parece que el mejor es gini, con min_samples_split = 4 y el max_depth sea 20. Tienen bastante buen accuracy asi que vamos a dejarlo asi. Creamos nuevamente este nuevo mejor arbol y vemos las metricas definitivas

# arbol_mejor = DecisionTreeClassifier(min_samples_split=4, criterion='gini',max_depth=20) 
# Entrenamos el modelo
arbol_mejor = DecisionTreeClassifier(min_samples_split=7, criterion='gini',max_depth=3,random_state=seed)
arbol_mejor.fit(X_train,y_train)


# Predicciones en conjunto de entrenamiento y prueba
y_train_pred = arbol_mejor.predict_proba(X_train)[:,1]
y_train_pred_2 = arbol_mejor.predict(X_train)
y_test_pred = arbol_mejor.predict_proba(X_test)[:,1]
y_test_pred_2 = arbol_mejor.predict(X_test)

## accuracy score
print(f'Se tiene un accuracy para train de: {accuracy_score(y_train,y_train_pred_2)}')
print(f'Se tiene un accuracy para test de: {accuracy_score(y_test,y_test_pred_2)}')
print('Comprobar que la diferencia no sea muy grande por temas de sobreajuste')

##############3 vamos con la precicsion socre
precision=precision_score(y_train, y_train_pred_2)
precision_test=precision_score(y_test,y_test_pred_2)
print(f"Precisión train: {precision}")
print(f"Precisión test: {precision_test}")

################ vamos con la recall score

## aqui hablamos de la sensibilidad
recall = recall_score(y_train, y_train_pred_2)
recall_test = recall_score(y_test,y_test_pred_2)
print(f"Recall/sensibilidad train: {recall}")
print(f"Recall/sensibilidad test: {recall_test}")
###3 vamos con el f1 score
f1=f1_score(y_train, y_train_pred_2)
f1_test=f1_score(y_test, y_test_pred_2)
print(f"F1_score train: {f1}")
print(f"F1_score test: {f1_test}")

## ahora vamos a ver gráficamente algunas de estas métricas
## matriz de confusion
cm = confusion_matrix(y_train, y_train_pred_2)
clases = ['Cliente no deja (0)', 'Cliente deja (1)']
# Crear un mapa de calor para mejorar la visualización
plt.figure(figsize=(2, 2))
sns.heatmap(cm, annot=True, cmap='Greens', fmt='g', xticklabels=clases, yticklabels=clases)
plt.xlabel('Valores predichos')
plt.ylabel('Valores reales')
plt.title('Matriz de confusión')
plt.show()
plt.close()



# vamos a ver ahora graficamente la curva roc
fpr, tpr, thresholds = roc_curve(y_train, y_train_pred)
print(f"Tasa de falsos positivos: {fpr}")
print(f"Tasa de verdaderos positivos: {tpr}")
print(f"Puntos de corte (thresholds): {thresholds}")
roc_auc = auc(fpr, tpr)
print(f"AUC: {roc_auc}")
print('El valor del AUC nos dice que el modelo ha hecho una clasificación aleatoria')

plt.figure()
plt.plot(fpr, tpr, color='darkorange',
         label='ROC curve')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--') 
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('FPR=1-especifidad')
plt.ylabel('TPR=recall')
plt.title('Curva ROC')
plt.legend(loc="lower right")
plt.show()

## segun vemos las metricas puede realmente parecer un overfitting...

print(f'La frecuencia de cada clase en train es: \n{y_train.value_counts(normalize=True)}')
print(f'\nLa frecuencia de cada clase en test es: \n{y_test.value_counts(normalize=True)}')

# Conocer los niveles de la variable a predecir
print(arbol_mejor.classes_)
# Conocer el nombre de las variables predictoras
print(arbol_mejor.feature_names_in_)
# Obtener información detallada de cada nodo y las reglas de decisión
tree_rules = export_text(arbol_mejor, feature_names=list(x.columns),show_weights=True)
print(tree_rules)
## AQUI EN ESTE ARBOL SE VE COMO SE HA FORMADO entonces donde pone weights: ['cantidad de iondividuos q no','cantidad de individuos que si'] basandose en esto, los pone en una clase u en otra

# se puede ver graficamnete tmb<>:
plt.figure(figsize=(30, 15))
plot_tree(arbol_mejor, feature_names=x.columns.tolist(), class_names=['No', 'Yes'], filled=True,
         proportion = True)
plt.show()

###########################################################################################################################3
















###########################################3 Random forest y xgboost #####################################################
#########################################3Random fortest primero##########################################################
arbol_rf = RandomForestClassifier(max_depth = 3, criterion='gini', random_state=seed) 
arbol_rf.fit(X_train, y_train)
# Predicciones en conjunto de entrenamiento y prueba
y_train_pred_rf = arbol_rf.predict_proba(X_train)[:,1]
y_train_pred_2_rf = arbol_rf.predict(X_train)
y_test_pred_rf = arbol_rf.predict_proba(X_test)[:,1]
y_test_pred_2_rf = arbol_rf.predict(X_test)
# vamos a agregarle poco max_depth para que no nos pase como antes (mx 3), criterio agrego el gini como antes, el resto, default

## vemos algunas metricas y verificamos si hay algun otro modelo mejor


# Medidas de bondad de ajuste en train
print(f'Se tiene un accuracy para train de: {accuracy_score(y_train,y_train_pred_2_rf)}')
print(f'Se tiene un accuracy para test de: {accuracy_score(y_test,y_test_pred_2_rf)}')
print('Comprobar que la diferencia no sea muy grande por temas de sobreajuste')


##############3 vamos con la precicsion socre
precision=precision_score(y_train, y_train_pred_2_rf)
precision_test=precision_score(y_test,y_test_pred_2_rf)
print(f"Precisión train: {precision}")
print(f"Precisión test: {precision_test}")

################ vamos con la recall score

## aqui hablamos de la sensibilidad
recall = recall_score(y_train, y_train_pred_2_rf)
recall_test = recall_score(y_test,y_test_pred_2_rf)
print(f"Recall/sensibilidad train: {recall}")
print(f"Recall/sensibilidad test: {recall_test}")
###3 vamos con el f1 score
f1=f1_score(y_train, y_train_pred_2_rf)
f1_test=f1_score(y_test, y_test_pred_2_rf)
print(f"F1_score train: {f1}")
print(f"F1_score test: {f1_test}")

## ahora vamos a ver gráficamente algunas de estas métricas
## matriz de confusion
cm = confusion_matrix(y_train, y_train_pred_2_rf)
clases = ['Cliente no deja (0)', 'Cliente deja (1)']
# Crear un mapa de calor para mejorar la visualización
plt.figure(figsize=(2, 2))
sns.heatmap(cm, annot=True, cmap='Greens', fmt='g', xticklabels=clases, yticklabels=clases)
plt.xlabel('Valores predichos')
plt.ylabel('Valores reales')
plt.title('Matriz de confusión')
plt.show()
plt.close()

## como podemos ver no esta mal el modelo pero vamos a buscar uno mejor. usamos grid_search nuevamente

params_rf = {
    'max_depth': [2, 3],
    'min_samples_split': [4,5,10, 20],
    'criterion': ["gini", "entropy"]
}
#recordar que arbol2 es el árbol cuyas VI son todas las variables.
# cv = crossvalidation
grid_search_rf = GridSearchCV(estimator=arbol_rf, 
                           param_grid=params_rf, 
                           cv=4, scoring = scoring_metrics, refit='accuracy') # vemos conm accuracy ya q es loq  pide el modelo

grid_search_rf.fit(X_train, y_train)
# Obtener resultados del grid search
results_rf = pd.DataFrame(grid_search_rf.cv_results_)
sorted_results_rf = results_rf.sort_values(by='mean_test_accuracy', ascending=False)
pd.set_option('display.max_colwidth', None)
# Mostrar resultados
print("Resultados de Grid Search:")
print(sorted_results_rf[['params', 'mean_test_accuracy', 'mean_test_precision_macro', 'mean_test_recall_macro', 'mean_test_f1_macro']])
# segun podemos ver el mejor modelo seria con gini, maxdepth 3 y min_samples split 3, pero vamos a inverstigar mejor los 5 mejores modelos q tenemos
res_1 = sorted_results_rf[['split0_test_accuracy', 'split1_test_accuracy','split2_test_accuracy', 'split3_test_accuracy']].iloc[0]
res_2 = sorted_results_rf[['split0_test_accuracy', 'split1_test_accuracy','split2_test_accuracy', 'split3_test_accuracy']].iloc[1]
res_3 = sorted_results_rf[['split0_test_accuracy', 'split1_test_accuracy','split2_test_accuracy', 'split3_test_accuracy']].iloc[2]
res_4 = sorted_results_rf[['split0_test_accuracy', 'split1_test_accuracy','split2_test_accuracy', 'split3_test_accuracy']].iloc[3]
res_5 = sorted_results_rf[['split0_test_accuracy', 'split1_test_accuracy','split2_test_accuracy', 'split3_test_accuracy']].iloc[4]
plt.boxplot([res_1.values,res_2.values,res_3.values,res_4.values,res_5.values], label = ['res_1','res_2','res_3','res_4','res_5'])
plt.title('Boxplots de Accuracy para los 4 Splits')
plt.xlabel('Splits de Cross Validation')
plt.ylabel('Accuracy')
plt.show()

# aqui podemos ver dos posibilidades buenas.
# - el modelo 1 tiene buena pinta ya q es el que mejor accuracy tiene yno tiene tanta variabilidad como el 2,3 y 5 pero el punt de abajo es un poco preocupante ya que peude ser que alguna vez caiga aqui
# - el modelo 4 tiene buena pinta tamb ya qu ees el q menos variabilidad tiene y no tiene muchoa ccuracy menos que el 1, pero es cierto q tiene algo menos

# como estamos viendo por accuracy, nos quedamos el modelo 1

arbol_rf_mejor = RandomForestClassifier(**sorted_results_rf['params'].iloc[0], random_state=seed)
arbol_rf_mejor.fit(X_train, y_train)

# Predicciones en conjunto de entrenamiento y prueba
y_train_pred_rf = arbol_rf_mejor.predict_proba(X_train)[:,1]
y_train_pred_2_rf = arbol_rf_mejor.predict(X_train)
y_test_pred_rf = arbol_rf_mejor.predict_proba(X_test)[:,1]
y_test_pred_2_rf = arbol_rf_mejor.predict(X_test)
# vamos a agregarle poco max_depth para que no nos pase como antes (mx 3), criterio agrego el gini como antes, el resto, default

## vemos algunas metricas y verificamos si hay algun otro modelo mejor


# Medidas de bondad de ajuste en train
print(f'Se tiene un accuracy para train de: {accuracy_score(y_train,y_train_pred_2_rf)}')
print(f'Se tiene un accuracy para test de: {accuracy_score(y_test,y_test_pred_2_rf)}')
print('Comprobar que la diferencia no sea muy grande por temas de sobreajuste')


##############3 vamos con la precicsion socre
precision=precision_score(y_train, y_train_pred_2_rf)
precision_test=precision_score(y_test,y_test_pred_2_rf)
print(f"Precisión train: {precision}")
print(f"Precisión test: {precision_test}")

################ vamos con la recall score

## aqui hablamos de la sensibilidad
recall = recall_score(y_train, y_train_pred_2_rf)
recall_test = recall_score(y_test,y_test_pred_2_rf)
print(f"Recall/sensibilidad train: {recall}")
print(f"Recall/sensibilidad test: {recall_test}")
###3 vamos con el f1 score
f1=f1_score(y_train, y_train_pred_2_rf)
f1_test=f1_score(y_test, y_test_pred_2_rf)
print(f"F1_score train: {f1}")
print(f"F1_score test: {f1_test}")

## ahora vamos a ver gráficamente algunas de estas métricas
## matriz de confusion
cm = confusion_matrix(y_train, y_train_pred_2_rf)
clases = ['Cliente no deja (0)', 'Cliente deja (1)']
# Crear un mapa de calor para mejorar la visualización
plt.figure(figsize=(2, 2))
sns.heatmap(cm, annot=True, cmap='Greens', fmt='g', xticklabels=clases, yticklabels=clases)
plt.xlabel('Valores predichos')
plt.ylabel('Valores reales')
plt.title('Matriz de confusión')
plt.show()
plt.close()

## para esto primero empezamos viendo por ejemplo la importancia de las variables input
df_importancia = pd.DataFrame({'Variable': arbol_rf_mejor.feature_names_in_, 'Importancia': arbol_rf_mejor.feature_importances_}).sort_values(by='Importancia', ascending=False)

# Crear un gráfico de barras
plt.bar(df_importancia['Variable'], df_importancia['Importancia'], color='skyblue')
plt.xlabel('Variable')
plt.ylabel('Importancia')
plt.title('Importancia de las características')
plt.xticks(rotation=45, ha='right')  # Rotar los nombres en el eje x para mayor legibilidad
plt.tight_layout()
plt.show()
######################################################################################################################33














############################################ xgboost segundo#######################################################333
arbol_xgb = XGBClassifier(booster = 'gbtree', random_state=seed, max_depth = 3, tree_method = 'hist')
arbol_xgb.fit(X_train, y_train)
# Predicciones en conjunto de entrenamiento y prueba
y_train_pred_xgb = arbol_xgb.predict_proba(X_train)[:,1]
y_train_pred_2_xgb = arbol_xgb.predict(X_train)
y_test_pred_xgb = arbol_xgb.predict_proba(X_test)[:,1]
y_test_pred_2_xgb = arbol_xgb.predict(X_test)
# vamos a agregarle poco max_depth para que no nos pase como antes (mx 3), criterio agrego el gini como antes, el resto, default

## vemos algunas metricas y verificamos si hay algun otro modelo mejor


# Medidas de bondad de ajuste en train
print(f'Se tiene un accuracy para train de: {accuracy_score(y_train,y_train_pred_2_xgb)}')
print(f'Se tiene un accuracy para test de: {accuracy_score(y_test,y_test_pred_2_xgb)}')
print('Comprobar que la diferencia no sea muy grande por temas de sobreajuste')

##############3 vamos con la precicsion socre
precision=precision_score(y_train, y_train_pred_2_xgb)
precision_test=precision_score(y_test,y_test_pred_2_xgb)
print(f"Precisión train: {precision}")
print(f"Precisión test: {precision_test}")

################ vamos con la recall score

## aqui hablamos de la sensibilidad
recall = recall_score(y_train, y_train_pred_2_xgb)
recall_test = recall_score(y_test,y_test_pred_2_xgb)
print(f"Recall/sensibilidad train: {recall}")
print(f"Recall/sensibilidad test: {recall_test}")
###3 vamos con el f1 score
f1=f1_score(y_train, y_train_pred_2_xgb)
f1_test=f1_score(y_test, y_test_pred_2_xgb)
print(f"F1_score train: {f1}")
print(f"F1_score test: {f1_test}")

## ahora vamos a ver gráficamente algunas de estas métricas
## matriz de confusion
cm = confusion_matrix(y_train, y_train_pred_2_xgb)
clases = ['Cliente no deja (0)', 'Cliente deja (1)']
# Crear un mapa de calor para mejorar la visualización
plt.figure(figsize=(2, 2))
sns.heatmap(cm, annot=True, cmap='Greens', fmt='g', xticklabels=clases, yticklabels=clases)
plt.xlabel('Valores predichos')
plt.ylabel('Valores reales')
plt.title('Matriz de confusión')
plt.show()
plt.close()

## como podemos ver no esta mal el modelo pero vamos a buscar uno mejor. usamos grid_search nuevamente

params_xgb = {
    'n_estimators': [100,200,300],
    'eta' : [0.1,0.4,0.7],
    'gamma' : [0.1,0.5,1],
    'max_depth': [2,3]
}

#recordar que arbol2 es el árbol cuyas VI son todas las variables.
# cv = crossvalidation
grid_search_xgb = GridSearchCV(estimator=arbol_xgb, 
                           param_grid=params_xgb, 
                           cv=4, scoring = scoring_metrics, refit='accuracy') # vemos conm accuracy ya q es loq  pide el modelo

grid_search_xgb.fit(X_train, y_train)
# Obtener resultados del grid search
results_xgb = pd.DataFrame(grid_search_xgb.cv_results_)
sorted_results_xgb = results_xgb.sort_values(by='mean_test_accuracy', ascending=False)
pd.set_option('display.max_colwidth', None)
# Mostrar resultados
print("Resultados de Grid Search:")
print(sorted_results_xgb[['params', 'mean_test_accuracy', 'mean_test_precision_macro', 'mean_test_recall_macro', 'mean_test_f1_macro']])
# segun podemos ver el mejor modelo seria con gini, maxdepth 3 y min_samples split 3, pero vamos a inverstigar mejor los 5 mejores modelos q tenemos
res_1 = sorted_results_xgb[['split0_test_accuracy', 'split1_test_accuracy','split2_test_accuracy', 'split3_test_accuracy']].iloc[0]
res_2 = sorted_results_xgb[['split0_test_accuracy', 'split1_test_accuracy','split2_test_accuracy', 'split3_test_accuracy']].iloc[1]
res_3 = sorted_results_xgb[['split0_test_accuracy', 'split1_test_accuracy','split2_test_accuracy', 'split3_test_accuracy']].iloc[2]
res_4 = sorted_results_xgb[['split0_test_accuracy', 'split1_test_accuracy','split2_test_accuracy', 'split3_test_accuracy']].iloc[3]
res_5 = sorted_results_xgb[['split0_test_accuracy', 'split1_test_accuracy','split2_test_accuracy', 'split3_test_accuracy']].iloc[4]
plt.boxplot([res_1.values,res_2.values,res_3.values,res_4.values,res_5.values], label = ['res_1','res_2','res_3','res_4','res_5'])
plt.title('Boxplots de Accuracy para los 4 Splits')
plt.xlabel('Splits de Cross Validation')
plt.ylabel('Accuracy')
plt.show()

# aqui podemos ver dos posibilidades buenas.
# - el modelo 1 tiene buena pinta ya q es el que mejor accuracy tiene yno tiene tanta variabilidad como el 2,3 y 5 pero el punt de abajo es un poco preocupante ya que peude ser que alguna vez caiga aqui
# - el modelo 4 tiene buena pinta tamb ya qu ees el q menos variabilidad tiene y no tiene muchoa ccuracy menos que el 1, pero es cierto q tiene algo menos

# como estamos viendo por accuracy, nos quedamos el modelo 1

arbol_xgb_mejor = XGBClassifier(**sorted_results_xgb['params'].iloc[0], random_state=seed)
arbol_xgb_mejor.fit(X_train, y_train)

# Predicciones en conjunto de entrenamiento y prueba
y_train_pred_xgb = arbol_xgb_mejor.predict_proba(X_train)[:,1]
y_train_pred_2_xgb = arbol_xgb_mejor.predict(X_train)
y_test_pred_xgb = arbol_xgb_mejor.predict_proba(X_test)[:,1]
y_test_pred_2_xgb = arbol_xgb_mejor.predict(X_test)
# vamos a agregarle poco max_depth para que no nos pase como antes (mx 3), criterio agrego el gini como antes, el resto, default

## vemos algunas metricas y verificamos si hay algun otro modelo mejor


# Medidas de bondad de ajuste en train
print(f'Se tiene un accuracy para train de: {accuracy_score(y_train,y_train_pred_2_xgb)}')
print(f'Se tiene un accuracy para test de: {accuracy_score(y_test,y_test_pred_2_xgb)}')
print('Comprobar que la diferencia no sea muy grande por temas de sobreajuste')


##############3 vamos con la precicsion socre
precision=precision_score(y_train, y_train_pred_2_xgb)
precision_test=precision_score(y_test,y_test_pred_2_xgb)
print(f"Precisión train: {precision}")
print(f"Precisión test: {precision_test}")

################ vamos con la recall score

## aqui hablamos de la sensibilidad
recall = recall_score(y_train, y_train_pred_2_xgb)
recall_test = recall_score(y_test,y_test_pred_2_xgb)
print(f"Recall/sensibilidad train: {recall}")
print(f"Recall/sensibilidad test: {recall_test}")
###3 vamos con el f1 score
f1=f1_score(y_train, y_train_pred_2_xgb)
f1_test=f1_score(y_test, y_test_pred_2_xgb)
print(f"F1_score train: {f1}")
print(f"F1_score test: {f1_test}")

## ahora vamos a ver gráficamente algunas de estas métricas
## matriz de confusion
cm = confusion_matrix(y_train, y_train_pred_2_xgb)
clases = ['Cliente no deja (0)', 'Cliente deja (1)']
# Crear un mapa de calor para mejorar la visualización
plt.figure(figsize=(2, 2))
sns.heatmap(cm, annot=True, cmap='Greens', fmt='g', xticklabels=clases, yticklabels=clases)
plt.xlabel('Valores predichos')
plt.ylabel('Valores reales')
plt.title('Matriz de confusión')
plt.show()
plt.close()

## para esto primero empezamos viendo por ejemplo la importancia de las variables input
df_importancia = pd.DataFrame({'Variable': arbol_xgb_mejor.feature_names_in_, 'Importancia': arbol_xgb_mejor.feature_importances_}).sort_values(by='Importancia', ascending=False)

# Crear un gráfico de barras
plt.bar(df_importancia['Variable'], df_importancia['Importancia'], color='skyblue')
plt.xlabel('Variable')
plt.ylabel('Importancia')
plt.title('Importancia de las características')
plt.xticks(rotation=45, ha='right')  # Rotar los nombres en el eje x para mayor legibilidad
plt.tight_layout()
plt.show()
#######################################################################################################################333

################################### ultimo apartado explicación###############################
# este apartado se encuentra completo dentro del word/pdf de entrega de la tarea
############################################################################################3
########################################################################################################33

