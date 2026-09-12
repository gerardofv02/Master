## AHORA VAMOS A HACER ESTE MODELO CON UN CONJUNTO DE DATOS MAS GRANDE
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from sklearn import svm
### visualizando SVM en un caso mas general
import seaborn as sns
iris = sns.load_dataset("iris")
print(iris.head())
y = iris.species
X = iris.drop('species',axis=1)
sns.pairplot(iris, hue="species",palette="bright") ## nos quedamos solo con dos datos y clases


plt.show()


## para simplificar el problema quitamos la clase virginica y las variables sepal.
## Asi tenemos un problema de clasificacion de dos clases con dos variables que podemos visualizar


df=iris[(iris['species']!='virginica')]
df=df.drop(['sepal_length','sepal_width'], axis=1)
df.head()

sns.pairplot(df, hue="species",palette="bright")
plt.show()



#let's convert categorical values to numerical target -> transformacion de datos y cogemos los datos correctos
df=df.replace('setosa', 0)
df=df.replace('versicolor', 1)
X=df.iloc[:,0:2]  ## para coger las dos primeras columnas
V=df[['petal_length', 'petal_width']] ## otra manera de coger las dos columnas

y=df['species'].astype(int)
plt.scatter(X.iloc[:, 0], X.iloc[:, 1], c=y, s=50, cmap='autumn')
plt.scatter(df[['petal_length']], df[['petal_width']] , c=y, s=50, cmap='autumn') ## con la V
plt.show()

from sklearn.svm import SVC
model = SVC(kernel='linear', C=1) ## cogemos el kernel lineal. SI tuviesemos que escoger otro, tendriamos que ajustar mas parametros
model.fit(X, y)


support_vectors = model.support_vectors_
print("Vectores Soporte:\n", support_vectors)

support_indices = model.support_
print("\nIndices de los vectores Soporte:\n", support_indices)


num_support_vectors = model.n_support_
print("\nNumero de vectores soporte para cada clase:\n", num_support_vectors)


print("\nDecision Function:\n", model.decision_function)

# Get the coefficients of the hyperplane
w = model.coef_[0]
b = -w[0] / w[1]
print("\nCoeficientes del Hiperplano:\nw =", w, "\nb =", b)

## visualizamos el hiperplano
from sklearn.inspection import DecisionBoundaryDisplay

plt.scatter(X.iloc[:, 0], X.iloc[:, 1], c=np.ravel(y), s=50, cmap='viridis') # O 'plasma', 'inferno', 'magma', 'cividis', 'Paired', etc.

# plot the decision function
ax = plt.gca()
DecisionBoundaryDisplay.from_estimator(
    model,
    X,
    plot_method="contour",
    colors="k",
    levels=[-1, 0, 1],
    alpha=0.5,
    linestyles=["--", "-", "--"],
    ax=ax,
)
# plot support vectors
ax.scatter(
    model.support_vectors_[:, 0],
    model.support_vectors_[:, 1],
    s=100,
    linewidth=1,
    facecolors="none",
    edgecolors="k",
)
plt.show()

#######################################
########### VISUALIZACION NUMERO 2

## los pintamos para visualizarlos
plt.scatter(X.iloc[:, 0], X.iloc[:, 1], c=y, s=50, cmap='autumn')
plt.scatter(model.support_vectors_[:,0],model.support_vectors_[:,1])
### hiperplano separador

ax = plt.gca()
plt.scatter(X.iloc[:, 0], X.iloc[:, 1], c=y, s=50, cmap='autumn')
xlim = ax.get_xlim() ## limites de la variable x
ylim = ax.get_ylim() ## ## limites de la variable y

xx = np.linspace(xlim[0], xlim[1], 30) ## dividimos el espacio de la x en 30 partes iguales
yy = np.linspace(ylim[0], ylim[1], 30)
YY, XX = np.meshgrid(yy, xx)
xy = np.vstack([XX.ravel(), YY.ravel()]).T
Z = model.decision_function(xy).reshape(XX.shape)

ax.contour(XX, YY, Z, colors='k', levels=[-1, 0, 1], alpha=0.5,
           linestyles=['--', '-', '--'])

ax.scatter(model.support_vectors_[:, 0], model.support_vectors_[:, 1], s=100,
           linewidth=1, facecolors='none', edgecolors='k')
plt.show()

############### VISUALIZACION NUMERO 3
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# use seaborn plotting defaults
import seaborn as sns; sns.set()
from sklearn.datasets import make_blobs

plt.scatter(X.iloc[:, 0], X.iloc[:, 1], c=y, s=50, cmap='autumn')

### pintamos hiperplanos a mano

xfit = np.linspace(1, 6)
plt.scatter(X.iloc[:, 0], X.iloc[:, 1], c=y, s=50, cmap='autumn')
plt.plot([2.6], [0.9], 'x', color='red', markeredgewidth=2, markersize=10) # el punto que aparece con la x

#for m, b in [(1, 0.65), (0.5, 1.6), (-0.2, 2.9)]:
#    plt.plot(xfit, m * xfit + b, '-k')

plt.xlim(1, 5.5);

def plot_svc_decision_function(model, ax=None, plot_support=True):
    """Plot the decision function for a 2D SVC"""
    if ax is None:
        ax = plt.gca()
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    # create grid to evaluate model
    x = np.linspace(xlim[0], xlim[1], 30)
    y = np.linspace(ylim[0], ylim[1], 30)
    Y, X = np.meshgrid(y, x)
    xy = np.vstack([X.ravel(), Y.ravel()]).T
    P = model.decision_function(xy).reshape(X.shape)

    # plot decision boundary and margins
    ax.contour(X, Y, P, colors='k',
               levels=[-1, 0, 1], alpha=0.5,
               linestyles=['--', '-', '--'])

    # plot support vectors
    if plot_support:
        ax.scatter(model.support_vectors_[:, 0],
                   model.support_vectors_[:, 1],
                   s=300, linewidth=1, facecolors='none');
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

plt.scatter(X.iloc[:, 0], X.iloc[:, 1], c=y, s=50, cmap='autumn')
plot_svc_decision_function(model)

plt.show()

############################################################################################3
# ESTE PRIMER CASO ES CON UN CONJUNTO DE DATOS LINEALMENTE SEPARABLE
# AHORA EL SIGUIENTE CASO QUE CAMOS A VER ES CON UN CONJUNTO DE DATOS QUE NO ES LINEALMENTE SEPARABLE
############################################################################################333

from sklearn.svm import SVC
from sklearn.datasets import make_blobs
X, y = make_blobs(n_samples=100, centers=2, n_features=2, random_state=0, cluster_std=1.2)
plt.scatter(X[:, 0], X[:, 1], c=y, s=50, cmap='autumn')

clf = SVC(kernel='linear', C=0.1).fit(X, y)

plot_svc_decision_function(clf, plot_support=False)
plt.show()