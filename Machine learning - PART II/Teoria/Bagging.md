# Bagging

## ¿Mezclar funciona?

Parace que mezclar funciona. Hay mcuhos escenarios poibles
- Que un modelo sea manifiestamente mejor que los demás, en general todas las regiones de X -> la solución buena sería utilizar ese algoritmo
- Que en promedioalgunos algoritmos funcionen igual de bien pero hay discrepancia según las regiones de X-> si están identificadas estas regiones se pueden particionar las predicciones y aplicar el algoritmo adecuado a cada región
- Que los datos de performance sean oscuros, hay discrepancias entre modelos, en promedioparecen funcionar similar pero su performance relativa varía de partición a partición -> se puede estudiar empíricamente el funcionamiento de métodos ensemble
- etc...


## Principales métodos de esemble: agregacion

- Promedio:Consiste en tomar el promedio de las predicciones de los modelosen caso de problemasde regresiono al predecirprobabilidades en problemas de clasificación
- voto mayoritario:Eleccion de la predicción con el voto/recomendacionmaximo entre las prediccionesde varios modelos al prever el resultado de un problema de clasificacion
- promedio ponderado: Se aplicacn diferentes pesos a las prediccionesde varios modelos y luego se calcula el promedio, lo que implica asignar una importancia alta o baja a la salida específica de un modelo en particular

##Bagging
La agregación bootstrap, también conocida como bagging, es un meta-algoritmo diseñado para conseguir combinaciones  de modelos a partir de  una familia inicial, provocandouna disminucionde la varianza y evitando el sobreajuste.Lo mas común es aplicarlo con los métodos basados en arboles de decisiónpero se puede usar con cualquier familia de algoritmos

### Bagging arboles de decision
Para construir bagged trees, el proceso es facil. Supongamos que se queiren construir 100 modelos de arbol que posteriormente promediarán. Para cada uno de los 100 modelos:

1. Tomar una muestra con reemplazo del conjunto de datos original
2. Entrenar un árbol en esta muestra
3. Conservar un modelo predictivo
4. Una vez que todos los modelosestén entrenados, para obtener una predicicon del modelo de ensamblado sobre nuesvos datos:
	1. Obtener estimacion sobre datos nuevos de cada uno de los arboles individuales
	2. Agregar las estimaciones  de los arvoles individualespara obtener la solución final
	
### Bagging boostrap agregating

En esencia bagging hace uso de técnicas de remuestreo boostrap para entrenar multiples modelosen conjuntos de datos ligeramente difrentes y luego promediar  o vombinar sus predicciones. El termino boostrap averaging  se refiere a este procesoo deonde se generan multiples conjuntos de datos de entrenamiento mediante muestreo con reemplazo. Estos conjuntos de datos se utilizan para entrenar modelos independientes y luego se promedian para mejorar la estabbilidad y la generalizacion del modelo final

### Bagging decisiones tomar (distintas)

- Porcentaje (tamaño) de la muestra en cada uno de los elementos
- Cuantos clasificadores /muestras hacer
- Sistemas de agregacion

El bagigng se puede utilizar con cualquier tipode algortimo base.
El proceso es muy similar al detallado en los arboles:
1. Extracicon de muestras boostrap de los datos (seleccion con reemplazamiento)
2. Construccion de un modeloindividual para cada muestra boostrap (estimacion  de paramaetros y opciona,mente,seleccion de variables)
3. Prediccion de datos de test a cada una  d elas muestras de boostrap
4. Promedio/agregacion d elos resultados de las predicciones individualessobre datos de test

Elalgoritmo random forest es un tipo de bagging generalmente aplicado  sobre arboles de decision que incluye sorteo de varibales en cada nodo


OJO: el lagoritmo base es un esemmble baging no tiene que ser de la misma familia
CUIDADO: aL combninar modelos de diferentes familiasse deben considerar las escalas de las predicciones y ajustar adecuadamente la contribucion por modelo para evitar sesgos
Fortaleza del bagging: radica en la diversidad de los modelos bases. La usar distitnos algortimoso configuracione sd eparametros se puede aumenar la variabilidad ente los modelos base  lo que a menudomejora el rendimiento del esmeble
Fortaleza del bagging: radica en la diversidad de los modelos bases. La usar distitnos algortimoso configuracione sd eparametros se puede aumenar la variabilidad ente los modelos base  lo que a menudomejora el rendimiento del esmeble