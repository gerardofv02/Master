
y_true = [1, 1, 1, 0, 1, 0]
y_pred = [1, 1, 0, 1, 0, 0]


## vamos a construir las métricas¡ de bondad de ajuste


####### COmenzamos con la matriz de confusion#####################################33
from sklearn.metrics import confusion_matrix
#.rabvel() convierte un arreglo de varias dimensiones en una secuencia lineal de elementos. 
#En este caso, una matriz de confusión 2x2 a un array con 4 elementos
#es más rápido que .flatten() porque no hace copias
tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel() # sirve apra aplanar la matriz de confusion

#otra forma de obtener los elementos de la matriz de confusión sin aplanarla
cm = confusion_matrix(y_true, y_pred)
tn, fp, fn, tp= cm[0][0], cm[0][1], cm[1][0], cm[1][1]     
print(f"Los elementos de la matriz de confusión son tn: {tn}; fp: {fp}; fn: {fn} y tp: {tp}.")



import matplotlib.pyplot as plt
import seaborn as sns
clases = ['No Spam (0)', 'Spam (1)']

# Crear un mapa de calor para mejorar la visualización
plt.figure(figsize=(2, 2))
sns.heatmap(cm, annot=True, cmap='Greens', fmt='g', xticklabels=clases, yticklabels=clases)
plt.xlabel('Valores predichos')
plt.ylabel('Valores reales')
plt.title('Matriz de confusión')
plt.show()
plt.close()

## aqui le podemos añadir color a la matriz de confusion

################################################################################################ç
########## vamos con el accuracy score#####################################################

from sklearn.metrics import accuracy_score
accuracy = accuracy_score(y_true, y_pred)
print(f"Accuracy: {accuracy}")
################################################################################################

##############3 vamos con la precicsion socre#####################################################################
from sklearn.metrics import precision_score
precision=precision_score(y_true, y_pred)
print(f"Precisión: {precision}")
#################################################################################################

################ vamos con la recall score#####################################################################

from sklearn.metrics import recall_score ## aqui hablamos de la sensibilidad
recall = recall_score(y_true, y_pred)
print(f"Recall/sensibilidad: {recall}")
##################################################################################################3
#################3 vamos con el f1 socre#####################################################################
from sklearn.metrics import f1_score
f1=f1_score(y_true, y_pred)
print(f"F1_score: {f1}")
#####################################################################################################

####################33 También se pueden calcular de forma manual las métricas de bondad de ajuste a partir de los elementos de la matriz de confusión########################
accuracy=(tp+tn)/(tp+tn+fp+fn)
print(f"Accuracy: {accuracy}")
precision=tp/(tp+fp)
print(f"Precisión: {precision}")
recall=tp/(tp+fn)
print(f"Recall/sensibilidad: {recall}")
f1=2*((precision*recall)/(precision+recall))
print(f"F1_score: {f1}")
especifidad = tn / (tn + fp)
print(f"Especificidad: {especifidad}")

###############################################################################################################

################### ahroa vamos con el calculo de la curv roc ########################################################
from sklearn.metrics import roc_curve, auc
#roc_curve calcula las tasas fpr y tpr para distintos punto de corte, establecidos por el sistema dependiendo de los datos
fpr, tpr, thresholds = roc_curve(y_true, y_pred)
print(f"Tasa de falsos positivos: {fpr}")
print(f"Tasa de verdaderos positivos: {tpr}")
print(f"Puntos de corte (thresholds): {thresholds}")
## esta se puede aplicar cuando nuestra vaiabrle predicha son probabilidades  
#####################################################################################################
roc_auc = auc(fpr, tpr)
print(f"AUC: {roc_auc}")
print('El valor del AUC nos dice que el modelo ha hecho una clasificación aleatoria')

################33 una vez tenemos la curva ORC la podemos dibujar dandole coordenadas: #####################
plt.figure()
plt.plot(fpr, tpr, color='darkorange',
         label='ROC curve')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--') #lw indica el grosor de la línea. la línea naranja es la referencia de la clasificación aleatoria
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('FPR=1-especifidad')
plt.ylabel('TPR=recall')
plt.title('Curva ROC')
plt.legend(loc="lower right")
plt.show()
### eje x falsos postivios
#### eje y verdadreos positivos
#######################################################################################################

######################33 Vamos ahora con un problema de variable continua ###############################
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
# Datos reales (precios reales de las viviendas en miles de euros)
y_true = np.array([300, 450, 200, 500])
# Datos predichos (precios predichos por el modelo en miles de euros)
y_pred = np.array([320, 430, 210, 490])

 # 1. Calcular el MSE (Error Cuadrático Medio)
# --------------------
# Fórmula manual: MSE = promedio((y_true - y_pred)^2)
mse_manual = np.mean((y_true - y_pred) ** 2)
print(f"MSE (manual): {mse_manual}")
# Usando scikit-learn
mse_sklearn = mean_squared_error(y_true, y_pred)
print(f"MSE (scikit-learn): {mse_sklearn}")

# 2. Calcular el RMSE (Raíz del Error Cuadrático Medio)
# --------------------
# Fórmula manual: RMSE = sqrt(MSE)
rmse_manual = np.sqrt(mse_manual)
print(f"RMSE (manual): {rmse_manual}")

# Usando scikit-learn (calculando la raíz del MSE)
rmse_sklearn = np.sqrt(mse_sklearn)
print(f"RMSE (scikit-learn): {rmse_sklearn}")


# 3. Calcular el MAE (Error Absoluto Medio)
# --------------------
# Fórmula manual: MAE = promedio(|y_true - y_pred|)
mae_manual = np.mean(np.abs(y_true - y_pred))
print(f"MAE (manual): {mae_manual}")

# Usando scikit-learn
mae_sklearn = mean_absolute_error(y_true, y_pred)
print(f"MAE (scikit-learn): {mae_sklearn}")

# 4. Calcular el R2 (Coeficiente de Determinación)
# --------------------
# Fórmula manual: R2 = 1 - (SS_res / SS_tot)
# SS_res = suma((y_true - y_pred)^2)
# SS_tot = suma((y_true - promedio(y_true))^2)
ss_res = np.sum((y_true - y_pred) ** 2)
ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
r2_manual = 1 - (ss_res / ss_tot)
print(f"R² (manual): {r2_manual}")

# Usando scikit-learn
r2_sklearn = r2_score(y_true, y_pred)
print(f"R² (scikit-learn): {r2_sklearn}")

#######################################################################################################