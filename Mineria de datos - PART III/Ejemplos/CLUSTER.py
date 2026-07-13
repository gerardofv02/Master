## Analisis cluster:
# sirve para resumir y simplificar la gran cantidad de datos
# machine learning: a diferencia de algortimos supervisados el clusterign opera sin etiquetas predefinidas
#tecnica estadistica: busca organizar datos en grupos coherentes

# por ello, el analisis cluster es una tecnica estadistica para clasificar elementos basandose en su homogeiedad. busca homogeniedad entre ellos y 
# heteregeniedad entre elementos de distintos grupos

# posicion inicial: seleccion de una medida de distancia. usa algoritmos segun las medidas.

# algoritmos: 
#   - Jerárquico: forma grupos secuencialmente ya sean fusionados (aglomerativo) o dividiendo (divisivo). no se conoce el numero de grupos de antemano
#   - No herárquico: Se predefine un numero de grupos. Las observaciones se asignan a esos grupos basandose en esta cantidad de grupos distintos

# IMportancia de la seleccion: El exito depende  de la eleccion adecuada de la medida de distancia y del algortimo
# Interpretacion de grupos: La formacion de grupos revela patrones, tendencia y relaciones en los datos que pueden no ser evidentes sin el agrupamiento


# requisitos para realizar analisis de cluster:
# - Escala de variables: Las variables de entrada stienen que estar en la misma escala o ser estandarizadas
# - Ausencia de valores atipicos: Es importante encontrar y manejar estos valores
# - Datos perdidos: Puede ser necesario aplicar técnicas de imputacion de datos
# - Miniminizar la corrlacion entre variables: Es importante que las variables no estén fuertemente correlacionadas entre si

## Pasos para realizar el análisis de clustering:
# - Evaluacion del parecido entre observaciones:
#   - Determinar la proximidad o similitud entre observaciones utilizando medidas de distancia
# - Evaluacion del parecido entre variables
#   - Evaluar la similitud o correlacion entre variables, is el enfoque es entre las caracteristicas en lugar de las observaciones
#- Seleccion de tipos de agrupacion:
#  - Decidir si escoger jerárquico o no jerárquicos.
# - Seleccion de algortimo de agrupacion: Por ejemplo k-menas, agrupamiento jerarquico,...
#- Determinacion del numero optimo de clusters: Este es solo para no jerarquicos. Definir un numero correcto de grupos
#- Interpretaciony validacion de clusters formados:
#  - Analizar e interpretar los grupos resultantes para validar su significado y relevancia.

## ahora vamos a ver las medias distancias entre observaciones:

# las medidas de distancias mas utilizadas son:

# - Distancia euclídia: es la mas utilizada y es la raiz cuadracda de las diferencias de cada vairable al cuadrado

# - Distancia minkowski: En esta se define como la raiz p- esima de la suma de las diferencias de las observaciones de cada valor

# - Distancia de correlacion de pearson: esta la tenemos que usar cuando tenemos que hacer un analisis cluster sobre las variables. Esta medida evalua la similitud entre dos varables
#       basandose en la correlacion lineal de pearson. 
#       - Un valor de -1 indica una relacion lineal perfecta negativa
#       - Un valor de 0 sugiere que no hay relacion loineal
#       - Un valor de 1 indica una relacion lineal perfecta positiva

# - Distancia de correlacion de spearman: esta la tenemos que usar cuando tenemos que hacer un analisis cluster sobre las variables. Utiliza ciando los datos son ordinales o 
#       no cumplen con los supuestos de la correlacion de pearson. por ejemplo, cuando los datos son respuestas a una encuesta de satisfaccion.
#       - Un valor de -1 indica una relacion monotona perfecta negativa
#       - Un valor de 0 sugiere que no hay relacion monotona
#       - Un valor de 1 indica una relacion monotona perfecta positiva

#una relacion monotona sign ifica que las variables tienden a cambiar juntas

# - Distancia de correlacion de kendall: evalua la concordancia nentrre dos conjuntos de datos basandose en la concordancia o discordancia nde los pares de observaciones.
#       - Un valor de -1 indica una falta de concordancia entre los conjuntos de datos
#       - Un valor de 0 sugiere que no hay concordancia ni discordancia sistematica
#       - Un valor de 1 indica que hay una concordancia perfecta

# Vamos a ver como determinar el numero optimo de grupos (k) para algoritmos no jerarquicos.
# # esta relacionada con la bondad de ajuste. se va a utilizar el metodo del codo: se va a trazar el wcss(suma de cuadrados dentro de cada gfrupo) cion respecto al numero k del cluster
# buscando que un grupo mas no produzca diferencias significativas

# otro coeficiente es el coeficiente de la silueeta que nos permite ver como de bneunos hemos sido identiuficando los componentes
# para calculoarlo, primerp por un aldo tenemos que calcular la distancia media a sub i que mida cuan bien se agrupa una observacion i a su propio cluster
# tmb tenemos que calcular la distancia media b sub i al cluster mas cercano. mide cuan bien se separa i de los clusters mas cercanos
# por ultimo tenemos que caluclaur el coeficiente de la silueta que es como la diferencia de b-a entre la diferencia de estas.

#interpretacion:
#       - Un valor de -1 indica posiblemente una asignaciond e cluster erroneo
#       - Un valor de 0 sugiere que esta cerca de la frontera entre dos clusters
#       - Un valor de 1 indica que está bien agruppada y lejos de clusters vecinos

# esto nios ayuda a seleccionar el número de cluisters que ofrece mejor equilibrio

## ahora vamos a ver cluster de caracterizacion:

# sirve para comprender cada cluster a través de  un analisis descriptivo de las variables
# identificacion de miembros: determinar los elemnetos de cada cluster; listados o tablas de pertenencia
# estadisticos descriptivos: medidas como la media mediana,m varianza  desviacion estandar para ver como se comportan los lcusteres
# compoarancion entre clusteres: usar estadisticos para diferenciar clusteres en terminos de variables nalizadas.
# perfilado de cluisters: crear perfiles de basados en estadisticos incluyendo graficas o tablas resumen
# analisis de variables significaticas: identificar variables clave enb la formacion y descripcion de los clusteres
# visaulizacion de los datos: utilizar graficos de barras histogramas o boxplots para ilustrar carasterisitcas de los clusteres.

## fatla solo el ejemplo de pytthon 