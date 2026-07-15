############################################## IMPORTS Y TRATEMIENTO DATOS ###################################################################
##############################################################################################################################################
import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from scipy.spatial import distance
import scipy.cluster.hierarchy as sch
from scipy.cluster.hierarchy import fcluster
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.metrics import silhouette_samples
from scipy.spatial.distance import pdist, squareform
import warnings
warnings.filterwarnings("ignore")
os.chdir('C:/Users/gerar/Desktop/Master/Master/Mineria de datos - PART III/Tarea/Data')

pinguinos = pd.read_excel('penguins.xlsx')
# ####print(notas)


# eliminamos las variables categoricas
island = pinguinos.iloc[:,[1]]
sex = pinguinos.iloc[:,[6]] 
species = pinguinos.iloc[:,[0]] 
print(island,'\n',sex)
eliminar = ['island','sex','species']
pinguinos = pinguinos.drop(eliminar, axis=1)
print(pinguinos)

variables = list(pinguinos.columns)
# calculamos ahora los estadisticos descriptivos
estadisticos = pd.DataFrame({
    'Mínimo': pinguinos[variables].min(),
    'Percentil 25': pinguinos[variables].quantile(0.25),
    'Mediana': pinguinos[variables].median(),
    'Percentil 75': pinguinos[variables].quantile(0.75),
    'Media': pinguinos[variables].mean(),
    'Máximo': pinguinos[variables].max(),
    'Desviación estandar': pinguinos[variables].std(),
    'Varianza': pinguinos[variables].var(),
    'Datos perdidos': pinguinos[variables].isna().sum()
})
# print(estadisticos)
## vemos q estan bien los datos
cov = pinguinos.cov()
corr = pinguinos.corr()

pinguinos_estandarizados = pd.DataFrame(
    StandardScaler().fit_transform(pinguinos),
    columns=['{}_z'.format(variable) for variable in variables],
    index=pinguinos.index
)

pca = PCA(n_components=4) # cantidad de varianbes q tentemos
fit = pca.fit(pinguinos_estandarizados) # añadimos la base de datos estandarizada ajustando el modelo


############################################## APARTADO 4 ###################################################################
var_explicada = fit.explained_variance_ratio_*100
print(var_explicada)
#############################################################################################################################

############################################## APARTADO 5 ###################################################################
# [68.63389314 19.45292928  9.21606299  2.69711459] -> sale este array con lo q para el 90% mninimo se encesitan 3 componentes (por poco)
#############################################################################################################################

############################################## APARTADO 6 ###################################################################
autovectores = pd.DataFrame(pca.components_.T,
                            columns = ['Autovector {}'.format(i) for i in range(1,fit.n_components_+1)],
                            index= ['{}_z'.format(variable) for variable in variables])
print(autovectores)
#############################################################################################################################


############################################## APARTADO 7,8 ###################################################################
pca = PCA(n_components=2) # cantidad de varianbes q tentemos
fit = pca.fit(pinguinos_estandarizados) # añadimos la base de datos estandarizada ajustando el modelo
resultados_pca = pd.DataFrame(fit.transform(pinguinos_estandarizados),
                              columns=['Componente {}'.format(i) for i in range(1,fit.n_components_+1)],
                              index= pinguinos_estandarizados.index)
pinguinos_z_cp = pd.concat([pinguinos_estandarizados,resultados_pca], axis=1)

correlacion_var_comp = pinguinos_z_cp.corr()
correlacion_var_comp = correlacion_var_comp.iloc[:fit.n_features_in_, fit.n_features_in_:]
print(correlacion_var_comp)
###############################################################################################################################

############################################## APARTADO 9 ###################################################################
cos2 = correlacion_var_comp**2
print('Apartado 9: ' ,cos2)
#############################################################################################################################

############################################## APARTADO 10 ###################################################################
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
            
plot_pca_scatter(pca, pinguinos_estandarizados, fit.n_components)

############################################## APARTADO 10 ###################################################################



############################################## APARTADO 14 ###################################################################
## METODO DEL CODO
wcss = []
    
for k in range(1, 11):  # Puedes elegir un rango diferente de valores de K
    kmeans = KMeans(n_clusters=k, random_state=0, n_init=10)
    kmeans.fit(pinguinos_estandarizados)
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

##############################################################################################################################