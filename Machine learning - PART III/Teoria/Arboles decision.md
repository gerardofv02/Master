# Arboles decision

## INtroduccion

Un arbol de decsion son metodos que proporcionan modelos que satisfacen objetivos tanto predictivos como explicativos
EL objetivo es predecir una variable respuesta en funcion de un conjunto de variables independientes con un metdo que me permita una explicabilidad del proceso que estoy haciendo

Los pasos son generales independeintemente del tipo de arbol que usemos. 
UN arbol de clasificacion/regresion es el resutlado de preguntar una secuencia ordenada de cuestiones. Las cuestiones que se plantean en cada etapa dependen de las respuestas a las cuestiones previas de la secuencia

EStas uestiones se ordenan de más importante a menos

El punto unico de inicio de arbol se llama nodo raiz y contiene el conjunto total de datos a clasificar en la parte superior del arbol

UN nodo es un subconjunto del conjunto de variables y peude ser terminal o no. Un nodo no terminal o padre es un nodo que se dividi en k nodosdescencdientes
Un nodo terminal es un nodo q no se vuelve a subdividir

Un tipo muy generalizado de arbol son arboels de decision binarios en los que cada nodo padre se divide ne dos nodos descendientes

Una division binaria queda determinada mediante una condicion booleana sobre los valores de una unica variable siendo satisfecha la condicon o no satisfecha por el valor observado de dicha variabel

Todas las observacione sque alcanzan un nodo padre acabaran en un lugar o otro.

EL unico nodo que no sigue es el terminal y se tendra que asignar un valor. SI estamos en un modelo de clasificacion, debemos de indicar a que clase pertenece mientras que si estamos en uin modelo de regresion tenemos que hacer una estimacion numerica

HAy que considerar cada posible division sobre todas las variables presentes en dicho nodo, enumerar después todas las posibles divisiones evaluar cada una y decidir cual es la mejor siguiendo algun criterio

(ver ejemplos en diapositivas)

## Tipos

### Arboles de clasificacion

EStos la variable respuesta Y es cualitativa

### Arboles de regresion

EStos la variable respuesta Y es cuantitativa



## Cuando se debe usar este modelo (sobre que conjunto de datos)

Basicamente, es casi mas importante qu el aprediccioon, explicar porque se esta dando esta explicacion.

Debido a su estructura y pkanteamiento este algoritmo es especialmente indicado cuando la explicabildiad de un modelo es funcamental

Algun ejemplo:
- Concesion de créditospara determinar y porque s un determinado solicitante es rechazado o no
- EStudios de marketing para conocer la satisfaccion de los clientes
- DIagnostico medico

Existen casos en los que estos modelos pueden no ser adecuados a pesar de su capacidad explicativa.
- CUando se tiene una gran cantidad de variables nominales con muchos niveles
- Gran cantidad de variables numericas  

El arbol presenta muchas ramas, resultando un arbol complejo y dificil de interpretar

EN resumen, si Y es la variable dependiente y X1....xp son las variables fijas independientoes o predictoras, se trata de resolver el problema estadistico de establecer una relacion enrre Y y x1...xy de forma que sea posible predecir el valor de Y en base a los valores de C1..XP

Matematicamente se quiere estudiar la probabilidad condicional de la variable aleatoria o una funcion de probabilidad tal como la esperanza condicional dependiendo de si se trata de un arbol de clasificacion o de regresion, respectivamente.

## Criterios  para la division de nodos

EL objetivo es encontrar en los datos el punto de corte que divida estos en dos grupos lo mas puros posibles. ESto consiste en asegurar que un nodopadre produzca a sus nodos hijos en cuya composición de clases sea lo mas pura posible. EL objetivo es que cada nodopadre produzca un nodo hijo que iunicamente contiene un clase

ESte grado de pureza se suele medir con alguno de los siguientescriterios:
- Entropía
- Indice de gini
- Minima probabilidad

LLegara un momento que demos por saturado el arbol y por lo tanto los nodos descendientes no peudan seguir y hacer una particion de ellos. EStos son los nodos terminales.
EL numero de divisiones permitidas para un nodo disminuye cuando aumentan los nieveles del arbol. Cualuqier nodo que no pieda o no sea dividido es uin nodo terminal

## Metodos de creacion de arbol de dcision

ESte proceso es laborioso por la complicada casuistica y combinatoria que se va generarndo cada vez  que es necesario dividir un nodo

Hisotricamente la construccion de arboles ha ido mejorando, creandose nuevos algoritmos:
- CRT o CART
- CHAID
- ID3
- C4.5
-etc...

EStos algortimos aportan trucos y opciones para solucionar problemas de arboles

Las dos técnicas mas usadas y constratadas son CART Y CHAID. En cualquier caso hay muy poca diferencia entre unas y otras. DEpendiendo del paquete se usa una u otra. 

## CART
ESta metodoliga consiste en construir un arbol grande e ir podando  hasta dar con el tamaño correcto. COnsta de tres pasos:
1. Construccion del arbol saturado
2. ELccion del tamaño correcto
3. Clasificacion de nuevos datos a partir del arbol construido

## CHAID

Explora los datos de forma rapida y eficaz. PErmite la deteccion automatica de interacciones mediante ji-cuadrado

- CHAID examina tablas cruzadas entre los campos de entrada y los resultados para, a copntinuacion, comprobar la significacion mediante una comprobacion de independencia de chi-cuadrado.
- Si varias de estas relaciones son estadisticamente importantes, CHAID seleccionara el campo de netrada con el valor de significacion menor
- SI una entrada cuenta con mas de dos categorias, se comprobaran esas categorias y se contraen las que no presenten diferencias en los resultados, uniendose el par de categorias con menor diferencia, y asi sucesivamente.
- ESte proceso se detiene cuando todas las categorias restante difieren entre si en el nivel de comprobacion especificado. EN el caso de  campos de entrada nominales, pueden fundirse todas las cateogrias. EN los conjuntos ordinales, unicamnete podran fundirse las categorias continuas.


## ID2, C4.5

- El algoritmo ID3 esta superado y solo queda como un predecesor el C4.5    
- El algoritmo C4.5 tiene la misma filosofia que el algoritmo CART, crear un arbol completo y luego estudiar la poda del mismo
- Los criterios de seleccion de variables, determinacion del corte y tratamiento de datos perdidos es diferente al de CART
- En general es un metodo que se puede utilizar en los mismos casos que CART


## Criterios

Para una correcta construccion de arboles, es importante tener en cuenta diversos criterios, entre los que cabe destacar:
- CRiterios para elegir qué variable independiente  y nodo va a ser la base para la siguiente división
- CRiterios para elegir grupos de corte para variables independientes nominales conmmas de una categoriao para variables numericas.
- Criterios para elegir el/los puntos de corte optimo dentro de cada variableindependiente o nodo
- NUmero de observaciones minimas para construir un ndoo
- Limites de numeros de nodos, divisiones,...
- Criterios de parada-fin algoritmo
- Criterio de tratamiento de valores perdidos
- CRiterios de poda de arbol
- SI se van a utilizar datos de validacion para controlar el proceso de construccion o no

## Creitrios para un punto de corte optimo

Dependiendo de la naturaleza de variables dependeinte / independiente hay varios criterios para elegir el ounto de corte
SI nuestra variable respuesta es categorica, podemos usar:
- Indice de gini    
- CHi cuadrado
- Entripia

SIn embargo si mi variable es numeroica usaremos:
- F-Snedecor
- MAxima varianza

### Chi-cuadrado

SE analiza la independencia de una tabla de frecuencias cruzando la VD CON LA vi, seleccionando el caso que presente un mayor nivel de significacion

Valores altos indican que la tabla de frecuencias es poco independiente, poco aleaotria: Corte plaanteado crea grupso muy claros y poco aleatorios.

(ejemplo en diapositivas)


- LO ideal es escoger el corte que maximice el valor de chi cuadrado
- Porceso: Para todas las variables y todos los puntos de corte, calcular chi cuadrado para obtener el maximo
- Problema: Dependiendo de las variables que haya y de la complejidad de los datos, este proceso puede tener demasiado coste computacional
- Importante: EL test de CHAID usando el criterio de chi cuadrado se basa en la hipotesiscon normalidad. La mayoria de  los datos reales NO estan distribuidos normalmente, lo ue dificulta obtener resultado coherentes con este método.

Una alternativa peude ser   el índice de gini-

### Indice de Gini

El indice de gini es una medida de desigualdad que refleja el grado de homogeniedad o heterogeniedad de valores que presenta un conjunto de datos. Puede reflejar la impureza de los valroes.

LOs valores minimos indican perfecta igualdad: Todos los valores son el mismo. Por su parte, valores altos indican ue todos los datos son distintos entre si. POr lo tanto nos quedamos con estos valores alto para decidir cual va a ser el siguietne corte que vamos a realizar 

### Entropía

Consiste en asegurar que un nodo padre produzca nodos hijos en cuya composicion de clases sea lo mas pura posible. El objetivo es que cada nodo padre produzca un nodo hijo que unicamente contiene una clase

La medicion de la entropia refleja la impureza de  la distribucion de clases o como de mezcladas esten

UN valor de 0indica el nivel maximo de homogeniedad
Un valor de 1 indica el nivel maximo de heterogeniedad

### F-Snedecor

 ES el estadistico de constraste utulizado en ANOVA

Se asume que, si los elementos  de los distintos grupos pertenecen a la misma poblacion, la varianza intragrupal debe de ser la misma que la varianza intergrupal. Asi, se compara como de grande es la varianza entre grupos en comparacion con la varianza intragrupal.

Estimador de la varianza intragrupal se construye como un promedio de  las distintas mediaselevadas al cuadrado. DOnde se tienen J grupos y scuadrado J es la varianza muestral de un grupo J, se hace la media ponderada de las J varianzas muestrales.

### Varianza

SE calcula la variabilidad de la variable dependiente en cada grupo y se suma /(literlamente la varianza estadistica seria diviendo por n pero no se ahce asi) la diferencia entre los datos con la media y se busca maximizar.

SE elige la division que construye los gruposmas homogenos internamente y diferentes entre si.

### Caso:VD: continua; VI: Continua

Los nodos continuos han de ser tratados como categoricos para realizar la division por lo tanto el punto de corte se buscara entre un conjunto de puntos de corte candidatos seleccionados a través de  metodos iterativos y se calcularan las mismas medidas PROB.F o varianza vistas anteriormente, donde la variable independeitne  continua, dividida en dos grupso, hace el papel de cagtegorica

### Caso VD: CATEGORICA; VI CONTINUA

SE categoriza la variable continua por metodos iteraitovos y se utilizan los criterios chi cuadrado, gini o etropia

## Criterios para seleccionar la VI que va a crear la siguiente division

- Importante: NO todas las variables de la base de datos son utiles para hcer modelos de ML
- Ojo: DEpendiendo del modelo se usan unas u otras variables
- SE deben eliminar las variables de la base de datos que no se puedan tener en el momento de realizar las predicciones
- SE pueden eliminar las varibales de la base de datos que no tengan relacion con la variable independiente
- NO es necesario eliminar las variables de la base de datos que tengan milticolinealidad entre ellas

## CRiterios para el manejo de calores perdidos

Posibilidaddes:
- Asignar las observaciones con missing a la rama mas grande
- Asignarlos missing a la rama con menor error calculado en las observaciones sin missings
- IMputar los valores perdidos

IMportante: El tratamiento de missings puede enturbiar la informacion disponible y desequilibrada. ES imprescindible conocer bienla base de datospara dar un tratamiento correcto. A veces, es conveniente usar los valores missing como un valor mas de una variable categorica. 

(ver ejemplo diapo)

## Arbol final, subarboles y prining

El algoritmo finaliza cuando se cumple alguno de los criterios de parada:
- NO hay suficientes observaciones en las hojas finales para considerar su division
- La profundidad maxima (parametro prefijada) ha sido alcanzada
- EN ningun nodo se puede mejorar el cirterio de division, por ejemplo el indice de gini (o f para variables dependientes continuas)

EL modelo final de arbol puede estar sobreajustado si los datos son complejos. TRas obtener el arbol final, puede actuarse como en los metodos cluster: 'escogerla solucion= subarbolque parezca mas estable'- Preuning significa podar y es el actode quedarse con un subarbol

## Poda o prunning

UN arbol de decision puede crecer indefinidamente en particiones mas y mas pequeñas hasta encontrar la solucion perfecta.
Las soluciones serían tan específicas que resultaria en un modelo con overfitting
EL proceso de poda asegura la generalizacion de los resultados a traves de la reduccion del tamaño del arbol

- Pre-poda: Determinar un numero especifico de decisiones o ien establedcer un minimo de casospor nodo
- Post-poda: Permitir el alto crecimietno de un arbol para despues podar de acuerdo a la reduccion de los ratios de los errores encontrados

## Poda o prunning con CART

- Hya que usar el parametro de control de la complejidad cp, que establece rofundizaciones si se producen muchas divisiones. EL valor predetermindado de cp es 0.01. CUnato mas alto sea el valor de cp, mas pequeño sera el arbol

- Un valor de cp demasiado pqueñoprovoca sobreajuste y un valor de cp demasiado alto resultará un arbol demasiado pequeño. Ambos casos disminuyen el rendimiento predictivo del modelo.

- Se puede estimar un valor de cp optimo probandodiferentes valroes y tulizandovalidacion cruzada para determinar la precision de prediccion correspondientedel modelo. El mejor cp se define entonces como el que maximiza la precision de la validacion cruzada.

## VEntajas y desventajas

Ventajas:
- Gran potencia descriptiva, se comprende muy bien el resultado. REsultados a menido simples
- Las transformaciones monótonas sobre las variables continuas no tienen efecto, el arbol solo tiene en cuenta el orden entre observaciones
- Las relaciones no lineales no afectan tanto al comportamiento de los arboles como a otros metodos
- Incorporacion automatica de interacciones, detectan relaciones por regiones que ninguno otro metodo puede encontrar
- SObre todo en clasificacion, pero tmb en regresion, se descubren interacciones y reglas muy dificiles de encontrar con otros metodos. EStas reglas se pueden itilizar como varibales dummy para utulizar en otros metodos predictivos
- NO hay asunciones teoricas  sobre los datos
- Manera propua y eficiente de tratar los missings, incorporada al proceso

DEsventajas:
- Poca fiabilidad y mala generalizacion: cada hoja es un parametro y esto provoca modelos sobreajustados e inestablespara la prediccion. Añadir una variable nueva o un nuevo conjunto de observaciones puede alterar mucho el arbol
- Complejidad en la construccion del arbol y casuistica: dos plataformas diferentes dan dos arboles diferentes
- Poca eficacia predictiva, sobre todo en regresion: toscos en los valores de prediccion. Por ello raramente son el modelo final. SE suelen usar como apoyo  a otros modelos