## librerias necesarias a importar
import numpy as np
import pandas as pd
import os
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.api import ExponentialSmoothing,SimpleExpSmoothing,Holt
from tabulate import tabulate
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import statsmodels.api as sm
import pmdarima as pm

## una vez tenemos los imports hechos, tenemos que realizar el import y el tratamiento de los datos

directorio = 'C:/Users/gerar/Desktop/Master/Master/Mineria de datos - PART II/Tarea/Data'
os.chdir(directorio)
data = pd.read_excel('Media Temperaturas 2012-2024 Madrid.xlsx',header=None)
# print(data)
# ahora con estos datos vamos a darle formato fecha a estas dos primeras ccolumnas conviertiendolo en una única columna
meses = {
    'Enero': '01',
    'Febrero':'02',
    'Marzo':'03',
    'Abril':'04',
    'Mayo':'05',
    'Junio':'06',
    'Julio':'07',
    'Agosto':'08',
    'Septiembre':'09',
    'Octubre':'10',
    'Noviembre':'11',
    'Diciembre':'12'
}
data['Fecha'] = (data[0].astype(str) + '-' + data[1].map(meses))
# print(data)
data['Fecha'] = pd.to_datetime(data['Fecha'], format='%Y-%m')
data['Temp. Media'] = data[2]
data = data.drop([0,1,2], axis=1)
data = data.set_index('Fecha')
print(data)
