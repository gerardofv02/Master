# Gradient boosting

Funciona añadiendo secuencialmente predictores a un conjunto y cada uno de ellos corrige los errores de su predecesor. ESte modelo se entrena con los errores residuales del predictor anterior

SE basa en ir actualizandolas predicciones en la direccion de decrecimiento dada por el negativo del gradiente, de la funcion de error L(Yi,F(Xi)) donde Yi es la etiqueta real y F(Xi) el valor predicho por el modelo.

La actualizacion de las predicciones se realiza en direccion de decrecimiento de la funcion de error

IDEA: buscar la pendiente de crecimiento

NOta: tanto el gradient boosting como el xgboost son modelos sin ninguna explicanilidad, totalmente caja negra.
Consejo: usarlos solo cuando la ganancia en eficacia sea muy significativa.
Cuanod se pierde la idea intuitiva del origen de una ineficiencia, es muy dificil resolver los probelmas.

EN cada iteracion se calcula la pendiente
EN cada arbol calculo los parametros que lo mejorarian y actualizo

1. COmenzar con un modelo inicial simple, como con un solo arbol de decision
2. Calcularlas predicciones iniciales y los errores residuales
3. Ajustar un nuevo modelo para predecir estos errores residuales. ESte nuevo modelo se agrega al modelo existente, corrigiendo los errores
4. REpetir los pasos 2 y 3 iterativamente, para mejorar el modelo en cada paso. Cada nuevo modelo se enfoca en corregirlos errores restantes del conjunto anterior.


Entonces, basicamente, en problemas de regresion, el algoritmo gradietn boosting consiste en modificar las predicciones en la direccion de decrecimiento del gradiente (en este caso el residuo).

Si el residuo sale negativo en una observacion (estamos prediciendo valores mas altos que la realidad), se actualiza la predccion en la direccion  de decredimiento, es decir, se reduce el valor predicho.

NOTA: Gradietn boosting se suele usar con arboles, pero no es mas que un tipo de ensamblado que se podría aplicar en cualquier modelo

OJO: A diferencia del bagging/random forest, gradient boosting no calcula un monton de arboles y despueslos agrega, sino que, para cada arbol construido, analiza como se ha equivocado y trata de aliviar el error de cara a la construccion del siguiente: cada arbol es una mejora del anterior. EL ultimoa rbol no es la agregacion de todos sino el ultimo de ellos

## Algoritmo gradient boosting para regresion

1. Dar como valor predictivo de la variabley para cada observacion la media de los valores de la variable y. ESte sera el punto de partida, y en cada iteracion del algoritmo la prediccion de y para cada observacion sera actrualizada de manera individual

2. REpetir los siguientes pasos para cada iteracion m:
    i calcular el residuo actual
    ii construir un arbol de regresion para predecirlos residuos, tomando ri^m como variable dependiente, yel conjunto de variables X inputo como independientes. ESto nos datra como resultado un residuo predicho que no es exactamente igual que el real pero nos sirve para actualizar las observaciones test para las que no hay residuo real al no haber y
    iii Actualizar la prediccion de ypara cada observacion (incluidas las observaciones d elos datos test) en la direccion de decrecimiento

3. EL proceso se detiene cuando se llega al numero de iteraciones final deseado
    - es conveniente señalar que los datos train convergenal verdadero valor de la y, asi que no se debe tomar en ningun caso como referencia la performance del gradient boosting sobre adtos train, sino solamente sobre datos test.

## Algoritmo gradient boosting para clasificacion
minuto 8:51