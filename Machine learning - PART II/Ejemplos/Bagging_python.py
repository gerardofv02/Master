###### Aqui lo que vemos es lo mismo que estamos haciendo en bagging manual pero en lugar de realziarlos nosotros lo realizamos con la funcion de python

import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split

## leemos nuestra base de datos. Un dataframe clasico 
## 30 variables, +1 target  569 observaciones
 
bc = datasets.load_breast_cancer()
X = bc.data
y = bc.target

## creamos train & test 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1, stratify=y)

# aplicamos algunos modelos de ML
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression

LR=LogisticRegression(random_state=1) # regresion logistina
KNN=KNeighborsClassifier() # knn (k neighbours)

LR.fit(X_train, y_train) ## entrenando
KNN.fit(X_train, y_train) ## entrenando

#
# Model scores on test and training data
#
print('Model test Score: %.3f, ' %LR.score(X_test, y_test),
      'Model training Score: %.3f' %LR.score(X_train, y_train))

#
# Model scores on test and training data
#
print('Model test Score: %.3f, ' %KNN.score(X_test, y_test),
      'Model training Score: %.3f' %KNN.score(X_train, y_train))

## no esta nada mal .... podemos hacer un bagging? SE ve que el train es mejor que el test


# vamos a probar cpon un bagging para reducir el salto q hay y mejore el modelo

from sklearn.ensemble import BaggingClassifier

bagging_1 = BaggingClassifier(KNeighborsClassifier(), n_estimators=500,
                            max_samples=0.45, max_features=1.0, bootstrap_features=False,
                            random_state=123) ## aqui estamos poniendole 500 estimadores, la muestra (0.45), le estamos dando la opcion al algoritmo de muestrear csobre el conjunto de variables (max_features). las caracteristicas no se muestrean y luego el random
## si en el max features le ponemos un 0.8 va a salir un aespecie de random forest pero con knn. que no seria un bagging y se perderia el efecto este que se busca

#
# Fit the bagging classifier
#
bagging_1.fit(X_train, y_train)
#
# Model scores on test and training data
#
print('Model test Score: %.3f, ' %bagging_1.score(X_test, y_test),
      'Model training Score: %.3f' %bagging_1.score(X_train, y_train))

## como se puede ver lo que ha ocurrido es que tanto el test como el training tienen ahora predicciones muy parecidas

# max_samples % de la muestra que extraemos cada vez
# max_features=1.0 % numero de variables que se toman con reemplazamiento. 
# El bagging clasico toma todas, otra cosa es 
# bootstrap_features=False tomamos las variables con reemplazamiento. 

bgclassifier = BaggingClassifier(KNeighborsClassifier(), n_estimators=100,
                                 max_features=10,
                                 max_samples=100,
                                 random_state=1)
#
# Fit the bagging classifier
#
bgclassifier.fit(X_train, y_train)
#
# Model scores on test and training data
#
print('Model test Score: %.3f, ' %bgclassifier.score(X_test, y_test),
      'Model training Score: %.3f' %bgclassifier.score(X_train, y_train))


##########################################################################33
# Ahora vamos a usar unn bagging con un regresor de SVM
###########################################################################

from sklearn.svm import SVR
from sklearn.ensemble import BaggingRegressor
from sklearn.datasets import make_regression
X, y = make_regression(n_samples=100, n_features=4,
                       n_informative=2, n_targets=1,
                       random_state=0, shuffle=False)
regr = BaggingRegressor(estimator=SVR(),
                        n_estimators=10, random_state=0).fit(X, y)
regr.predict([[0, 0, 0, 0]])

# lo repetimos bien

## creamos train & test 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)

regr = BaggingRegressor(estimator=SVR(),
                        
                        n_estimators=10, random_state=0).fit(X_train, y_train) ## aqui le decimso que el estimador es el svm


regr.score(X_test, y_test)
