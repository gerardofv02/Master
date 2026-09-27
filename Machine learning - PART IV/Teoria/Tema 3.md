# Hands on classification problem

## Limpieza de datos

Tras una primera exploracion de los datos, vamos a centrarnos, vamos a centrarnos ahora en algunas operaciones habituales de limpieza de datos:
    - DEtectar posibles filas duplicadas
    - DEtectar posibles columnas no informativas
    - DEtectar posibles NA/Null values
    - Detectar posibles outliers

### FIlas duplicadas

- Las filas duplicadas sesgan cualquier modelo predictivo
- ES, por tanto, prioritario eliminarlas antes de usarlas en cualquier modelo
- EN muchas ocasiones, realizamosla eliminación de los duplicados siempre al principio de cualquier trabajo
- Pero, al ir transformando nuestro dataset, se van eliminando columnas y puede existir filas que se distinguian en el dataset originalpor alguna de las variables eliminadsas. POr tanto, conviene realizar este proceso también justo antes de entrenar el modelo

### COlumnas poco informativas

- Las columnas categoricas que tienen todos sus valores iguales, no aportan información para el modelo
- EStas variables, se pueden identificar relativamente bien en cualquier análisis exploratorio con un simple barplot
- Igualmente , las columnas numericas con poca varianza tienen el mismo problema. Pero para identificarlas cuesta siempre un poco mas

### null/na values

- NOtiene sentido trabajar con valores nulos. hay que tomar una decision:
    - O se transofmran
    - O se rellenan
    - o se eliminan

- y pueden estar tanto en las columnas como en las filas. ES decir, podemos encontrarnos filas con casi todos sus valores nulos o columnas con casi todos sus valroes nulos.

- La decision tiene un carácter subjetivo que depende del data scientist y de la naturaleza del modelo y los datos
- CUalquier decision que tomemos va a implicar un sesgo en el modelo

- EN muchjas ocasiones, se pueden crear variables dummy(booleanas) que indiquen si la columna tiene o no un valor nulo. Generalmente se hace cuando hay un 50/50
- CUnado es una serie temporal, se suelen interpolar los datos
- Cuando representan menos del 5% de los datos, se podrían eliminar
- Cunado no tenemos claro qué estrategia llevar, se pueden sustituir por valores medios, medianos, modas o el valor más cercano. Aqui podemos utilizar imputers
- EN ocasiones más específicas se peuden generar números aleatorios que sigan la dsitribución de la variable

### outliers

- En distribuciones normales, se cumple qu el 99.7% de los datos debe estar en el intervalo 'seis-sigma' alrededor de la media. LO que esté fuera de este intervalo puede ser outlier
- Otra forma de hacer lo mismo es mediante el Rnago Intercuartílico para lozalizar outliers, pero igualmente, funciona vien en distribuciones normales

- Otra forma interesante es utilizar la técnica que abarcan mas de una dimension como:
    - LOcal outlier factort
    - DBSCAN
    - IsolationFOrest


## transfoamrcion de vairbales

Vamos a distinguir transformaciones segun tipo de variabel
Para categoricas, veremos aqui:
    - Label encoder
    - Ordinal encoder
    - One hot encoder
    - DUmmy variables

Para las numericas, ya estudiamos standarize y minmaxscaler. En este ejemplo veremos algunas mas robustas:
- Robust scaler
- Box-Cox

### label encoder

Transforma a numerico ordinal la variable target

### ordinal encoder

Trnaforma a numericoo ordinal cualquiera de las variables predictoras manteniendo sentido de orden

### one hot encoder

Transforma a booleana cualquiera de la sbariables predictoras y crea variablespara cada una de las opcioens

### dummy variables

Transofrma  a boolean cualquiera de las variabels predictoras y crea variables para cada una de las opciones

## numericasahora

### robust scaler

- El principal problema  de los outliers es que afecta mucho al a todo fórmula que conlleve en el cálculo operaciones algebraicas sobre los datos:
    - MEdias, desviaciones, varianzas,...
    - Algoritmoscomo regresion lineal, linear discriminant analysis,...

SIn embargo, no afecta tanto a otros tipos de calculos
    - Percentiles, cuartiles,...
    - Algunos algoritmos como decision trees, random forest,...


### Box-cox

- Mediante transformaciones no linealespodemos conseguir que una variable aleatoriacon una disribucion no gaussiana consiga aproximarse a algo mas normal y ratable
- AUnque haya mas posiblesopciones de transformacion de variables. Box-cox nos permite, rapidamente, intuir cual seria la trnasformacionmas aproximada

## TEcnicas de validacion

### corss validation splits

Objetivo: overfitting & imbalanced data

- cviteration: numero de veces q se realiza el fitting del modelo para cada una de las particiones del conjunto de datos
- class: Etiqueta eu tratamos de predecir
-GRoup


## Metricas

las metricas q veremos se usan con bastante frecuencia y todas provienen de la matriz de confusion
    - precision
    - recall
    - f1
    - classification report

### Precision-recall (and f1)
la precision es una medida util del exito de la predicccion cuando las clases estan muy desbalanceadas
La precision es una medida de relevancai de los resultados mientras que recall es una medida de cuantos resultados verdaderamente relevantes se devueven
finalmente f1 es la medida armonica de ambas

### clasificaction report

de dicha cm , tmb podemos mostrar un report

## parametriuzacion de algoritmos

Randomized earch cv

A diferencia del gridsearchcv, no se prueban todos los valores de los parametros, sino que se muestra un numero fijo de ajustes de parámetros de las distribuciones especificacdas
EL numeroo de ajustes de parametros que se prueban viene dado por n_iter. La caractersitica mas importante es el ahorro computacional