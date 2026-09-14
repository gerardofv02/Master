# Esemble

Este modelo que combina distintos algortimos de ML que busca mejorar cada una de las partes de los algoritmos. Por ejemplo, red neuronal, clasificacion, regresion,...
La idea de este modelo es que a partir de unos datos de entranmiento, realiza distintos test de ejemplo pasa por los algoritmos y se generan los distintos clasificadores. Tras estos calsificadores saca el modelo con lo mejor de cada algoritmo

Quitando el modelo general q es el stacking, se va a ver el bagging y el boosting:

## Bagging:

Imagina que estás haciendo predicciones y tienes un caja de dados. En lugar de lanzar un solo dado para obtener una prediccion, lanzas varios dados y promedias los resultados.
Ejemplo: Random forest es un tipo popular de modelo de ensemble que utiliza bagging. Crea varios arboles de decision y combina los resultados para obtener una prediccion mas precisa.

## Boosting

Supongamos que estás aprendiendo a andar en bicicleta y te caes muchas veces. Después de cada caida, un amigo te ayuda a identificar que hiciste mal y te da un pequeño impulso para que lo hagas mejor la proxima vez.
Ejemplo: AdaBoost es un algortimo de boosting. Entrena varios modelos débiles en secuencia. Cada modelo se enfoca en corregir los errores del anteror, mejorando asi la precisión general del ensemble.

## Ejemplo de esemble

Suponiendo un problema de regresion:

1. Se construye un modelo de redes que da lugar a la prediccion y1 (sobre los datos de test)
2. Se construye otro modelo con regresion logistica que da lugar a la prediccion y2
3. Se construye un modelo random forest que da lugar a la prediccion y3
4. Se estudia la performance de y1,y2,y3 y del promedio de ellas, y4. Esta variable y4 es una prediccion nueva que a veces puede funcionar mejor que cualquiera de las predicciones y1,y2,y3.
5. O bien en luegar de promediar y1,y2,y3 se construye, por ejempo, un modelo de red neuronal en el que las variables de entrada sean y1,y2,y3
ETC...


MINUTO 4:15 -> EJEMPLO PYTHON