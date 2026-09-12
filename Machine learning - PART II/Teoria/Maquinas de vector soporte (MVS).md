# MVS

Es un algoritmo estadistico diseñado para problemas de clasificacion binaria, y como todo algoritmo responde a estas ideas de tratar conjunto de datos y encontrar el mejor modela que pueda clasificarlo.

## Aprendizaje estadistico

El aprendizaje estadisticocaracteriza las propiedades de las matematicas de aprendizaje

El MVS trata de plantear el problema de separación linealde clases con métodos algebraicos. Se basa en 3 ideas importantes:

## 1. Maximal margin
Se trata de no solamente separar las clases por un hiperplano, sino de incluir en la decisión de la construcción del separador,el concepto de separador con máximo margen. Esto a menudo mejora tanto el sesgo comola varianza de los resultados.
Basicamnete se baa en dibujar lineas rectas para separar las clases creadas

Todos los hiperplanos spearan las dos clases.

Ejemplo: Hiperplanos en ejemplos

## 2. Soft margin

La separacion perfecta no suele existir y es necesario permitir observaciones mal clasificadas por los separadores para no incurrir sobreajustes.

Es una modificacion del SVM básico que permite cierto grado de error o superposición. En lugar de insistir en una diferenciacion perfecta, permite que algunos elementos caigan dentro del margen o incluso en el lado incorrecto del hiperplano

### Aplicación

Consideracion de un parametro de regularización que modelice la cantidad de error permitido.
- Valor pequeño de C permite más errores (soft margin)
- Valor alto de C penalizará más fuertemente los errores (hard margin)

## 3. El kernel

La separación entre clases en muchos problemas no es lineal. UNa idea para aplicar a pesar de todo un algoritmo de separación lineal es trabajar en un espacio de dimensión superior donde sí tenga sentido la separación lineal. 

Basicamente se trata de crear como una nueva dimensión para que un hiperplano pueda separar las clases correctamente ya que igual en la dimensión anterior seria imposible

### IMportante: diferencias entre mapping y kernel

- Kernel:
    - Función matemática que cuantifica la similitud entre dos vectores de datos en el espacio original de caracteristicas
    - Permite realizar operaciones en el espacio de características de mayor dimensión sin tener que calcular explícitamente las coordenadas de los puntos en ese espacio
    - PErmiten manejar eficientemente problemas no lineales separables al mapear iimplícitamente los datos a un espacio de características de mayor dimension.
    - Ejemplo: kernel lineal, kernel polinómico y kernel radial o gaussino

- Mapping:
    - Transformación de datos desde el espacio de características original a un espacio de características de mayor dimensión
    - IMplica realizar la trasnformación real de los datos a un espacio de características de mayor dimension
    - EL mapeo se utitliza para abordar problemas no linealmente separables al proyectar los datos en un espacio donde sea más probable que sean linealmente separables.

Por lo tanto: EL kernel mide similitudes en el espacio original mientras que el mapeo implica transformación real de datos a un espacio de caracteristicas de mayor dimension.Ambos conceptos son cruciales para el funcionamiento de las SVM en problemas más complejos.

## BUsqueda paramétrica

ESto sirve para buscar parametricamente cual sería el mejor modelo de usar según los parametros.

Parametros importantes:
- Parametro C: aumentar C implica menos sesgo y mayor sobreajuste. EL rango de valores que puede tomar C depende mucho de los datos
- Función de kernel (no siempre es necesaria )y sus parametros
- RBF: Aumentar el parámetro 'y' en la funcion RBF implica menor sesgo y mayor sobreajuste
- Polonomial: AUmentar el grado del polinomio implica menor sesgo y mayor sobreajuste

OJO: hay interdependencia entre ambos parámetros

## VEntajas y desventajas de SVM

- Ventajas de SVM:
    - Muy flexible, sobre todo por el truco kernel. Hya versión para regresión y para clasificacion multinomial
    - Puede competir en datos separables linealmente con la regresión logística
    - Buena performance en clasificación de imágenes

- DEsventajas del SVM:
    - El proceso de optimización puede ser muy lento
    - Dificultad en la selcción de la función kernel y sus parámetros asociados
    - Los valores faltantes, las categorías poco representadas o las variables irrelevantes son un problema importante que SVM no aborda bien
