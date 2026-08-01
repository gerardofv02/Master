# Redes neuronales

## Instroduccion

La idea se baso de que las neuronas biologicas tienen distintas partes que actuan con disttinso proposit.
Hay partes que detectan señales, otra que las procesan y otras que responden a las señales.

Sirven para ser usadas en forma de precciones, separar variables,...
Es un algortimo más complejo.
Las redes neuronales se conectan entre sí para transmitirse señales
La información de entrada llega a una neurona. mientras la atraviesasufre distintas operaciones obetniendose un valor de salida.
Las neuronas se conectan entre sí mediante enlaces
En los enlaces el valor de salida de la neurona antrerior se multiplica por peso
Estos pesos en los enlaces pueden incrementar o inhibir el estado de activación de las neuronas adyacentes.
La conexión entre neuronas se lleva a cabo mediante funciones de combinación
A la salida de la neurona, puede existir una funcion limitadora o umbral que modifica el valor del resultado o impone un limite que no se debe sobrepasar antes de propagarse a otra neurona. Es la funcion de activacion 

### Caracterisitcas principales

- Autoorganizacion yu adaptabilidad: Descubrir estructura de datos por si mismo sin supervisacion y ajustar sus parametros continuamente cuando llegan datos nuevos o cambian las condiciones
- Procesado no lineal: aumenta la capacidad de la red para aproximar funciones, clasificar patrones y aumenta su inmunidad frente al ruido
- Procesado paralelo: Normalemente se usa un gran número de nodos de procesado con alto nivel de interconectividad

## Por qué utilizar redes neuronales

Se deben usar cuando las relaciones entre variables no sean lineales o no sean conocidas o cuando el volumne de datos es excesivo.

### Limitaciones en los modelos estadísticos

Estos modelos son muy robustos y muy estables, sin embargo habrá veces que habrá modelos mejores.

### Multiplicidad de modelos

No se puede olvidar compara modelos clasicos con modelos algoritmicos. Siempre aplciando tecnicas de validacion cruzada

### Explicar o predecir.

Hay que saber exactamente que es lo que se quiere hacer si predecir, o explicar. 
Si queremos explicar seguramente un moedlo clasico funcionara mejor siempre ya que estan los datos, sin embargo, para poder predecir los modelos algorítimocs suelen ir mejor.

### Cuando la modelización previa es inviable

En estos casos tan complejos es cuando las redes neuronales suelen funcionar muy bien.


## Arquitectura de las redes neuronales

Cuando se habla de las arquitectura, nos refereimos a las capas que tienen y como se organizan las redes dentro de las capas.

- perceptrón: Es la unidad báscia de una red neuronal. Consiste en una sola capa de neuronas conectadas directamente a la entrada y produciendo una salida. Puede utilizarse paraproblemas de clasificacion binaria pues basicamente su capacidad es separar los datos.
- Red neuronal multicapa: Compuesta por multiples capas de neuronas. utiliza la retropropagacion del error del entrenamiento. Adecuada para una variedad de tareas incluyendo clasificacion y regresion.

### Otros tipos de arquitectura

Se usan en funcion de la tarea:

- Redes neuronales recurrentes: diseñada para trabajar con datos secuenciales como series temporales o texto.
- Redes neuronales generativas: Compuestas por un generador y un  discriminador. Utilizadas para generacion de imagenes y otros datos
- Autoencoders: Formado por un codificador y un decodificador: Utiles en tareas de reducciond e dimensionalidad y reconstruccion de datos.
- Redes residuales: Introducen conexiones residuales para facilitar el entrenamiento de redes profundas. Dirigida para superar el problema de descenso gradiente en arquitecturas profundas.
- Redes neuronales Siamesas: Utilizadas para comparar similitudes entre dos entradas. Comparten parametros entre dos ramas de la red para aprender representaciones similares.
- Redes Neuronales de atencion: Introducen mecanismos de atencion para capturar relaciones entre diferentes partes de la entrada. Ampliamente utilizadas en tareas de procesamiento de lenguaje natural.

### Estructuras de conexion:

Las neuronas se conectan con las de la sigueitne capa pero no entre las de las mismas capas. 
Distintos tipos de conexiones entre neuronas:

- Conexiones hacia delante: Se conectan con las de la capa superior
- Conexiones hacia atras: LLevan valores de una capa superior a una inferior
- Conexiones laterales: Ejemplo: a la neurona de salida que da el valor mas alto se le asigna el valor total
- Conexiones con retardo: Los elementos de retardo se incorporan en las conexiones para implementar modelos dinámicos y temporales 