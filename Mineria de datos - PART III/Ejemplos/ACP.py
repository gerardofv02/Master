## Es una técnica que se usa poara transformar variables en componentes principales que sean independientes (ya que damos por hecho que son variables correlacionadas)
## Una vez transaformadas,  El primer componente principal captura la mayor parte de variabilidad y resume la info de las variabvles originals
## El segundo componente principal es ortogonal al primeroy expliva el que sigue de mayor variabilidad

## Los requisitos que tienne que tener los datos originales son:
# - Variables tienne que estar en la misma escala, es decir, que tengan el mismo peso.
# - Ausencia de valores atípicos: Quitar los datos atipicos y convertirlos en moda, varianza,...
# - Datos Perdidos: No puede hjaber datos perdidos por lo q es necesaria técnicas de imputación

## Pasos matemáticos del proceso:
# -Estandarizaciónj de los datos: Si las esalas difieren, tenemos que estandirizar sus datos.
# - #Si los datos originales estan en la misma escala (poco habitual) se podria calcular la matriz de covarianzas (no es lo mas aconsejable pero seri suficiente
# - Si  no, se tiene que calcular la matriz de correlaciones
# Una vez tenemos la matriz, tenemos que calcular los autovalores propios asociados a dicha amtriz
# Cada autovalor esta asociado a un componente principal es por ello q no es necesario que datonos con todos los autovalores (nos quedaremos solo con los k q nos interesen)
# Determincacion de los vectores propios asociados.
#Construcción de la matriz de transformacion con los vectores de los valores propios asociados para transformar los datos en los componentes principales
# Calculo de los componentes principales para tener un nuevo conjunto de datos estandarizados.

# Cosas a tener en cuenta: Influencia de variables(Si no se estandariza las variables con mayor vbariabilidad tendrán más peso
# ) y comparabilidad: SI se planea comprar un acp con otro pero con distintas escalas, la estandarizacion podría ser esencial

## Una de las decisiones mas importantes es la seleccion del numero de los componentes principales (denotado como k). Esto es esencial para que el acp tenga una 
# cantidad razonable de variabilidad que si añado otra, no me suponga tanta mejora.



## Para hacer un ACP es muy importante daber la relacion entre componentes principales y variables
# esta relacion se basa en conceptos clave. 
# - Lambda sub i representa el autovalor asociado a la i-esima componente principalobtenido en la ACP. Una 
# valor alto, implica que el componente principal de i retiene una gran cantidad de información o varibailidad mientras que uno bajo retiuene poco
# - e sub ij representa el coeficiente ubicado en la posicion ij del vector propio asociadop a la componente principal sub i. En otras palabras: eij muestra cuanto 
# peso tiene la variable Xj en la definicion de los valores de los componentes principales i
# - Ser puede calcular la covarianza para que nos de informacion sobra la relacion lineal entre el componente principal y la variable.
#Una covarianza positiva indica que cuando una variable aumenta, la otra tmb, mientras que al reves casi que no o iuncluso decrece. pero si es 0 no tiene relacion

# - Correlacion entre el componente principal y la variable. Esto tiene relacion con la covarianza. si una vcorrelacion vale 0 tiene poca relacion lineal.
# - Cosenos al cuadrado expresan la proporcion de la varianza de cada variable origenal que se explica mediante cada componente principal
# - Ahora vemos lam relacion contraria como cada variable ayuda en la construccion de cada uino de los componentes. para ello hay que calcular
# la constribucion de ij = cos al cuadradoij * la raiz de lambda sub i

## Si vienen individuos nuevos , se llaman individuos suplemnetarios poero si vienen nuevas pvariables, se les llama variable suplementarias. Esto se +
# debe a que cuando se hace un ACP, los datos de donde los coghemos podrían crearse mas col8umnas con lo q no estaban en el acp incial pero se tienen que incorporar

# El proceso a seguir es lel siguiente:
# - individuos suplemnetarios: Primero se tienen que estandarizar los datos originale, posteriormente lo añadimos  anuestra base de datos estandarizada para proceder a 
# calcualr sus coordenadas CP
#- VBairables nuevass: Representar el centroides de estas categorías en los ejes de las componentes principales, Estros actuan como resumenes para entender la relacion entre distintas categorias


## EJEMPLO COMPLETO DE ACP EN PYTHON::

##importamos librerias

import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

os.chdir('C:/Users/gerar/Desktop/Master/Master/Mineria de datos - PART III/Ejemplos/Data')

notas = pd.read_excel('NOTAS.xlsx')
# ####print(notas)

notas  = notas.set_index('Alumno', drop=True)

extra = notas.iloc[:,[7]] ##quitamos la variable extraescolar pero la guardamos en otra variable para un futro analisis

eliminar = ['EXTRA_ESC']
notas = notas.drop(eliminar, axis=1)

variables = list(notas.columns)

# calculamos ahora los estadisticos descriptivos
estadisticos = pd.DataFrame({
    'Mínimo': notas[variables].min(),
    'Percentil 25': notas[variables].quantile(0.25),
    'Mediana': notas[variables].median(),
    'Percentil 75': notas[variables].quantile(0.75),
    'Media': notas[variables].mean(),
    'Máximo': notas[variables].max(),
    'Desviación estandar': notas[variables].std(),
    'Varianza': notas[variables].var(),
    'Datos perdidos': notas[variables].isna().sum
})
####print(estadisticos)
# como vemos en estos estadisticos, hay datos erroneos ya que en el maximo que nso devuelve tenemos notas cuyo máximo supera el 10 cuando no debe ser asi

# primero vemos cuantos son
observaciones_altas = notas[(notas['Ingles'] > 10) | (notas['Literatura'] > 10)]
cantidad = len(observaciones_altas)
# ####print(cantidad) ## vemos que son solo 3
## decidimos que lkas notas que son mas de 10, sean 10
notas['Ingles'] = notas['Ingles'].clip(upper=10)
notas['Literatura'] = notas['Literatura'].clip(upper=10)

## arreglado :)

## calculamos la matriz de la covarianza:
cov = notas.cov()
# ####print(cov)
## aqui podemos ver como diagonalmente tenemos los valores mas altos ya que matimaticas depende de mates pero leugo en el resto tenemos mas o menos altas dependendias
# pero nos tenemos que centrar mas en la correlacion

corr = notas.corr()
####print(corr)
# matriz de corelacion con los datos de la correlacion que es la covarianza pero con los datos ya estandarizados
## comom podemos ver en estas relaciones vemos que hay mucha correlacion entre las asignaturas que son consideradas ciencias enre ellas mientras que tmb hay fuerte correlacion
# entre las asignaturas que se han considereo letras entre ellas.

## mostramos gráficamente matriz de correlaciones:
plt.figure(figsize=(10,8))
sns.heatmap(corr,annot=True,cmap='coolwarm',fmt='.2f',linewidths=0.5)
plt.show()  

## analisis de componentes principales (PCA/ACP)

##PRIMERO DE TODO: ESTANDARIZAR LOS DATOS
notas_estandarizadas = pd.DataFrame(
    StandardScaler().fit_transform(notas),
    columns=['{}_z'.format(variable) for variable in variables],
    index=notas.index
)
##print(notas_estandarizadas) # ya tenemos las notas estandarizazdas para que todas las variables tengan el mismo peso tenemos la base de datos ya estandarizada

# Procedemos a la construicciion de las compontentes principales
pca = PCA(n_components=7) # cantidad de varianbes q tentemos
fit = pca.fit(notas_estandarizadas) # añadimos la base de datos estandarizada ajustando el modelo
autovalores = fit.explained_variance_ # obtenemos los autovalores asociados a cada componente principal
##print(autovalores)

#vemos el primer valor divido entre la suma del resto :
###print(autovalores[0]/sum(autovalores)) ## 0.41100
#esto quiere decir que la primera componente explciara un 41% de la base de datos
###print(autovalores[1]/sum(autovalores))# 0.33
# esto quiere decir que el segundo componente explicara un 33% de la base de datos

#una vez tenemos calculados los autovalores procedemos a calcular sus autovectores asociados:
autovectores = pd.DataFrame(pca.components_.T,
                            columns = ['Autovector {}'.format(i) for i in range(1,fit.n_components_+1)],
                            index= ['{}_z'.format(variable) for variable in variables])

##print(autovectores)
## aqui vemos la relacion lineal que tienne las variables con los componentes. por ejemplo en el primer compoennte tiene un relacion con matematicas de 0.11

##construimos los componentes:
resultados_pca = pd.DataFrame(fit.transform(notas_estandarizadas),
                              columns=['Componente {}'.format(i) for i in range(1,fit.n_components_+1)],
                              index= notas_estandarizadas.index)

##print(resultados_pca) # con esto nos quedamos con la matriz de coordenadas de las 120 observaciones (alumnos) en los nuevos ejes


##PASAMOS A DETERMINAR EL NUMERO DE COMPONENTES PRINCIPALES
var_explicada = fit.explained_variance_ratio_*100
var_acumulada = np.cumsum(var_explicada)

data = {'Autovalores': autovalores, 'Variabilidad Explicada':var_explicada, 'Variabilidad Acumulada': var_acumulada}
tabla = pd.DataFrame(data, index=['Componente {}'.format(i) for i in range(1,fit.n_components_+1)])
##print(tabla)
# en esta tabla podemos ver completamente lo siguietne : el autovalor del componente principal, la vbariabildiad explicada y la acumulada
# vam,os a verlos graficamente

# Representacion de la variabilidad explicada (Método del codo):   

def plot_varianza_explicada(var_explicada, n_components):
    """
    Representa la variabilidad explicada por cada componente principal
    Args:
      var_explicada (array): Un array que contiene el porcentaje de varianza explicada
        por cada componente principal. Generalmente calculado como
        var_explicada = fit.explained_variance_ratio_ * 100.
      n_components (int): El número total de componentes principales.
        Generalmente calculado como fit.n_components.
    """  
    # Crear un rango de números de componentes principales de 1 a n_components
    num_componentes_range = np.arange(1, n_components + 1)

    # Crear una figura de tamaño 8x6
    plt.figure(figsize=(8, 6))

    # Trazar la varianza explicada en función del número de componentes principales
    plt.plot(num_componentes_range, var_explicada, marker='o')

    # Etiquetas de los ejes x e y
    plt.xlabel('Número de Componentes Principales')
    plt.ylabel('Varianza Explicada')

    # Título del gráfico
    plt.title('Variabilidad Explicada por Componente Principal')

    # Establecer las marcas en el eje x para que coincidan con el número de componentes
    plt.xticks(num_componentes_range)

    # Mostrar una cuadrícula en el gráfico
    plt.grid(True)

    # Agregar barras debajo de cada punto para representar el porcentaje de variabilidad explicada
    # - 'width': Ancho de las barras de la barra. En este caso, se establece en 0.2 unidades.
    # - 'align': Alineación de las barras con respecto a los puntos en el eje x. 
    #   'center' significa que las barras estarán centradas debajo de los puntos.
    # - 'alpha': Transparencia de las barras. Un valor de 0.7 significa que las barras son 70% transparentes.
    plt.bar(num_componentes_range, var_explicada, width=0.2, align='center', alpha=0.7)

    # Mostrar el gráfico
    plt.show()
    
plot_varianza_explicada(var_explicada, fit.n_components_)

## Como podemos ver en esta graficaa a partir del tercer componente ya no tiene tanbta variabildiad y no nos dicen tanto el componente.
#por lo tanto añadir una tercera componente no aporta mucho y ademas (impoortante) si añado la tercera porq no añadir el resto cuando tienen variabilidades similares?
# por ello solo se coge el primer y el segundo componente principal

# Como hempos decidido quedarnos con dos compoenntes, repetimos todo pero solo con 2 componente en el PCA:
pca = PCA(n_components=2)
fit = pca.fit(notas_estandarizadas)

autovalores = fit.explained_variance_
autovectores = pd.DataFrame(pca.components_.T,
                            columns=['Autovector {}'.format(i) for i in range(1,fit.n_components_+1)],
                            index=['{}_z'.format(variable) for variable in variables])
#print(autovectores)
# para calcular nuestros componentes pprincipales por alumno, se tendria que usar la formula que viene en imagen

# calculamos los dos primeros componentes principales y las añadimos a la bse de datos estandarizado:
resultados_pca = pd.DataFrame(fit.transform(notas_estandarizadas),
                              columns=['Componente {}'.format(i) for i in range(1,fit.n_components_+1)],
                              index= notas_estandarizadas.index)
notas_z_cp = pd.concat([notas_estandarizadas,resultados_pca], axis=1)
#print(notas_z_cp)

# vamos a ver ahora las relaciones enrtre componentes principales y variables
variables_cp = notas_z_cp.columns # guaradmos columnas de la tabla completa
n_variables = fit.n_features_in_ #ver la cantidad de variables noramles de la base original
# ahora creamos a la matriz de covarianzas entre variables y componentes
covarianza_var_comp = notas_z_cp.cov()
covarianza_var_comp = covarianza_var_comp.iloc[:fit.n_features_in_, fit.n_features_in_:]
# print(covarianza_var_comp) # no esuna metrica adecuada y se usa mas la correlacion #
correlacion_var_comp = notas_z_cp.corr()
correlacion_var_comp = correlacion_var_comp.iloc[:fit.n_features_in_, fit.n_features_in_:]
print(correlacion_var_comp) ## aqui en esta matriz podemos ver la correlacion entre vairables y componentes pprincipales
# vemos que la primera compoente esta fuertemente relacionada con la nota de lengua, ingles historia y literatura. (letras)
#Luego vemos que la componente dos esta fueremente relacionada con matematicas, fisica  y economia (ciencias)
# obtenemos los cosenos cuadradados
cos2 = correlacion_var_comp**2
print(cos2)
# estos valores nos indican que porcenajte de la variable es explicado por la primera y cuanto por alñ segunda.
# la suma es de cuanto se ha explicado con las dos componentes a la vez (mates un 88% ñor ejemplo 4% por la componente 1 mientras que un 84% en la 2)

# lo vamos a ver coin un gráfico.

# Contribucion de las componentes a la variabilidad explicada de las variables
def plot_cos2_heatmap(cosenos2):
    """
    Genera un mapa de calor (heatmap) de los cuadrados de las cargas en las Componentes Principales (cosenos al cuadrado).

    Args:
        cosenos2 (pd.DataFrame): DataFrame de los cosenos al cuadrado, donde las filas representan las variables y las columnas las Componentes Principales.

    """
    # Crea una figura de tamaño 8x8 pulgadas para el gráfico
    plt.figure(figsize=(8, 8))

    # Utiliza un mapa de calor (heatmap) para visualizar 'cos2' con un solo color
    sns.heatmap(cosenos2, cmap='Blues', linewidths=0.5, annot=False)

    # Etiqueta los ejes (puedes personalizar los nombres de las filas y columnas si es necesario)
    plt.xlabel('Componentes Principales')
    plt.ylabel('Variables')

    # Establece el título del gráfico
    plt.title('Cuadrados de las Cargas en las Componentes Principales')

    # Muestra el gráfico
    plt.show()


plot_cos2_heatmap(cos2)

# ahora vamos a realizar la suma de los cosenos para ver el porcentaje completo de cada una de las asignaturas:
# Cantidad total de variabildiad explicada de una variable por el conjunto de componentes

def plot_cos2_bars(cos2):
    """
    Genera un gráfico de barras para representar la varianza explicada de cada variable utilizando los cuadrados de las cargas (cos^2).

    Args:
        cos2 (pd.DataFrame): DataFrame que contiene los cuadrados de las cargas de las variables en las componentes principales.

    Returns:
        None
    """
    # Crea una figura de tamaño 8x6 pulgadas para el gráfico
    plt.figure(figsize=(8, 6))

    # Crea un gráfico de barras para representar la varianza explicada por cada variable
    sns.barplot(x=cos2.sum(axis=1), y=cos2.index, color="blue")

    # Etiqueta los ejes
    plt.xlabel('Suma de los $cos^2$')
    plt.ylabel('Variables')

    # Establece el título del gráfico
    plt.title('Varianza Explicada de cada Variable por las Componentes Principales')

    # Muestra el gráfico
    plt.show()
    

plot_cos2_bars(cos2)

# como vemos matematicas es la que mas se ha explicado con el analisis y luego ingles la que menos

# ahora vamos con otro grafico donde se representa un vector por cada variuable usando como eje las componentes

def plot_corr_cos(n_components, correlaciones_datos_con_cp):
    """
    Genera un gráfico en el que se representa un vector por cada variable, usando como ejes las componentes, la orientación
    y la longitud del vector representa la correlación entre cada variable y dos de las componentes. El color representa el
    valor de la suma de los cosenos al cuadrado.
    
    Args:
        n_components (int): Número entero que representa el número de componentes principales seleccionadas.
        correlaciones_datos_con_cp (DataFrame): DataFrame que contiene la matriz de correlaciones entre variables y componentes
    """
    # Definir un mapa de color (cmap) sensible a las diferencias numéricas
    cmap = plt.get_cmap('coolwarm')  # Puedes ajustar el cmap según tus preferencias
    
    for i in range(n_components):
        for j in range(i + 1, n_components):  # Evitar pares duplicados
            # Calcular la suma de los cosenos al cuadrado
            sum_cos2 = correlaciones_datos_con_cp.iloc[:, i] ** 2 + correlaciones_datos_con_cp.iloc[:, j] ** 2
            
            # Crear un nuevo gráfico para cada par de componentes principales
            fig, ax = plt.subplots(figsize=(10, 10))
            
            # Dibujar un círculo de radio 1
            circle = plt.Circle((0, 0), 1, fill=False, color='b', linestyle='dotted')
            ax.add_patch(circle)
            
            # Dibujar vectores para cada variable con colores basados en la suma de los cosenos al cuadrado
            for k, var_name in enumerate(correlaciones_datos_con_cp.index):
                x = correlaciones_datos_con_cp.iloc[k, i]  # Correlación en la primera dimensión
                y = correlaciones_datos_con_cp.iloc[k, j]  # Correlación en la segunda dimensión
                
                # Seleccionar un color de acuerdo a la suma de los cosenos al cuadrado
                color = cmap(sum_cos2.iloc[k])
                
                # Dibujar el vector con el color seleccionado
                ax.quiver(0, 0, x, y, angles='xy', scale_units='xy', scale=1, color=color)
                
                # Agregar el nombre de la variable junto a la flecha con el mismo color
                ax.text(x, y, var_name, color=color, fontsize=12, ha='right', va='bottom')
            
            # Dibujar líneas discontinuas que representen los ejes
            ax.axhline(0, color='black', linestyle='--', linewidth=0.8)
            ax.axvline(0, color='black', linestyle='--', linewidth=0.8)
            
            # Etiquetar los ejes
            ax.set_xlabel(f'Componente Principal {i + 1}')
            ax.set_ylabel(f'Componente Principal {j + 1}')
            
            # Establecer los límites del gráfico
            ax.set_xlim(-1.1, 1.1)
            ax.set_ylim(-1.1, 1.1)
            
            # Agregar un mapa de color (colorbar) y su leyenda
            sm = plt.cm.ScalarMappable(cmap=cmap)
            sm.set_array([])  # Evita errores de escala
            plt.colorbar(sm, ax=ax, orientation='vertical', label='cos^2')  # Agrega la leyenda
            
            # Mostrar el gráfico
            plt.grid()
            plt.show()

plot_corr_cos(fit.n_components, correlacion_var_comp)

# aqui segun la direccion de la flkecha vemos la relacion con las disitntas componentes y segun la intensidad refleja el valor conjunto. cuanto mas intenso mas se ha explciado

# vamos a ver otro grafico ahora con las contribuciones normalizadas de cada varaible en la construccion de los copmponentes.

# adem,as lo vemos graficamente:


# Contribuciones de cada variable en la construcción de las componentes


def plot_contribuciones_proporcionales(cos2, autovalores, n_components):
    """
    Cacula las contribuciones de cada variable a las componentes principales y
    Genera un gráfico de mapa de calor con los datos
    Args:
        cos2 (DataFrame): DataFrame de los cuadrados de las cargas (cos^2).
        autovalores (array): Array de los autovalores asociados a las componentes principales.
        n_components (int): Número de componentes principales seleccionadas.
    """
    # Calcula las contribuciones multiplicando cos2 por la raíz cuadrada de los autovalores
    contribuciones = cos2 * np.sqrt(autovalores)

    # Inicializa una lista para las sumas de contribuciones
    sumas_contribuciones = []

    # Calcula la suma de las contribuciones para cada componente principal
    for i in range(n_components):
        nombre_componente = f'Componente {i + 1}'
        suma_contribucion = np.sum(contribuciones[nombre_componente])
        sumas_contribuciones.append(suma_contribucion)

    # Calcula las contribuciones proporcionales dividiendo por las sumas de contribuciones
    contribuciones_proporcionales = contribuciones.div(sumas_contribuciones, axis=1) * 100

    # Crea una figura de tamaño 8x8 pulgadas para el gráfico
    plt.figure(figsize=(8, 8))

    # Utiliza un mapa de calor (heatmap) para visualizar las contribuciones proporcionales
    sns.heatmap(contribuciones_proporcionales, cmap='Blues', linewidths=0.5, annot=False)

    # Etiqueta los ejes (puedes personalizar los nombres de las filas y columnas si es necesario)
    plt.xlabel('Componentes Principales')
    plt.ylabel('Variables')

    # Establece el título del gráfico
    plt.title('Contribuciones Proporcionales de las Variables en las Componentes Principales')

    # Muestra el gráfico
    plt.show()
    
    # Devuelve los DataFrames de contribuciones y contribuciones proporcionales
    return contribuciones_proporcionales

contribuciones_proporcionales = plot_contribuciones_proporcionales(cos2,autovalores,fit.n_components)

## aqui vemos que matematicas fisica y economia tiene unn color mas intenso en la segunda componente significando que estas son las que mayor participacion tienen en 
##la construccion de esta componente mientras que lengua historia  y literatura particpoan en la construccioin de la primera componente
## es imporntante saber que en esta gráfica vemos como se hjan construido las compoentnes y no cuanta relevancia tienen como en el coseno.

## ahora vamos a vrear gráficamente como creamos las coordenadoas de los nuevos ejes es decir, calcular la nube de puntos para las nuevas compoenntes

# Nube de puntos de las observaciones en las componentes = ejes

def plot_pca_scatter(pca, datos_estandarizados, n_components):
    """
    Genera gráficos de dispersión de observaciones en pares de componentes principales seleccionados.

    Args:
        pca (PCA): Objeto PCA previamente ajustado.
        datos_estandarizados (pd.DataFrame): DataFrame de datos estandarizados.
        n_components (int): Número de componentes principales seleccionadas.
    """
    # Representamos las observaciones en cada par de componentes seleccionadas
    componentes_principales = pca.transform(datos_estandarizados)
    
    for i in range(n_components):
        for j in range(i + 1, n_components):  # Evitar pares duplicados
            # Calcular la suma de los valores al cuadrado para cada variable
            # Crea un gráfico de dispersión de las observaciones en las dos primeras componentes principales
            plt.figure(figsize=(8, 6))  # Ajusta el tamaño de la figura si es necesario
            plt.scatter(componentes_principales[:, i], componentes_principales[:, j])
            
            # Añade etiquetas a las observaciones
            etiquetas_de_observaciones = list(datos_estandarizados.index)
    
            for k, label in enumerate(etiquetas_de_observaciones):
                plt.annotate(label, (componentes_principales[k, i], componentes_principales[k, j]))
            
            # Dibujar líneas discontinuas que representen los ejes
            plt.axhline(0, color='black', linestyle='--', linewidth=0.8)
            plt.axvline(0, color='black', linestyle='--', linewidth=0.8)
            
            # Etiquetar los ejes
            plt.xlabel(f'Componente Principal {i + 1}')
            plt.ylabel(f'Componente Principal {j + 1}')
            
            # Establece el título del gráfico
            plt.title('Gráfico de Dispersión de Observaciones en PCA')
            
            plt.show()
            
plot_pca_scatter(pca, notas_estandarizadas, fit.n_components)

# aqui estamos viendo los distintos alumnos con las distintas compoenntes. por ejjempplo el 105 y 106 nos están diciendo  que son muy de ciencias ya que tienen alto valor
# de la componente 2, mientrras que en la componente 1, tienen un valor un poco nulo, pero no muy por debajo. es decir sus notas de letras están mas o menos en la media
# mientras que en las de ciencias son mas altas

#ahora vaamos a ver la misma nuvbe de puntos con los vectores que vimos anteriormente de las asignaturas

# Nube de puntos de las observaciones en las componentes = ejes y correlaciones entre variables y componentes
def plot_pca_scatter_with_vectors(pca, datos_estandarizados, n_components, components_):
    """
    Genera gráficos de dispersión de observaciones en pares de componentes principales seleccionados
    con vectores de las correlaciones escaladas entre variables y componentes

    Args:
        pca (PCA): Objeto PCA previamente ajustado.
        datos_estandarizados (pd.DataFrame): DataFrame de datos estandarizados.
        n_components (int): Número de componentes principales seleccionadas.
        components_: Array con las componentes.
    """
    # Representamos las observaciones en cada par de componentes seleccionadas
    componentes_principales = pca.transform(datos_estandarizados)
    
    for i in range(n_components):
        for j in range(i + 1, n_components):  # Evitar pares duplicados
            # Calcular la suma de los valores al cuadrado para cada variable
            # Crea un gráfico de dispersión de las observaciones en las dos primeras componentes principales
            plt.figure(figsize=(8, 6))  # Ajusta el tamaño de la figura si es necesario
            plt.scatter(componentes_principales[:, i], componentes_principales[:, j])
            
            # Añade etiquetas a las observaciones
            etiquetas_de_observaciones = list(datos_estandarizados.index)
    
            for k, label in enumerate(etiquetas_de_observaciones):
                plt.annotate(label, (componentes_principales[k, i], componentes_principales[k, j]))
            
            # Dibujar líneas discontinuas que representen los ejes
            plt.axhline(0, color='black', linestyle='--', linewidth=0.8)
            plt.axvline(0, color='black', linestyle='--', linewidth=0.8)
            
            # Etiquetar los ejes
            plt.xlabel(f'Componente Principal {i + 1}')
            plt.ylabel(f'Componente Principal {j + 1}')
            
            # Establece el título del gráfico
            plt.title('Gráfico de Dispersión de Observaciones y variables en PCA')
            
            
            # Añadimos vectores que representen las correlaciones escaladas entre variables y componentes
            fit = pca.fit(datos_estandarizados)
            coeff = np.transpose(fit.components_)
            scaled_coeff = 8 * coeff  #8 = escalado utilizado, ajustar en función del ejemplo
            for var_idx in range(scaled_coeff.shape[0]):
                plt.arrow(0, 0, scaled_coeff[var_idx, i], scaled_coeff[var_idx, j], color='red', alpha=0.5)
                plt.text(scaled_coeff[var_idx, i], scaled_coeff[var_idx, j],
                     notas_estandarizadas.columns[var_idx], color='red', ha='center', va='center')
            
            plt.show()
            
plot_pca_scatter_with_vectors(pca, notas_estandarizadas, fit.n_components, fit.components_)

## en este grafico n os ayuda a ver emjor las correlaciones entre alumnos y asignaturas

#ahora vamos a estudair cuando añadimos individuos nuevos. recibimos una base de datos con 4 individuos nuevos:

#cargamos los individuos:
individuos_nuevos = pd.read_excel('notas_S.xlsx')
print(individuos_nuevos)

#preparamos los datos como antes:
notas_s = individuos_nuevos.set_index('Alumno', drop=True)
# Guarda la variable el indice y 'EXTRA_ESC' en un dataframe
extra_S = notas_s.iloc[:, [7]]
extra_S
# Elimina la variable 'EXTRA_ESC' del DataFrame 'notas'.
notas_S = notas_s.drop(notas_s.columns[7], axis=1)
notas_S

# Calcular la media y la desviación estándar de 'notas'
media_notas = notas.mean()
desviacion_estandar_notas = notas.std()

# Estandarizar 'notas_S' utilizando la media y la desviación estándar de 'notas'
notas_S_estandarizadas = pd.DataFrame(((notas_S - media_notas) / desviacion_estandar_notas))

notas_S_estandarizadas.columns = ['{}_z'.format(variable) for variable in variables]

# Agregar las observaciones estandarizadas a 'notas'
notas_sup = pd.concat([notas_estandarizadas, notas_S_estandarizadas])

# Calcular las componentes principales para el conjunto de datos combinado
componentes_principales_sup = pca.transform(notas_sup)

# Calcular las componentes principales para el conjunto de datos combinado
# y renombra las componentes
resultados_pca_sup = pd.DataFrame(fit.transform(notas_sup), 
                              columns=['Componente {}'.format(i) for i in range(1, fit.n_components_+1)],
                              index=notas_sup.index)


resultados_pca_sup

# Representacion observaciones + suplementarios
plot_pca_scatter(pca, notas_sup, fit.n_components)
# aqui podemos ver a los nuevos alumnos. por ejemplo el 124 podemos ver que saca buenas notas tanto en letras como en ciendas (mas ciencias que letras).

#ahroa cvamos a añadir una variable categórica nueva, en este caso la variable extraescolar como hemos quitado antes:

# Variable suplementaria
# Añadimos la variable categórica "EXTRA_ESC" en los datos
notas_componentes_sup= pd.concat([notas_sup, resultados_pca_sup], axis=1)  
extra_sup = pd.concat([extra, extra_S], axis=0)
notas_componentes_sup_extra= pd.concat([notas_componentes_sup,
                                               extra_sup], axis=1)  
print(notas_componentes_sup_extra)

# representamos los centroides con las variables:


def plot_pca_scatter_with_categories(datos_componentes_sup_var, componentes_principales_sup, n_components, var_categ):
    """
    Genera gráficos de dispersión de observaciones en pares de componentes principales seleccionados con categorías.

    Args:
        datos_componentes_sup_var (pd.DataFrame): DataFrame que contiene las categorías.
        componentes_principales_sup (np.ndarray): Matriz de componentes principales.
        n_components (int): Número de componentes principales seleccionadas.
        var_categ (str): Nombre de la variable introducida
    """
    # Obtener las categorías únicas
    categorias = datos_componentes_sup_var[var_categ].unique()

    # Iterar sobre todos los posibles pares de componentes principales
    for i in range(n_components):
        for j in range(i + 1, n_components):
            # Crear un gráfico de dispersión de las observaciones en las dos primeras componentes principales
            plt.figure(figsize=(8, 6))
            plt.scatter(componentes_principales_sup[:, i], componentes_principales_sup[:, j])

            for categoria in categorias:
                # Filtrar las observaciones por categoría
                observaciones_categoria = componentes_principales_sup[datos_componentes_sup_var[var_categ] == categoria]
                # Calcular el centroide de la categoría
                centroide = np.mean(observaciones_categoria, axis=0)
                plt.scatter(centroide[i], centroide[j], label=categoria, s=100, marker='o')

            # Añadir etiquetas a las observaciones
            etiquetas_de_observaciones = list(datos_componentes_sup_var.index)

            for k, label in enumerate(etiquetas_de_observaciones):
                plt.annotate(label, (componentes_principales_sup[k, i], componentes_principales_sup[k, j]))

            # Dibujar líneas discontinuas que representen los ejes
            plt.axhline(0, color='black', linestyle='--', linewidth=0.8)
            plt.axvline(0, color='black', linestyle='--', linewidth=0.8)

            # Etiquetar los ejes
            plt.xlabel(f'Componente Principal {i + 1}')
            plt.ylabel(f'Componente Principal {j + 1}')

            # Establecer el título del gráfico
            plt.title('Gráfico de Dispersión de Observaciones en PCA')

            # Mostrar la leyenda para las categorías
            plt.legend()
            plt.show()
plot_pca_scatter_with_categories(notas_componentes_sup_extra, componentes_principales_sup, fit.n_components, 'EXTRA_ESC')

# como podemos ver aqui el punto verde es el centroide de deporteque este puinto nos quiere decir que los que ajhcer deprote estánm un poco por debajo de la media
# de los q hacen letras y un poco por debajo en ciencias.

# los que ahcen musica esta en la media en letras y por encima en ciencias

# los que ahcen ambas están por encima de la media en ambas