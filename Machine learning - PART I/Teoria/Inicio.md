# MACHINE LEARNING
El machine learning es el aprendizaje automatico en base a datos existentes.
Resume patrones y hace predicciones. 
Tipos de ML:
- Supervisado: Aprende con ejemplos etiquetados
- No supervisazo: Descubre patrones ocultos
- Refuerzo: Prueba y error con recompensas
## Introducción
El machine learning se centra en el desarrollo de algoritmos y modelos estadísticos que permiten a las máquinas aprender y mejorar su rendimiento en una tarea específica sin ser programadas explícitamente para ello. Se basa en patrones e inferencias y no en programación directa.
Basicamnete se basa en patrones en base de ejemplos.

La maquina 'aprende' en base de las repeticiones. Con lo q a base de enseñarle a la maquina muchas veces, entiende las respuestas a ese patron y cuando le llegue una similar, podrá devolver una respuesta.

## Tipos de ML

### Aprendizaje supervisado

Decimos que está dentro del aprendizaje supervisado cuando conocemos del valor real de la respuesta. Estas etiquetas nos van a permitir comprobar si la respuesta que ha dado es correcta según loq ue pone en la etiqueta o no

### Apredizaje no supervisado

Son algortimos que intentan descubrir patrones pero sin tener el conocimiento previo como se tiene en el supervisado.
El ejemplo mas comun de no supervisados es el analisis cluster.

### Aprendizaje semisupervisado y de refuerzo
Es una mezcla de los dos anteriores grupos

## Técnicas de clasificación/regresión

- Reglas de asociación: detectan relaciones entre variables.
- Algoritmos genéricos: Procesos de búsqueda heurística que imitan la evolución biológica como estrategia para resolver problemas de optimización de búsqueda global, explorando todo el espacio de soluciones del problema permitiendo salir de posibles óptimos locales e ir en búsqueda de óptimos globales
- Árboles de decisión: son algortimos con una estructura de árbol similar a un diagrama de flujo que utilizan un método de bifurcación para ilustrar cada resultado posible de una decisión.
- Redes neuronales y deep learning: Compreneden muchos elementos de procesamiento interconectados que trabajan al unísono para resolver problemas específicos. Aprenden con ejemplo y experiencia.
- Máquinas de vector de soporte: Métodos utilizados para clasificación y regresión, usando un conjunto de ejemplos de entrenamiento clasificado en dos categorías para construir un modelo quqe prediga si un nuevo ejemplo eprtenecea una u otra de dichas categorías.
- Algoritmos de agrupamiento: Permite la clasificación de observación en subgrupos, de modo que las observaciones en cada grupo se asemejen entre sí según ciertos criterios
- Reyes bayesianas: modelos probalísticos que representan una serie de vairables de azar y sus independencias condicionales a través de un grafo acíclico dirigido. Se usan para modelar, por ejemplo, las relaciones probalísticas entre enfermedades y síntomas.

## Fases

Fases de cualquier problema de ML

- Definición del objetivo : Planteamiento de un problema que requiera una solución a medio-largo plazo
- Recopilación y preparación de datos: Procesamiento y limpieza de datos
- Elcción del modelo: Clasificación binaria, multiclase,regresion,...
- Entrenamiento del modelo: Suministrar al algoritmo la información que necesita para el aprendizaje inicial
- Evaluación del modelo: Diferenciar entre los datos de prueba y los de entrenamiento
- Análisis de errores: Permite moldear y cambiar los aspectos no relevantes para mejorar el rendimiento.

## Elementos básicos de ML

- Dataset: Histórico de datos usado para entrenar el sistema seleccionados para detectar patrones
- Instancia: Cada uno de los datos disponibles para el análisis es una instancia (las filas)
- Caracterísitca: Atributos que definen cada una de las instancias (columnas)
- Objetivo: Atributo que se quiere predecir
- Confianza: Probabilidad de acierto que calcula el sistema para cada predicción hecha
- Aprendizajeo entrenamiento: Proceso en el que se detectan patrones de un conjunto de datos.

IMPORTANTE: división de datos
Esto sirve para que tengamos un conjinto de datos para entrenar el modelo y luego otros para verificar el correcto funcionamiento de modelos.
Luego podemos divirlo en tres partes: entrenamiento, validacion y test (80,10,10)
O en dos grupos que e slo mas comun: entrenamiento y test (80,20)