# TEma 2

## Ecploracion de los datos

La idea principal es que conozcamos los datos:
    - Variables categoricas y numericas
    - Distribucion de los datos
    - Null values
    - Outliers
    - Balanceo de datos
    - RElacion entre variables

## TRansformacion de variables

### REscale

REscalar los valores en el intervalo de 0,1

pros y contras:
    - Eliminamos unidades magnitudes
    - Se compra mejor entre variables, se interpretan mejor los resultados

### Estandarizacion

COnsiste en tipificar los datos

Pros y contras:
    - Eliminamos unidades (magnitudes)
    - CEntraliza los valores alrededor del 0
    - NO mejora skewness/kurtosis
    - Con datos no distribuidos normalmente, no gama,os mucho

## seleccion de vairables predictivas

COnsiste en usar criterios para escoger las varaibles más robustas y con mayor capacidad predictora

En este ejemplo vamos a trabajar las sigueitnes técnicas:
    - Chi-squared test
    - REcursive feature elimination
    - Principal component analist
    - Feature importance

### Chi-squared

Podemos elegir variables robustas basandonos en test analisticos
El test chi-squared contrasta cada bariablecon la variable target, es un test de independencia que destaca aquellas que son relevantes para la clasificacion

### FEature importance

A los algoritmos (tipo regresion) podemos consultarles tras ser entrenados por el valor de sus coeficientes de las variables para saber su relevancia en la predicción de las variables objetivo
A los algortimos (tipo árbol) podemos consultarles tras ser entrenados por la importancia de las variables (que está basado en el factor de impuridad de gini

### PCA

ES una técnica  para reduccion de variables basandose en la extraccion de los autovalores y autovectores de la matriz de  varianzas-covarianzas. ES decir, localizando aquellas variables que más varianza acumulen

### REcursive feature elimination

RFE elimina una a una las variables que menos importancia tienen para el modelo
Ajusta el algoritmo tantas veces como variables tenemos menos el número de variables deseavles

##  Técnicas de validacion

La mejor manera  de evaluar la calidad de los algoritmos seria hacer prediccionespara nuevos datos de los que ya se conocen las respuestas
Para ello, se utilizan tñecnicas de remuestreoque permiten hacer estimaciones precisas de cuán bien se ajusta un algoritmo con los datos
EN este ejemplo vamos a trabajar las sigueintes técnicas:
    - TRain test sets
    - kfolds corss validation
    - LEave one out cross validation
    - Shuffle split corss validation


### Train test sets
Subdividimos el dataset original de dos partes: train y test. ENtrenamos el calgoritmo con train y hacemos predicciones con test

pros y cons:
    - ES la técnicamas sencilla y rapida. Ideal apra datasets muy grandes
    - NO suele ajustar muy bien con modelos muy sesgados

### k-folds cross validation

SUbdividimos el dataset original en k partes. A cada parte la llamamos fold. EL algoritmo ahora se entrena con k-1folds y se testea restante. SE repite este proceso k veces.
Pros y cons:
    - ES mas lenta, tarda mas tiempo computacional
    - ES mas robusta a modelos sesgados

### LOO CROSS VALIDATION

Subdividimos el dataset original en k folds, pero k sera el numero de registros
pros y cons:
    - ES muy lenta, y muy costosa computacionalmente
    - ES mas robusta a modelos sesgados

### Shuffle split cross-validation

ES otra variante enla que realizar un train/test completamente aleatorio cada vez

Pros y cons:
    - Cada repeticion puede incluir los mismos datos en cada conjunto

## Métricas

SIrven para evaluar la bondad de un modelo
Las metricas influyen ademas en el entrenamiento de cualquier modelo, ya que son la funcion de perdida que el algoritmo siempre trata de optimizar
DEpendiendo del tipo del problema, las metricas son diferentes. En este ejemplo, trabajaremoslas siguientes métricas de clasificación:
    - COnfussion matrix
    - accuracy
    - LOgarithmic loss
    - AUC - Area under roc curve

### matriz de confusion

Tras entrenar un algoritmo de clasificacion, podemos examinar los resutlados en esta matriz
A partir de esta matriz podemos crear diversas métricas: accuracy, recall,...

### Accuracy

ES la proporción de registros correctamente clasificados
    - COmo accuracy, otras métricas pueden extraerse de la matriz de confusion: precisión,..

### Negative logarithmic loss

Basada en la entropía y la función log-likehood (verosimilitud)

### AUC

ROC nos permite estimar la relación entre tasa de falsos positivos y verdaderos positivos
    - EL área máxima es 1 y el mínimo es 0.5


## Parametrizacion de algoritmos

Cada algoritmo ofrece distintas opciones de parametrización. DEpendiendo del algoritmo elegido como base del modelo, ahora tendremos que tomar la mejor configuración para que los resultados sean mejores

### Grid search

Vamos a configurar alguna de estas aprametrizaciones y ejecutar varias pruebas de modelos para ver, como respuesta, qué parametrización ofrece resultados óptimos
