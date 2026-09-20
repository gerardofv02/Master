# Arbol + bagging

Dados los datos de tamaño N
1. REpetir m veces i y ii:
    i SEleccionar N observaciones con reemplazamiento de los datos originales
    ii aplicar un arbol y obtener predicciones para todas las observacionesoriginales N

2. Aregar las m predicciones obteneridas en el apartado 1

- Dependiendo del tamaño del conjunto de datos, habra que ensamblar mas o menos arboles,m
- AUnque el tamaño de todos los conjuntos  de datos que seleccionamos es el numero de filas del conjunto de datos, N, no tienen porque ser los mismos datos dado que podemos hacerlo con un muestreo con remplazamiento donde se pueden repetir observaciones
- Si algo se repeti, gana importancia. La gran sensibilidad  de los arboles provoca que, ante el vambio de pesos de los disitntos individuos, varie el resutlado
- EL resultado del bagging por agregacion de las m predicciones: en general promedio del valor o de la probabilidad
- FIlosoficamente, este proceso de ensamblado se podría hacer para cualquier tipo de modelos, pero se ha demostrado que solo es util con arboles
- cuidado con la complejidad computacional. Para ahorrar tiempo, es importante tener ajustado el numero minimo de observaciones en una hoja en arboles, para ahorrarse esas pruebas en bagging


- Con cada submuestra se genera un modelo con el que se predicen los datos. L aprediccion final será la media de las m diferentes predicciones
- Al utilizarse diferentes submuestras, se reduce la dependencia de la estructura de los datos completos para construir el modelo y como consecuenciase reduce la varianza del modelo

- Las instancias que no se incluyen en la muestra de entrenamiento de un arbol especifico se considera como instancias out-of-bag apra este arbol en particular. Estas instancias OOB proporcionan una evaluacion adicional del rendimiento del arbol, ya que no se utilizaron durante su entrenamiento. Por lo tanto, se pueden utilizar para estimar la precisión fuera de la miuestra del arbol sin la necesiad de un conjunto de prueba adicional

- En el apartado i admite todo tipo de variaciones: tomar n<N (para ganar velocidad computacional) con o sin reemplazamiento. CONSEJO: probar con un modelo grande, una vez visto lo que tarda, calcular que  es factible mantener el tamaño en este tipom d emetdoso.

- En cuanto a ii, la complejidad del arbol a utilizar es un debate . Inicialmente se propuso arboles debiles (pocas hojas) y muchas iteraciones m. Pero en algunas versiones se utilizan arboles desarrollados hasat el final sin prefijar el numero de hojas o profundidad. Tambien se puede hacer seleccion devariables.
- Si se trata de un problema de clasificacion, dosestrategias pueden ser usadas:
    - Promediarlas probabilidades estimadas y obtener una clasificacion a partirde un punto de corte
    - Clasificar en cada iteracion y asignar a cada observacion la clasificacion mayoritaria entre todas las iteraciones


EN general baggin funciona bien cuando:
1. Cuando los modelos no están claros
2. Cuando existen relaciones no lineales (regresion) o separaciones no lineales (clasificacion)
3. CUando existen iteracciones ocultas, muchas variables categoricas,...
OJO: no tiene mucho sentido aplicar bagging cuando hay POCAS variabels

## Principales parametros para controlar el bagging

### Controlar la aleatoridad -> la reporduccion es fundamental

Cuando se plantean modelos en ml se usan a menudo tecnicas de remuestreopara evaluar bien los modelos. EStas técnicas conllevan sorteos, ordenaciones aleatorias,... Para ello se usan semillas de aleatorizacion

SI el proceso depende de una sola semilla que se suele piner al principio del codifo, no hay problema con la reproducibilidad del modelo

También hay que recordarque la semilla de aletorizacion no es un parametro del modelo, la usamos como control y podemos jugar con ella, variandola como hacemos en la validacion cruzada repetida, para observar la sensibilidad del modelo y sus errores ante un esquema de sleeccion de observacione ligeramente diferentes.

### Optimizacion de resutlados

Para la optimizacion de los resultados, es necesario tunearlos parametros del bagging. LOs parametros a tener en cuenta son:
- EL tamaño de la muestra y si se va a usar bootstrap (con reemplazo) o sin reemplazamiento. SI el numero de observaciones es pequeño, mejor utilizar con reemplazamiento. SI es grande, es indiferente pues el resultado con o sin reemplazamiento es muy similar.
- EL numero de iteraciones m a promediar 
- E numero de variabels a utilzar en cada arbol

### Caracteristicas de los arboles

SOn bastante influyentes:
- Criterio de particion (entriopia, gini, varianza,...)
- El numero de observaciones minimo en una rama-nodo
- EL minimo tamaño apra dividir
- Profundidad maxima del arbol
-Parametro de complejidad
- Otros(numero maximo de divisiones por nodo,...)

(ejemplo ne python)