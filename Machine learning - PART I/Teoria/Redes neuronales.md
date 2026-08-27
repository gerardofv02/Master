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

## Tipos de redes

Hay tipos de redes segun algoritmos arquitectura y sobre todo para que tipo de tarea se utiliza

- Redes neuronales supervisadas: Es decir, estas redes neuronales usan datos etiquetados. Durante el entrenamiento la red ajusta sus parametros para ajustar el valor predicho a esa etiqueta. Esto se realiza mediante un proceso de retropropagación. Una vez se termina el entrenamiento este tipo usa el valor como el peso para poder predecir valores no vistos. Existen para distintos tipos unas mejores que otras (ver imagen).
- Redes neuronales no supervisadas: Se usan para problemas de clustering. El objetivo es encontrar patrones y similutedes entre datos. Es para aplicar un algortimo de clustering. Dentro de este tipo encontramos los distintos tipos de redes no supervisadas a usar segun la tarea. (Ver imagen)

## Uso general

### Preparacion de datos

Las variables deben seguit una distribucion normal o uniforme

- Las variables categóricas hay que convertirlas a dummies antes de introducirlas a la red.
- Para cada variable categórica con k categorias. (k-1)variables dummies. El valor de la 'ultima' variable dummy se puede obtener a partir de las (k-1)restantes
- Los datos deben estar depurados y sin datos missing: las redes no son una buena herramienta para la depuracion de datos.

### Seleccion de variables

La red una vez recibe la capa de entrada con unas reglas establecidas las va a usar sean o no utiles. Por lo tnato es muy importante hacer una eleccion de variables.

Para ello se tiene que seguir lo sigueinte:

- Eficiencia computacional: Reducir la cantidad de variables que puedan hacer que el proceso de entrenamiento sea mas rapido y menos intensivo. Menos variables implican menos calculos.
- Evitar dimensionalidad: Al incluir muchas variables el espacio de busqueda se vuelve mas grande por lo tanto la red neuronal de entrenamiento le costara mucho mas descubrir patrones
- Mejora la generalizacion: Un modelo entrenado con un conjunto de caracteristicas mas pequeño puede generalizar mejor a datos no vistos
- Interpretabilidad del modelo: Una red neuronal,ás simple con un conjunto de variables mas pequeño es mas facil de interpretar
- Reduccion de riesgo de overfitting: Un conjunto con muchas variables puede llevar  aun modelo que memoriza el conjunto de entrenamiento en lugar de aprender patrones. 
- Manejo de variables redundanteso colineales: La seleccion de varibales ayuda a identificar y eliminar caracterisitcas redundantes o altamente correlacionadas. El uso de variables redundantes puede afectar negativamente al rendimiento y dificultar la interpretacion del modelo.
- Reduccion del ruido: Para mejorar la calidad de los datos de entrada, facilitando que el modelo capture patrones significativos

Por lo tanto, en la selecicon de variables es muy importante tener en cuenta que tenga una capa de entrada que sea informativa, util y lo mas pequela posible.

Lo unico que estas redes haran las redes para quitar variables que no sean utiles sería jugar con los pesos de dichas variables, pero con ello estariamos cargandonos el proceso de optimizacion e irian mas lentas

### Como seleccionar las variables: 

- Importancia de las caracteristicas: Relalizar un analisis de sensibilidad, seleccion preliminar con modelos que miden la importancia inherentemente (arboles, gradient,...), RFE(eliminacion recursiva de caracterisitcas),...
- Seleccion manual: hecha por expertos en el dominio que puedan seleccionar manuealmente un subconjunto de caractersiticas (campos) basandose en su conocimiento y comprension del problema
- Técnicas automáticas: eliminacion recursiva de variables o técnicas basadas en información mutua.
- Regularización: L1 (LASSO) o L2 (Ridge), pueden ayudar a reducir la importancia de ciertas características al penalizar sus coeficientes
- Analisis de correlacion: si dos variables están altamente correlacionadas, una de ellas podría ser redundante y eliminarse
- rEDUCCION DE DIMENSIONALIDAD: Como analisis de componentes principales (PCA) o t-SNE

### Problematicas de sleccion de vairables:

- Filters: Ordenan las variables por importancia: Esto se tieene que calcular a posteriori una vez la red esta entrenada. Y se utilizara el método de olden garson. Esto se puede calcular haciendo uso de r por ejemplo
- Wrappers: Metodos de busqueda secuenciales: 
- Embedded: Aplican algoritmos de regularizacion que eliminan variables que no aportan

Es importante que NO se deben interpretar los pesos. Pero si se pueden utilizar herramientas para jugar con ellas:
- Vizualizaccion de pesos
- Mapas de activacion 
- Analisis de importancia de caractersiticas
- Capas de atencion.
- Estudion de conexiones ponderadas.

### Conclusion:

Siempre se debe aplicar el proceso de seleccion de variables antes de la definicion de la arquitectura, fijo la capa de entrada, intentando trabajar con un modelo lo mas sencillo posible. Estos modelos son robustos (por lo tanto me van a garantizar que lo que me dan es correcto) aunque tenga menos capacidad de prediccion
Por otro lado, esto depende de la necesidad del problema, ya que si tiene mucho mantenimiento, se pueden hacer uso de mas variables.

### Eleccion de los pesos inciales

El metodo va a asignar pesos aleatorios a cada una de las variables.  Por ello:
- Evitar simetría indeseada
- Facilita la convergencia
- Estabilidad numerica

### Evaluacion de un modelo.
Para evaluar un modelo de red neuronal nuestra metrica final sera la matriz de confusion

### Fases del entrenamiento:
1. Eleccion de los pesos iniciales
2. Eleccion de la arquitectura de la red
3. Evaluacion del rendimiento
4. Interpretacion de los pesos obtenidos (calculo del descenso del gradiente para ver como hay que modificar los pesos)

## Ideas sobre arquitecturas