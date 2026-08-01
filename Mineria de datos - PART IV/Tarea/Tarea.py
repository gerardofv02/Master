import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency, f_oneway
import sklearn.utils.validation as validation

_original_check_array = validation.check_array

def patched_check_array(*args, **kwargs):
    if "force_all_finite" in kwargs:
        kwargs["ensure_all_finite"] = kwargs.pop("force_all_finite")
    return _original_check_array(*args, **kwargs)

validation.check_array = patched_check_array

from optbinning import Scorecard, BinningProcess, OptimalBinning
import optbinning.binning.metrics as metrics

metrics.check_array = patched_check_array
from optbinning.scorecard import plot_auc_roc, plot_cap, plot_ks, ScorecardMonitoring

import sklearn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, balanced_accuracy_score
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

from libpysal import weights
from esda.moran import Moran
from spreg import OLS, GM_Error_Het
import os
import geopandas as gpd
import matplotlib.pyplot as plt
import os
from IPython.display import display
## cargamos datos: 
os.chdir('C:/Users/gerar/Desktop/Master/Master/Mineria de datos - PART IV/Tarea/Data')
# dt=pd.read_excel('DatosPractica_Scoring.xlsx')
# print(dt)
# dt["y"]=0
# dt.loc[dt["Age"]=="good",["y"]]=0
# dt.loc[dt["Age"]=="bad", ["y"]]=1
# dt.drop(labels='Age',inplace=True, axis=1)
# dt_train, dt_test = train_test_split(dt, stratify= dt["y"], test_size=.25, random_state=1234)
# variable="age.in.years"
# X=dt_train[variable].values
# Y=dt_train['y'].values
# optb = OptimalBinning(name=variable, dtype="numerical", solver="cp")
# optb.fit(X, Y)
# optb.splits
# binning_table = optb.binning_table
# print(binning_table.build())
# df = pd.read_csv("Data_Housing_Madrid.csv")
 
# gdfm = gpd.GeoDataFrame(
#     df,
#     geometry=gpd.points_from_xy(df.longitude, df.latitude),
#     crs="EPSG:4326"
# )

# gdfm_historical = gdfm[gdfm["historical"] == 1]

# w_hy = weights.distance.DistanceBand.from_dataframe(
#     gdfm_historical,
#     threshold=0.00225,   # ≈250 metros
#     alpha=-1,            # pesos inversamente proporcionales a la distancia
#     binary=False         # no binaria
# )

# w_hy.transform = "R"
# print(gdfm.columns)
# # Cálculo del retardo espacial del precio
# gdfm_historical["PRICE_lag"] = weights.spatial_lag.lag_spatial(
#     w_hy,
#     gdfm_historical["house.price"]
# )

# moran = Moran(gdfm_historical["house.price"], w_hy)

# print("I de Moran:", round(moran.I, 3))
# print("p-valor:", round(moran.p_sim, 3))

# print("Total viviendas:", len(gdfm))


# print("Casco histórico:", len(gdfm_historical))

# print("Precio mediano:", gdfm_historical["house.price"].median())

# print("Precio máximo:", gdfm_historical["house.price"].max())
# num_vecinos = np.array(list(w_hy.cardinalities.values()))

# print("Sin vecinos:", np.sum(num_vecinos == 0))
# print("Mediana vecinos:", np.median(num_vecinos))


dt = pd.read_excel("DatosPractica_Scoring.xlsx")

# Sólo clientes aceptados
dt = dt[dt["Cardhldr"] == 1].copy()

print("Número de clientes aceptados:", len(dt))
print(dt.columns.tolist())
# Variable objetivo
y = dt["default"]

# Variables predictoras
variables = [
    "Age",
    "Income",
    "Exp_Inc",
    "Avgexp",
    "Ownrent",
    "Selfempl",
    "Depndt",
    "Inc_per",
    "Cur_add",
    "Major",
    "Active"
]

for variable in variables:

    if variable in ["Ownrent", "Selfempl"]:
        dtype = "categorical"
    else:
        dtype = "numerical"

    X = dt[variable].values

    optb = OptimalBinning(
        name=variable,
        dtype=dtype
    )

    optb.fit(X, y)

    print("\n========================")
    print(variable)
    print("========================")

    print(optb.binning_table.build())