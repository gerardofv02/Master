import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from sklearn import svm

X1 = pd.DataFrame([1, 2, 3, 5, 6 ,7])
X2= pd.DataFrame([4, 3, 5, 2, 1, 3])

X1=X1.set_axis(['X1'], axis=1)
X2=X2.set_axis(['X2'], axis=1)

X= pd.concat([X1,X2], axis=1)

y = pd.DataFrame([-1, -1, -1, 1, 1, 1])
y=y.set_axis(['y'], axis=1)

plt.scatter(X.iloc[:, 0], X.iloc[:, 1], c=np.ravel(y), s=50, cmap='autumn')
plt.show()

## Teniendo este conjunto de datos vamos a sacar los hiperplanos

## creamos el modelo y lo entrenamos
model = svm.SVC(kernel='linear', C=100)
model.fit(X, np.ravel(y))
# mostramos datos
print(X)

### Obtenemos los hiperplanos y los vectores soporte
# Get support vectors
support_vectors = model.support_vectors_
print("Vectores Soporte:\n", support_vectors)

# Get indices of support vectors
support_indices = model.support_
print("\nIndices de los vectores Soporte:\n", support_indices)

# Get number of support vectors for each class
num_support_vectors = model.n_support_
print("\nNumero de vectores soporte para cada clase:\n", num_support_vectors)

# Print the decision function
print("\nDecision Function:\n", model.decision_function)

# Get the coefficients of the hyperplane
w = model.coef_[0]
b = -w[0] / w[1]
print("\nCoeficientes del Hiperplano:\nw =", w, "\nb =", b)


### MOstramos gráficamente los hiperplanos:

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
