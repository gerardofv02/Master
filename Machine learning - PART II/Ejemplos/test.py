import pandas as pd
from sklearn.datasets import load_iris

iris_data = load_iris()

iris = pd.DataFrame(
    iris_data.data,
    columns=iris_data.feature_names
)

iris["species"] = iris["species"].map(
    dict(enumerate(iris_data.target_names))
)

print(iris.head())