# Machine learning PART II 

## Introducción

### Porblemas predictivos supervisados
Prediccion de una variable continua, prediccion de variable binaria o multiclase

Los algoritmos de machine leagrmning mas tipicos son:
- Regresión
- Regresión logística
- Redes neuronales
- Árboles de decisión, Random forest y gradient boosting
- Support vector machines -> Este modulo se centra especialemnte en este

Todos estos tienen una cosa en comun: la variable objetivo es una variable continua (predecir ventas, clientes que se van,...).

### Problemas predictivos no supervisados
Clustering, segmentacion y reduccion de dimensiones, busquedas de estructuras.

Algortimos mas conocidos y eficientes:
- Algoritmos de clustering (k-means, jerarquicos,...)
- Analisis factorial, analisis de correspondencias  

## Pasos a seguir

- Preparacion de datos (80% que se le dedcia al ML)
    - EDA. Analisis descripptivo de los datos. Conocer el programa
    - Cleanning. Limpieza de datos (missing y anómalos)ç
    - FE (feature engineering). Transformación de vairables

- Métricas de muestreo (validacion de algoritmos)
- Metricas de precision (medidas para validar el ajuste/error del modelo)
- Seleccion de algoritmos
- Puesta a punto del algoritmo
    - Seleccion de variables (ojo se puede hacer desde el paso 1)
    - Parametrizacion/tuneo del algoritmo


### Transformacion de las variables

Esta fase consiste en realizar transformaciones de las variable sque permitan discriminar mejor las clases objetivos. Siempre se usan y que suele funcioinar son:
- Reescalar datos
- Estandarizar los datos
- Normalizar los datos
- Binarizar los datos
- Categorizar variables continuas
- Agrupar/eliminar categorias poco representadas
- ...

### Técnicas de muestreo

para poder evaluar la calidad de los modelos se utilizan este tipo de técnicas. Las mas conocidas:
- Train/tests sets
- k-folds cross-validation
- Leave one out(LOO) cross-validation
- Shuffle split cross-validation

### Medidas de precision de un modelo

Permiten evaluar la calidad de un modelo. Son las medidas que se quieren optimizar con el algoritmo de aprendizaje automatico, por lo que tienen un impacto importante en la fase de entrenamiento.
No se usan medidas si el problema es de clasificación o si es de regresión. Las mas usadas son las siguientes:
- Matriz de confusión
- Accuracy
- Kappa 
- AUC - Area sobre la curva ROC

### Selección de algoritmo

Según el propblema a tratar, se coge uno u otro. Entre otros, están:
- Logistic regression
- Redes
- K-nearest neiughbours
- Naive bayes
- Classification tree
- Support vector machines
- Random forest
- Eseembles & stacking