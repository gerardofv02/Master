# XGBOOST

La principal aportacion de este algoritmo con respecto a boosting es la regulatrizacion.
Proporciona mas eficiencia y rendimiento

Caractersiticas:
- Optimizacion de gradient boosting:  XBoost utiliza una implemnetacion optimizada del algoritmo de gradient boosting que lo ahce mas rapido y eficiente
- Caracteristicas esparsas: XGboost puede manejar conjuntos de datos con caracteristicas esparsas (conjuntos de datos en los que la mayoria de los valores de las caracteristicas son cero o muy cercanos a 0, lo que implica que la mayoria de  las caracteristicas tienen poco impacto en el resultado final del modelo)
- Regularizacion: incluye tecnicas de regularizacion para controlar el sobreajuste, como la penalizacion L1 Y L2  en los pesos de los arboles

## Filosofia:

SE basa  en la tecnica de aumento gradiente
COmbina multiples modelos debiles (normalmente arboles de decision, pero no es la unica opcion) para crear un modelo mas fuerte y preciso
IDEA PRINCIPAL: cada nuevo modelo se construye para corregir los errores cometidospor los modelos anteriores
    - comienza con un modelo inicial simple y luego construye modelos adicionales para enfocarse en los casos que fueron mal predichos anteriormente
    - Cada modelo se ajusta  a los datos de entrenamiento calculando los gradientes de una funcion de perdida especifica. Luego, el modelo intent minimizar esta funcionde perdida encontrando la mejor combinacion de caracteristicas y parametros para hacer predicciones mas precisas
    - Utiliza tecnicas de regularizacion para evitar el sobreajuste  mejorar la generalizacion del modelo. ESto incluyte terminos de penalizacion en la funcion de perdida para controlar la complejidad del modelo y  limitar la profundidad de los arboles de decision

## Regularizacion

Es una tecnica utilizada en el aprendizaje automatico para evitar el sobreajuste y mejorar la capacidad de generalizacion del modelo
COnsiste en agreagar terminos adicionales a la funcion de perdidia o error del modelo durante el proceso de entrenamiento, con el objetivo de penalizar los valores excesivamente grandes de los parametros del modelo
La regularizacion ayuda a controlar la complejidad del modelo, evitando que se ajuste demasiado a los datos de entrenamiento

## Otros metodos para controlar el sobreajuste
- Seleccionar modelos mas sencillos
- early stopping (q no haga demasiadas iteraciones)
- utilizar validacion cruzada para controlar la varianza del error
- ensamblados

La diferencia con la regularizacion es que esta intervines en la optimizacion interna del algoritmo

## REgularizacion Lasso (L1):

Funciona al agregar una penalizacion proporcianl al valor absoluto de los coeficientes del modelo. Esto significa que algunos de los coeficientespueden hacerse exactamente 0. L1 tiende a eliminar variables irrelevantes del modelo, seleccionando solo las mas importantes. Es util cuando se desea realizar una sleccion automatica de variables ante la sospecha de que solo algunas son importantes

## REgularizacion ridge (L2):

Funciona al agregar una penalizacion proporcional al cuadrado de los coeficienes del modelo. A diferencia de la regulatizacion Lasso, la regutlatizacion ridge no hace que los coeficientes sean exactamente 0. EN cambio, reduce la magnitud de todos los coeficientes, lo que ayuda a evitar que los coeficientes tengan valores extremadamente grandes y controla la complejidad del modelo. Es util cuando se desea reducir la influencia de variable smenos importantes en el modelo, sin eliminarlas por completo

CUnado hay colinealidad (variables independientes muy correladas entre ellas) la estimacion de losparametros puede ser muy erratica. Por ellos se introdudece n termino de penalizacion

en regriesion ridge se fija un parametro lamda y se pensalizacnlos valores altos de la suma de parametros al cuadrado

DE este modo, el caracter erratico de los parametros se ve corregido, obteniendo valores bajos y mas estables para los betas

En este algortimo se modifica el gradient boosting a la hora de construir cada arbol con una funcion de penalizacion basada en el numero de hojas y el socre-prediccion en cada hoja:
- arobles mas complejos = mas hojas, mas suma de cuadrados
- el algoritmo xboost predija dos parametris principales de regularizacion, lambda y alpha, que penalizan por los pesos w, socre-predicion en cada hoja. Un tercero gamma penaliza por el numero de hojas Q

## VEntajas
- REgularizacion: UNagrannovedad, aunque hay que monitorizar los parametros lambda, alpha, lambda_bias (gamma). SIrven para corregir la varianza del modelo. A mayores valores, mas conservador
- El paquete esta elabroado mas universalmente y permite utilziar diferentes funciones objetivo. ES muy rapido y esa es otra razon por su uso en grandes bases de datos
- EL algortimo implementadosigue diviiedno un nodo aunqueparezca malo, y después evalua el arbol final. EL gradiente boosting normal se para en un nodo si es malo. ESto peude significar una gran diferencia.
- EL programa XBOoost incorpora tmb, aparte de la regularizacion, el control del sobreajuste utilizando ideas de remuestreo del randomforest: tienen un parametro de % de sorteo de observaciones y otro de sorteo de variabels

## desventajas

- ES otra manera de construir arboles, no hay mucha teoria al respecto. tal vez leluge el momento en que se detecten problemas.
- Busuedas exahustivas de hiperparametros: hya que monitorizar los paraametros de regularizacion asumiendo el riesgo de que sean muy dependientes de los datos utilizados. los resultados   de tulizar regularizacion a mennudo no tienen efecto o son demasiado erraticos
. Mayor consumo de memoria, lo que es un problema cuando se trabaj con conjuntos de datos grandes o en entornos con recursos limitados
- Dificultad de interpretacion

## Principales parametros a controlar en xgboost
- EL tipod e modelo donde se va a aplicar xgboost, comunmente un modelo de arbol o lineal
- Los parametros del modelo elegido
- LOs parametros propios del xgboost

(ver ejemplo de python)