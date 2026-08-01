import geopandas as gpd
import matplotlib.pyplot as plt
import os
from IPython.display import display
os.chdir('C:/Users/gerar/Desktop/Master/Master/Mineria de datos - PART IV/Tarea/Data')
# gdfm =gpd.read_file("cartografias/Munic04_ESP.shp") 
# gdfm_Madrid =gdfm[gdfm['COD_PROV']=='28']

# m = gdfm_Madrid.explore(column='PrecioIn16', 
#                   scheme='NaturalBreaks',
#                    k=9, cmap='YlOrRd',
#                 legend=False,
#                     style_kwds=dict(fillOpacity=0.8)) 

# m.save('mapa.html')


import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
from pysal.lib import weights
from pysal.explore import esda


gdfm =gpd.read_file("cartografias/Munic04_ESP.shp")

wq = weights.contiguity.Queen.from_dataframe(gdfm)
wq.transform = "R"

gdfm["TASA_PARO_lag"] = weights.spatial_lag.lag_spatial(wq, gdfm["TASA_PARO"])


f, ax = plt.subplots(1, figsize=(9, 9))
sns.regplot(
    x="TASA_PARO",
    y="TASA_PARO_lag",
    ci=None,
    data=gdfm,
    line_kws={"color": "r"})
ax.axvline(0, c="k", alpha=0.5)
ax.axhline(0, c="k", alpha=0.5)
ax.set_title("Moran Plot - Tasa de Paro")
plt.show()