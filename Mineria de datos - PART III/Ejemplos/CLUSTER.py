## Analisis cluster:
# sirve para resumir y simplificar la gran cantidad de datos
# machine learning: a diferencia de algortimos supervisados el clusterign opera sin etiquetas predefinidas
#tecnica estadistica: busca organizar datos en grupos coherentes

# por ello, el analisis cluster es una tecnica estadistica para clasificar elementos basandose en su homogeiedad. busca homogeniedad entre ellos y 
# heteregeniedad entre elementos de distintos grupos

# posicion inicial: seleccion de una medida de distancia. usa algoritmos segun las medidas.

# algoritmos: 
#   - Jerárquico: forma grupos secuencialmente ya sean fusionados (aglomerativo) o dividiendo (divisivo). no se conoce el numero de grupos de antemano
#   - No herárquico: Se predefine un numero de grupos. Las observaciones se asignan a esos grupos basandose en esta cantidad de grupos distintos

# IMportancia de la seleccion: El exito depende  de la eleccion adecuada de la medida de distancia y del algortimo
# Interpretacion de grupos: La formacion de grupos revela patrones, tendencia y relaciones en los datos que pueden no ser evidentes sin el agrupamiento


# requisitos para realizar analisis de cluster:
# - Escala de variables: Las variables de entrada stienen que estar en la misma escala o ser estandarizadas
# - Ausencia de valores atipicos: Es importante encontrar y manejar estos valores
# - Datos perdidos: Puede ser necesario aplicar técnicas de imputacion de datos
# - Miniminizar la corrlacion entre variables: Es importante que las variables no estén fuertemente correlacionadas entre si

## Pasos para realizar el análisis de clustering:
# - Evaluacion del parecido entre observaciones:
#   - Determinar la proximidad o similitud entre observaciones utilizando medidas de distancia
# - Evaluacion del parecido entre variables
#   - Evaluar la similitud o correlacion entre variables, is el enfoque es entre las caracteristicas en lugar de las observaciones
#- Seleccion de tipos de agrupacion:
#  - Decidir si escoger jerárquico o no jerárquicos.
# - Seleccion de algortimo de agrupacion: Por ejemplo k-menas, agrupamiento jerarquico,...
#- Determinacion del numero optimo de clusters: Este es solo para no jerarquicos. Definir un numero correcto de grupos
#- Interpretaciony validacion de clusters formados:
#  - Analizar e interpretar los grupos resultantes para validar su significado y relevancia.

## ahora vamos a ver las medias distancias entre observaciones:

# las medidas de distancias mas utilizadas son:

# - Distancia euclídia: es la mas utilizada y es la raiz cuadracda de las diferencias de cada vairable al cuadrado

# - Distancia minkowski: En esta se define como la raiz p- esima de la suma de las diferencias de las observaciones de cada valor

# - Distancia de correlacion de pearson: esta la tenemos que usar cuando tenemos que hacer un analisis cluster sobre las variables. Esta medida evalua la similitud entre dos varables
#       basandose en la correlacion lineal de pearson. 
#       - Un valor de -1 indica una relacion lineal perfecta negativa
#       - Un valor de 0 sugiere que no hay relacion loineal
#       - Un valor de 1 indica una relacion lineal perfecta positiva

# - Distancia de correlacion de spearman: esta la tenemos que usar cuando tenemos que hacer un analisis cluster sobre las variables. Utiliza ciando los datos son ordinales o 
#       no cumplen con los supuestos de la correlacion de pearson. por ejemplo, cuando los datos son respuestas a una encuesta de satisfaccion.
#       - Un valor de -1 indica una relacion monotona perfecta negativa
#       - Un valor de 0 sugiere que no hay relacion monotona
#       - Un valor de 1 indica una relacion monotona perfecta positiva

#una relacion monotona sign ifica que las variables tienden a cambiar juntas

# - Distancia de correlacion de kendall: evalua la concordancia nentrre dos conjuntos de datos basandose en la concordancia o discordancia nde los pares de observaciones.
#       - Un valor de -1 indica una falta de concordancia entre los conjuntos de datos
#       - Un valor de 0 sugiere que no hay concordancia ni discordancia sistematica
#       - Un valor de 1 indica que hay una concordancia perfecta

# Vamos a ver como determinar el numero optimo de grupos (k) para algoritmos no jerarquicos.
# # esta relacionada con la bondad de ajuste. se va a utilizar el metodo del codo: se va a trazar el wcss(suma de cuadrados dentro de cada gfrupo) cion respecto al numero k del cluster
# buscando que un grupo mas no produzca diferencias significativas

# otro coeficiente es el coeficiente de la silueeta que nos permite ver como de bneunos hemos sido identiuficando los componentes
# para calculoarlo, primerp por un aldo tenemos que calcular la distancia media a sub i que mida cuan bien se agrupa una observacion i a su propio cluster
# tmb tenemos que calcular la distancia media b sub i al cluster mas cercano. mide cuan bien se separa i de los clusters mas cercanos
# por ultimo tenemos que caluclaur el coeficiente de la silueta que es como la diferencia de b-a entre la diferencia de estas.

#interpretacion:
#       - Un valor de -1 indica posiblemente una asignaciond e cluster erroneo
#       - Un valor de 0 sugiere que esta cerca de la frontera entre dos clusters
#       - Un valor de 1 indica que está bien agruppada y lejos de clusters vecinos

# esto nios ayuda a seleccionar el número de cluisters que ofrece mejor equilibrio

## ahora vamos a ver cluster de caracterizacion:

# sirve para comprender cada cluster a través de  un analisis descriptivo de las variables
# identificacion de miembros: determinar los elemnetos de cada cluster; listados o tablas de pertenencia
# estadisticos descriptivos: medidas como la media mediana,m varianza  desviacion estandar para ver como se comportan los lcusteres
# compoarancion entre clusteres: usar estadisticos para diferenciar clusteres en terminos de variables nalizadas.
# perfilado de cluisters: crear perfiles de basados en estadisticos incluyendo graficas o tablas resumen
# analisis de variables significaticas: identificar variables clave enb la formacion y descripcion de los clusteres
# visaulizacion de los datos: utilizar graficos de barras histogramas o boxplots para ilustrar carasterisitcas de los clusteres.

## fatla solo el ejemplo de pytthon 

## EJEMPLO DE CLUSTER EN PYTHON

# importamos librerias necesarias:
# Importamos las bibliotecas necesarias
import os
import pandas as pd    
import seaborn as sns  
import matplotlib.pyplot as plt  
import numpy as np
from scipy.spatial import distance
from sklearn.preprocessing import StandardScaler
import scipy.cluster.hierarchy as sch
from scipy.cluster.hierarchy import fcluster
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.metrics import silhouette_samples
from scipy.spatial.distance import pdist, squareform
import warnings

#puntos para el ejercuicio:;
#  1) Preparación de los datos: Cargar y visualizar la información contenida en el archivo $EsperanzaVida.xlsx$, estableciendo una comprensión inicial del conjunto de datos.
#  2) Análisis exploratorio: Implementar un mapa de calor para identificar relaciones preliminares y patrones dentro del conjunto de datos.
#  3) Cálculo de distancias: Generar y visualizar una matriz de distancias para evaluar la similitud entre las observaciones.
#  4) Estandarización de datos: Preparar los datos para el análisis de clúster mediante la estandarización, facilitando así la comparabilidad entre las variables.
#  5) Análisis de clúster jerárquico: Aplicar un enfoque jerárquico para agrupar los países y visualizar los resultados con un dendrograma.
#  6) Selección del número de clústers: Utilizar métodos como el del codo y la silueta para determinar el número óptimo de clústers.
#  7) Desarrollar un análisis no jerárquico mediante el algoritmo $k-means$.
#  8) Evalua la calidad de los grupos creados
#  9) Caracterización de clústers: Describir las propiedades y características distintivas de cada clúster identificado.

# Establecer el nivel de advertencias a "ignore" para ignorar todas las advertencias
warnings.filterwarnings("ignore") ## ponemos esto por la advertendia que nos da al hacer el kmeans al calcular el metodo del codo

# Establecemos la ubicación de nuestro directorio de trabajo
os.chdir('C:/Users/gerar/Desktop/Master/Master/Mineria de datos - PART III/Ejemplos/Data')

# Leemos el archivo de Excel en un DataFrame
df = pd.read_excel('EsperanzaVida.xlsx')

# #print(df)
df = df.set_index('PAIS')
# #print(df)

# realizamos un mapa de calor para identidificar relaciones preliminares y patrones del conjunto de datos:
# Creamos el mapa de calor (heatmap) donde se representan de manera ordenada los 
# valores observados, así como un proceso de cluster jerárquico donde se muestran 
# los diferentes pasos iterativos de unión de observaciones y variables.

sns.clustermap(df, cmap='coolwarm', annot=True)
# Agregamos un título al gráfico
plt.title('Mapa de Calor')
# Etiquetamos el eje x
plt.xlabel('          E(vida) por edad y sexo')
# Etiquetamos el eje y
plt.ylabel('País')
# Mostramos el gráfico
plt.show()
# como se puede ver que la esperanza de vida al nacer es mas alta que cuando se es mayopr (es normal)
# en este mapa de calor nos ofrece dos analisis jerarquicos, uno por observacione s al izq y otro por variables arriba

## por variable: se teninede que ha unido m75 y w75, que se encuentran con poca esperanza de vida. las sigueinte en unirse son m50 y w50, que no se ve tan clara la diferencia.
# tiene sentido las agrupaciones que ha hecho ya que ¡ha mezclado las unidades de edad de hombres y mujeres. luego ha juntado las de 50 y 75 y las de 25 y 0.

# lugo a nivel observaciones vemos que los ultimos en unirse soin camerun y madagascar ya que la probabilidad de vida es bastante reducida

# vamos al punto 3, donde calculamos las distinacias para evaluar la similiutud entre las observaciones sin estandarizar los datos
# Calculamos distancias sin estandarizar
# Calcula la matriz de distancias Euclidianas entre las observaciones
distance_matrix = distance.cdist(df, df, 'euclidean') ## vamos a usar la distancia uclidea, pero admite mas opciones. las opciones son las siguientes:
# $Euclidean$, $Manha-ttan$, $Minkowski$, $Chebyshev$, $Cosine$, $Hamming$, $Jaccard$, $Correlation$, $Mahalanobis$, $Canberra$.
# Crea un DataFrame a partir de la matriz de distancias con los índices de df
distance_df = pd.DataFrame(distance_matrix, index=df.index, columns=df.index)
# La distance_matrix es una matriz 2D que contiene las distancias Euclidianas 
# entre todas las parejas de observaciones.

# Seleccionamos las primeras 10 filas y columnas de la matriz de distancias
distance_small = distance_matrix[:10, :10]
# Agregamos los nombres de índice a la matriz de distancias
distance_small = pd.DataFrame(distance_small, index=df.index[:10], columns=df.index[:10])
# Redondeamos los valores en la matriz de distancias
distance_small_rounded = distance_small.round(2)
#print(distance_small_rounded)




## aqui hemos calcuilado la matriz de las distancias , ahora lo representamos gráficamente, poniendo las opciones mas relevantes:

# Representamos gráficamente la matriz de distancias

# Crea una nueva figura para el gráfico con un tamaño específico
plt.figure(figsize=(10, 8))
# Genera un mapa de calor usando Seaborn
# - `distance_df`: DataFrame de pandas que contiene los datos para el mapa de calor.
# - `annot=False`: No muestra las anotaciones (valores de los datos) en las celdas del mapa.
# - `cmap="YlGnBu"`: Utiliza la paleta de colores "Yellow-Green-Blue" para el mapa de calor.
# - `fmt=".1f"`: Formato de los números en las anotaciones, en este caso no se usan.
sns.heatmap(distance_df, annot=False, cmap="YlGnBu", fmt=".1f")
# Muestra el gráfico
plt.show()

## aqui podemos ver que camerun y madagascar muestra que estas tienen una distancia mayor comparados con el resto de paises, y ademas gracias al cuadrado de la distancia entre ellos mismos
# vemos que son parecidos.  luego en guatemala tmb vemos que esta mas alejado mas de la media, del resto. ademas vemois que gauatemala se aclara un ooco con camerun y madagascar
# lo q quiere decir que está mas cerca de ellos q el resto de los paises. pero no se peude ver mucho mas. vamos a hacer un grafico mas avanzado
#  usando tecniacas rde restructuracion para acercar las que estan mas cerca entre si y ademas hacer un analis cluster no jerarquico:

# Realizamos clustering jerárquico para obtener la matriz de enlace (linkage matrix). 
# Clustermap es una función compleja que combina un mapa de calor con dendrogramas para mostrar la agrupación de datos.
# Aquí, estamos usando el dataframe 'distance_df' que contiene las distancias euclidianas entre las observaciones.
# La opción 'cmap' establece la paleta de colores a 'YlGnBu', que es un gradiente de azules y verdes.
# La opción 'fmt' se usa para formatear las anotaciones numéricas, en este caso a un decimal.
# La opción 'annot=False' indica que no queremos anotaciones numéricas en las celdas del mapa de calor.
# La opción 'method' especifica el método de agrupamiento a usar, en este caso 'average' que calcula la media de las distancias.
linkage = sns.clustermap(distance_df, cmap="YlGnBu", fmt=".1f", annot=False, method='ward').dendrogram_row
plt.show()

## aqui en este grafico podemos observar de forma agrupada tanto el mapa de calor como las uniones que se hacen entre si
# por ejemplo podemos ver como guatemala es el ultimo pais que se une a la parte de la derecha
# vemos que camerun y madagascar van por otro lado y es lo ultimo que se une al resto. en cuanto al resto vemos que hay dos grupos, la parte de la izquierda se une todo parecido
# mientras que enm la parte de la derecha, guatemala es el ultimo que se une. 

# ahora vamos a estandarizar los datos que es como se tienen que trabajar: siempre hajy q eestandarizarlo para que todas las vbariables tengan el mismo peso

# Estandarizamos los datos
# Inicializamos el escalador de estandarizacion
scaler = StandardScaler() # usamos la funcion standard scaler para estandarizar los datos
    
# Ajustamos y transformamos el DataFrame para estandarizar las columnas
# 'fit_transform' primero calcula la media y la desviacion estandar de cada columna para luego realizar la estandarizacion.
df_std = pd.DataFrame(scaler.fit_transform(df), columns=df.columns) # lo aplicamos a nuestros datos y ponemos el indice

# Asignamos el indice del DataFrame original 'df' al nuevo DataFrame 'df_std'
# Esto es importante para mantener la correspondencia de los indices de las filas despues de la estandarizacion.
df_std.index = df.index
#print(df_std)

# en este df tenemos ya los datos estandarizadpos.-
# ahora procedemos a calcular las distancias ecluideas con estos datos estandarizados:
# Calculamos las distancias euclidianas por pares entre las filas del DataFrame estandarizado
# 'cdist' calcula la distancia euclidiana entre cada par de filas en 'df_std'.
# Esto resulta en una matriz de distancias donde cada elemento [i, j] es la distancia entre la fila i y la fila j.
distance_std = distance.cdist(df_std, df_std, 'euclidean') 

# Seleccionamos las primeras 10 filas y columnas de la matriz de distancias
distance_small = distance_std[:10, :10]
# Agregamos los nombres de índice a la matriz de distancias
distance_small = pd.DataFrame(distance_small, index=df.index[:10], columns=df.index[:10])
# Redondeamos los valores en la matriz de distancias
distance_small_rounded = distance_small.round(2)

#print(distance_small_rounded)

## ahroa vamos a ver gráficamente estas distancias como hemos visto anteriormente

# Esto determina las dimensiones del grafico
plt.figure(figsize=(10, 8))

# Creamos un nuevo DataFrame para la matriz de distancias
# 'distance_std' se convierte en un DataFrame con indices y columnas correspondientes a 'df_std'
# Esto facilita la interpretacion del mapa de calor, ya que las filas y columnas estaran etiquetadas con los indices de 'df_std'
df_std_distance = pd.DataFrame(distance_std, index=df_std.index, columns=df_std.index)

# Generamos un mapa de calor utilizando Seaborn
# - 'df_std_distance': DataFrame que contiene los datos de distancia para visualizar.
# - 'annot=False': No muestra anotaciones numericas en cada celda del mapa de calor.
# - 'cmap="YlGnBu"': Define una paleta de colores en tonos de azul y verde para el mapa de calor.
# - 'fmt=".1f"': Formato de los numeros en las anotaciones, en este caso, un decimal.
sns.heatmap(df_std_distance, annot=False, cmap="YlGnBu", fmt=".1f")

# Mostramos el grafico resultante
plt.show()

## lo q podemos ver es que los coleres se han aclarado un pooco, hemos perdido la referencia de la cruz de guatemala (se ha difumindao todo un poco mas)

# vamos a ver el otro grafico que se ve todo mejor:

# Realizamos clustering jerárquico para obtener la matriz de enlace (linkage matrix) sobre las distancias estandarizadas. 
linkage = sns.clustermap(df_std_distance, cmap="YlGnBu", fmt=".1f", annot=False, method='ward').dendrogram_row
plt.show()

# aqui vemos que algunos paises como nicaragua que se ha reducio distancia con el resto porq se ve uin poco mas azul

# tmb podemos ver las uniones de los grupos que ha cambiado (con lo q ha cambiado la jerarquia)
# tya no vemos los mismos grupos, ahora vemos mas grupos que son mas chicos y se van juntando aun mas con otros grupos. Esto sirve para ver la importancia de estandarizar los datos

# ahora vamos a ver el dendograma de manera aislada sin el mapa de calor. esto es iun resultado q nos es muiy util:
# Establecemos un umbral de color para el dendrograma
# color_threshold = 3
color_threshold = 5

linkage_matrix = sch.linkage(df_std, method='ward')  # Puedes elegir un metodo de enlace diferente si es necesario

# Creamos el dendrograma con el umbral de color especificado
dendrogram = sch.dendrogram(linkage_matrix, labels=df_std_distance.index.tolist(), leaf_rotation=90, color_threshold=color_threshold) # la funcioin de color_threshold, 
# nos da una idea de grupos. esto depende de el umbral del color que le demos. por ejemplo si le damos 5, nos salen 3 grupos pero si le damos 3, nos salen 7. Esto se debe a la cantidad de subgrupos q quieras agrupar

# Mostramos el dendrograma
plt.show()

# tenemos q poner de limite cuando un grupo que se van a juntar con otro, hace una diferencai vertical muy grande por lo tanto 5 es un buen punto y nos quedamos con 4 grupos 
# una vvez tenemos los grupos, vamos a especificar los grupos de clusteres. (en un analisis jerarquico se puede hacer el corte y prefijar el numero de grupos)

# vamos a ahcerlo:
# Asignamos las observaciones de datos a 4 clusters

# Especificamos el numero de clusters a formar
num_clusters = 4

# Asignamos los datos a los clusters
# 'fcluster' forma clusters planos a partir de la matriz de enlace 'linkage_matrix'
# 'criterion='maxclust'' significa que formaremos un numero maximo de 'num_clusters' clusters
cluster_assignments = fcluster(linkage_matrix, num_clusters, criterion='maxclust')
    
# Mostramos las asignaciones de clusters
print("Cluster Assignments:", cluster_assignments) 

# Creamos una nueva columna 'Cluster4' y asignamos los valores de 'cluster_assignments' a ella
# Ahora 'df' contiene una nueva columna 'Cluster4' con las asignaciones de cluster
df['Cluster4'] = cluster_assignments
print(df)

# con estop podemos ver que país se ha unido a qué grupo

# ahora vamos a relaizar un PCA representando estos clusters en 2 ejes (estos componentes de la PCA seran los ejes)
# Visualización de la distribución espacial de los clusters
# Paso 1: Realizar PCA
pca = PCA(n_components=2)  # Inicializamos PCA para 2 componentes principales
eliminar = ['Cluster4']
principal_components = pca.fit_transform(df.drop(eliminar, axis=1))  # Transformamos los datos a 2 componentes

fit = pca.fit(df_std)
# Calculamos las dos primeras componentes principales
resultados_pca = pd.DataFrame(fit.transform(df.drop(eliminar, axis=1)), 
                              columns=['Componente {}'.format(i) for i in range(1, fit.n_components_+1)],
                              index=df.index)

# Añadimos las componentes principales a la base de datos estandarizada.
df_z_cp = pd.concat([df_std, resultados_pca], axis=1)

# Calculo la matriz de correlaciones entre veriables y componentes
Correlaciones_var_comp = df_z_cp.corr()
Correlaciones_var_comp = Correlaciones_var_comp.iloc[:fit.n_features_in_, fit.n_features_in_:]
print(Correlaciones_var_comp)
# aqui opodemos ver las correlaciones enrtre las variables y lols compoinentes creados. 
# POdemos ¡ver que la componente 1 tiene fuerte correlacion mas con las edades bajas mientreas que la componente 2 también pero de forma mas brusca

# vamos a verlo graficamente en estos ejes:
# Creamos un nuevo DataFrame para los componentes principales 2D
# Nos aseguramos de que df_pca tenga el mismo índice que df
df_pca = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2'], index=df.index)


# Paso 2: Crear un gráfico de dispersión con colores para los clusters
plt.figure(figsize=(10, 6))  # Establecemos el tamaño del gráfico

# Recorremos las asignaciones únicas de clusters y trazamos puntos de datos con el mismo color
for cluster in np.unique(cluster_assignments):
    cluster_indices = df_pca.loc[cluster_assignments == cluster].index
    plt.scatter(df_pca.loc[cluster_indices, 'PC1'],
                df_pca.loc[cluster_indices, 'PC2'],
                label=f'Cluster {cluster}')  # Etiqueta para cada cluster
    # Anotamos cada punto con el nombre del país
    for i in cluster_indices:
        plt.annotate(i,
                     (df_pca.loc[i, 'PC1'], df_pca.loc[i, 'PC2']), fontsize=10,
                     textcoords="offset points",  # cómo posicionar el texto
                     xytext=(0,10),  # distancia del texto a los puntos (x,y)
                     ha='center')  # alineación horizontal puede ser izquierda, derecha o centro

# Líneas de referencia para los ejes x e y
plt.axhline(0, color='black', linestyle='--', linewidth=0.5)
plt.axvline(0, color='black', linestyle='--', linewidth=0.5)

plt.title("Gráfico de PCA 2D con Asignaciones de Cluster")
plt.xlabel("Componente Principal 1")
plt.ylabel("Componente Principal 2")
plt.legend()
plt.grid()
plt.show()

# viendo este gráficofijandonos en la componente 1 (eje x) madagascar y camerun son los q menos esperanza de vida tienen pporq estan por debajo de la media comparados al resto de paises
# igual pasa con cananda y estados unicos que son los que mas a la derecha aparecen con lo q tendran una media de edad mas por encia de la media
# aqui vemos la utilidad de utilizar las dos técnicas juntas (cluster y pca)
# aqui hemos terminado el analisis cluster jerarquico, ahora vmos con el no jerarquico. opara ello vamos indicar el numero de cluster que queremos

# para ello basandojnos en lo que nos ha indicado el jerarquico vamos a argumentar q 4 puede ser un buen numero de grupos. vamos a ver que nos dicen otros metodos como el del codo o el de la silueta

# primero vamos a ver el metodo del codo:

# Metodo del codo
# Creamos un array para almacenar los valores de WCSS para diferentes valores de K
wcss = []
    
for k in range(1, 11):  # Puedes elegir un rango diferente de valores de K
    kmeans = KMeans(n_clusters=k, random_state=0, n_init=10)
    kmeans.fit(df_std)
    wcss.append(kmeans.inertia_)  # Inserta es el valor de WCSS


# aqui enfrrentamos el wcss con el numero de grupos
# Graficamos los valores de WCSS frente al numero de grupos (K) y buscamos el punto "codo"
plt.figure(figsize=(8, 6))
plt.plot(range(1, 11), wcss, marker='o', linestyle='-', color='b')
plt.title('Metodo del Codo')
plt.xlabel('Numero de Clusters (K)')
plt.ylabel('WCSS')
plt.grid(True)
plt.show()

# en este gráfico vemos el punto de corte donde nos indica que perdemos muchja pendiente por lo tanto q deja de ser muy relevante. pero nod eja muy calra cuiandpo es cuando mas se peirde
# podemos suiponer q 4 es el mas razonabel

# vamos a ver el metodo de la silueta: que lo que hace es ver como de cerca estaria de un grupo y como de lejos estaria del q tiene al lado:
# Metodo de la silueta  
# Creamos un array para almacenar los puntajes de silueta para diferentes valores de K
silhouette_scores = []
    
# Ejecutamos el clustering K-means para un rango de valores de K y calculamos el puntaje de silueta para cada K
for k in range(2, 11):
    kmeans = KMeans(n_clusters=k, random_state=0)
    kmeans.fit(df_std)
    labels = kmeans.labels_
    silhouette_avg = silhouette_score(df_std, labels)
    silhouette_scores.append(silhouette_avg)
    
# Graficamos los puntajes de silueta frente al numero de clusters (K)
plt.figure(figsize=(8, 6))
plt.plot(range(2, 11), silhouette_scores, marker='o', linestyle='-', color='b')
plt.title('Metodo de la Silueta')
plt.xlabel('Numero de Clusters (K)')
plt.ylabel('Puntaje de Silueta')
plt.grid(True)
plt.show()

# este metodo de la silueta nos dice q lo mejor es 2 grupos. como nosotros sabemos que camerun y madascar estan muy separados del resto,m sabemos  q un grupo van a ser estos dos mientras que el otro grupo va a ser el resto. por ello gracias a lo q nos dicen los datos vamos a descartar el dos y vamos a buscar el siguietne maximo local q es 4.

# vamos a ahjcer el algortimo kmeans con el numero de centroides asignacdos (4 en este caso)

# Analisis no jerarquico
# Configurar el número de clusters (k=4)
k = 4

# Inicializar el modelo KMeans
# 'n_clusters=k' indica el número de clusters a formar
# 'random_state=0' asegura la reproducibilidad de los resultados
# 'n_init=10' indica el número de veces que el algoritmo se ejecutará con diferentes centroides iniciales
kmeans = KMeans(n_clusters=k, random_state=0, n_init=10)


# Ajustar el modelo KMeans a los datos estandarizados
# 'df_std' es el DataFrame que contiene los datos previamente estandarizados
kmeans.fit(df_std)

# Obtener las etiquetas de los clusters para los datos
# 'kmeans.labels_' contiene la asignación de cada punto a un cluster
kmeans_cluster_labels = kmeans.labels_

# Creamos una nueva columna 'Cluster' y asignamos los valores de 'kmeans_cluster_labels' a ella
# 'Cluster4_v2' sera el nombre de la nueva columna en el DataFrame 'df'
df['Cluster4_v2'] = kmeans_cluster_labels

# Ahora 'df' contiene una nueva columna 'Cluster4_v2' con las asignaciones de cluster
# Imprimimos los valores de la columna 'Cluster4_v2' para verificar las asignaciones de cluster
print(df["Cluster4_v2"])

# ahora vamos a calcular el coefciciente de la silueta para cada situacion y vamos a representar loq nahce:

# Calculamos los valores de silueta para cada observación
silhouette_values = silhouette_samples(df_std, kmeans.labels_)
    
# Configuramos el tamaño de la figura para el gráfico
plt.figure(figsize=(8, 6))
y_lower = 10  # Inicio del margen inferior en el gráfico

# Iteramos sobre los 4 clusters para calcular los valores de silueta y dibujar el gráfico
for i in range(4):
    # Extraemos los valores de silueta para las observaciones en el cluster i
    ith_cluster_silhouette_values = silhouette_values[kmeans.labels_ == i]
    # Ordenamos los valores para que el gráfico sea más claro
    ith_cluster_silhouette_values.sort()
    
    # Calculamos donde terminarán las barras de silueta en el eje y
    size_cluster_i = ith_cluster_silhouette_values.shape[0]
    y_upper = y_lower + size_cluster_i
    
    # Elegimos un color para el cluster
    color = plt.cm.get_cmap("Spectral")(float(i) / 4)
    # Rellenamos el gráfico entre un rango en el eje y con los valores de silueta
    plt.fill_betweenx(np.arange(y_lower, y_upper),
                      0, ith_cluster_silhouette_values,
                      facecolor=color, edgecolor=color, alpha=0.7)
    # Etiquetamos las barras de silueta con el número de cluster en el eje y
    plt.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))
    # Actualizamos el margen inferior para el siguiente cluster
    y_lower = y_upper + 10  # 10 para el espacio entre clusters

# Títulos y etiquetas para el gráfico
plt.title("Gráfico de Silueta para los Clusters")
plt.xlabel("Valores del Coeficiente de Silueta")
plt.ylabel("Etiqueta del Cluster")
plt.grid(True)  # Añadimos una cuadrícula para mejor legibilidad
plt.show()  # Mostramos el gráfico resultante

# apra cada grupo tenemosm representado el coeficiente de la silueta. Podemos ver q tenemos 2 observaciones mal clasificadas (estan a la izquierda del 0)

# igual aqui seria aconsejable probar con un 3, un 5,... probar y ver cuando salen los mejores coeficientes de la silueta.

# una vez calrificadas yta los grupos y demas, vamos a ver con los ejes de las componentes principales:
# Caracterizamos cada cluster
# Visualizacion de la distribucion espacial de los clusters

plt.figure(figsize=(10, 6))  # Definir el tamaño de la figura

# Iterar a traves de las etiquetas unicas de clusters y graficar puntos de datos con el mismo color
for cluster in np.unique(kmeans_cluster_labels):
    cluster_indices = df_pca.loc[kmeans_cluster_labels == cluster].index
    plt.scatter(df_pca.loc[cluster_indices, 'PC1'],
                df_pca.loc[cluster_indices, 'PC2'],
                label=f'Cluster {cluster}')  # Poner una etiqueta para cada cluster
    
    # Anotar cada punto con su respectivo indice
    for i in cluster_indices:
        plt.annotate(i,
                     (df_pca.loc[i, 'PC1'], df_pca.loc[i, 'PC2']),fontsize=10,
                     textcoords="offset points",  # Define como se posicionara el texto
                     xytext=(0,10),  # Define la distancia del texto a los puntos (x,y)
                     ha='center')  # Define la alineacion horizontal del texto

# Líneas de referencia para los ejes x e y
plt.axhline(0, color='black', linestyle='--', linewidth=0.5)
plt.axvline(0, color='black', linestyle='--', linewidth=0.5)

# Configurar el titulo y las etiquetas de los ejes del grafico
plt.title("Grafico 2D de PCA con Asignaciones de Cluster KMeans")
plt.xlabel("Componente Principal 1")
plt.ylabel("Componente Principal 2")
plt.legend()  # Mostrar la leyenda
plt.grid()  # Mostrar la cuadricula
plt.show()  # Mostrar el grafico

# el grafico es el mismo solo cambvian los colores. podemos ver que el unico cambio esta en mexico que en uno esta pro debajo y en el anterior esta poor arriba

#@ ahora para carazxterizar vamos a caracterizar agrupando por clusteres.
# Añadimos las etiquetas como una nueva columna al DataFrame original
df['Cluster'] = kmeans.labels_
# Ordenamos el DataFrame por la columna "Cluster"
df_sort = df.sort_values(by="Cluster")

# Agrupamos los datos por la columna 'Cluster' y calculamos la media de cada grupo
# Esto proporcionará las coordenadas de los centroides de los clusters en el espacio de los datos originales
cluster_centroids_orig = df_sort.groupby('Cluster').mean()
# Redondeamos los valores para facilitar la visualización
cluster_centroids_orig.round(2)
# 'cluster_centroids_orig' ahora contiene los centroides de cada cluster en el espacio de los datos originales