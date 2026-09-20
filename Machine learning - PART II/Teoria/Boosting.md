# Boosting

ES un procedimiento iterativo. EL bagging va en paralelo para entrenar el algoritmo mientras que el boosting es mas itreativo.
SE puede usar cualquier modelo base
SE basan esencialmente  en procedimientos irterativos que van mejorando a partir de clasificadores débiles con respecto  a una distribucion que se van a gregandopara obtener un clasificador fuerte final

CUando se agregan los clasificadores, generalmente se ponderan de alguna forma que suele estar relacionada con la precisión que han ido obteniendo. DEspues de agregar estos clasificadores, los pesos de los datos también se reajustam.

EL proceso de reajuste de las observaciones se denomina 're-ponderacion'- LOs datos de entrada mal clasificados ganan más peso y los datos que se clasifican correctamente por la mayoria de clasificadores debilespierden peso. DE esta manera en las iteraciones posteriores los clasificadores débiles entran mas en aquellas observaciones que anteriormente han sido clasificadas erroneamente

Este algoritmo se caracteriza por tener una gran cantidad de hiperparametros. Tres de los mas comunes son:
- EL número de weak learners o numero de iteraciones: a diferencia del bagging el boosting puede sufrir overfitting si este valor es excesivamente alto. Para evitarlo emplea un término de regularizacion conocido como learinign rate
- Learning rate: Controla el ritmo al que aprenden los modelos. Suelen recomendarse valores entre 0.01 y 0.001 aunque la eleccion correcta puede variar dependiendo de cual sea el problema. CUanto menos sea el vaor de learning rate mas modelos individuales se necesitan para alcanzar buenos resultados pero menor es el riesgo de overfitting
- LO shiperparametros propios de cada modelo base. SI los weak learners son árboles, el número de divisiones de cada arbol o el tamañode sus hojas. SUelen emplearse modelos sencillos, por ejemplo, árboles con menos de 10 divisiones o hojas grandes.