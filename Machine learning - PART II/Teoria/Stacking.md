# Stacking

ESte modelo tambien conocido como blending o averaging es para casos mas generales.
1. Averaging: SE calcula el promedio de las predicciones . SI se trata de clasificacion, se obtiene el promedio de probabilidades. SE puede utilziar también el promedio ponderado.
2. Voto (para clasificaciones): se predice el resultadocon mayoria entre las predicciones
3. Combinacion a paritr de otro algoritmo: por ejemplo, se introduce una regresion y un arbol como variables independientes. Esto equivaldría en regresion a u  promedio de modelos con distintos pesos


Esdta tecnica enseemble va un más allá del bagging y el boosting al combinar las predicciones de diferentes modelos base, pero en lugar de utilizar métodos simples de combinación como el promedio o la votación, emplea un modelo adicional llamado 'meta-modelo' o 'modelo apilaod' para realizar la combinación fina.

EL stacking permite que el modelo final aprovechelas fortalezas de cada modelo base y pueda aprender a realizar una combinacion ponderada de sus predicciones. ESto puede conducir a un mejor rendimiento en comparacion con cualquier modelo base individual.
EL stacking es un modelo muy flexible que se adpata bien a cualquier tipo de problemas con una buena eleccion del modelo base y sus parametros.

## Pasos

1. SEleccion del modelo base
2. División del conjunto de datos
3. ENtrenamiento de modelo base
4. Generación de predicciones de modelo base
5. Creacion del conjunto de datos meta: utilizar las predicciones d elos modelos base como caracterisitcas para constuir un nuevo conjunto de datos  llamad meta.
6. Entrenamiento del meta-modelo
7. Prediccion final

OJO: el conjunto de datos meta solo se usan con el meta-modelo y no debe confundirse con los datos originals