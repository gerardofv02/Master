# Arbol + Random forest

- Bagging soluciona gran parte del problema de sobre ajuste de los arboles pero tiene un problema importante: a veces es complicado obtener modelos nuevos. EL remuestreo no siempre garanntiza que el modelo obtenido vaya a cambiar.
- SEgun los datos disponibles si hay un subvocnjunt de variable smuy predominantes, siempre se obtienen los mismos arboles: estas variables importantes van a ahcer las particiones de las primeras ramas, que siempre van a quedar iguales
- Para solucionarlo se define el random forest

Random forest es un algoritmo de combinacion de arboles predictores ofreciendo un unico output fruto de la combinacion de estos
ES una modifciacion del bagging que consiste en incorporar aleatoridad en las variables utilziadaspara segmentar cada nodo del arbol. Mientras que en los arboles de decision consideran todas las divisiones posibles de caracteristicas, random forest solo seleccionan un subconjunto de caractersiticas, encontrando aqui la principal diferencia.

Random forest es una tecnica de agregacion que mejorala prediccion con respecto a otros metodos mediante  la inclusion de la aleatorizacion en la construccion  de las distintas estructuras.

## Random forest

Dados los datos de tamaño N:
1. REpetir m veces i, ii, iii:
    i SEleccionar N observaciones con reemplazamiento de los datos originales
    ii Aplicar un arbol de la siguiente manera:
        En cada nodo, seleccionar p variables de las k originales y de las p elegidas, escoger la mejor variablepara la particion del nodo.
    iii Obtener predicciones apra todas las observaciones originales N
2. Promedia las m predicciones obtenidas en el apartado 1


La aleatoridad de las caracteristicas tambien conocida como feature bagging, genera uin subconjunto aleatorio de caracteristicas loq ue garantiza una baja correlacion entre los arboles de decision empleados

- Random forest tiene una reazonable capacidad explicativa: no es tan caja negra
- Diferencia con bagging: bagging coge la mejor variable entre todas
- Ranfom forest escoger la mejor variable de entre un subconjunto p
- ESto garantiza la obterncion de nuevos modelos
- p pequeño para aliviar los probelmas de bagigng

El random forrest da un paso mas en soslayar el probelma de seleccion de variabels, evitando decidirse rigidamente por un set de variables y aprovechando a la vez las ventajas del bagging
SE trata de incorporar dos fuentes de variabilidad para ganar en capacidad de generalizacion y reducir el sobreajuste conservando a la vez la facultad de ajustar vien relaciones particulares en los datos
Ranom forest evita tambien probelmas de variables predictoras muy dominantes

## Principales parametros

- EL temaño o % de las muestras n y si se va a utilizar boostrap o sin reemplazamiento
- EL numero de iteraciones m a promeidar
- EL NUMERO  de  variables p a muestrear en cada nodo. p puede ser un procentaje o un numero
- Caracteristicas de los arboels
    Son bastante imporantes:
    - Criterio de particion
    - NUmero de observaciones minimo en una rama-nodo
    - EL minimo tamaño a dividir
    - Profundidad maxima del arbol
    - Parametro de complejidad
    - Otros

(Ejemplo en python)