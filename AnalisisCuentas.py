# Toma todos los datos de los flats y analiza el flujo de cuentas

import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Abrir archivos (Tener en cuenta distintos filtros)
filtros = ['c', 'u', 'b', 'v', 'r', 'i']
datos = {} # Diccionario que va a tener todos los datos para todos los filtros
path = '/home/Flats Yessy/Resultados/'
for filtro in filtros:
    datos["{}".format(filtro)] = np.loadtxt(path+'resultados_sky'+filtro+".txt",delimiter=',',usecols = (4,5,6,7),skiprows=1)

print datos["c"]



# Sacar datos relevantes de los archivos
# Tener en cuenta los limites para sacar imagenes que no sirven
# Mediana de cuentas menor a 60.000 y valor de luz menor a 15.000

# Realizar ajustes de los datos
def func(x,a,b,c):
    return a*10e5/(x-c) + b

#popt_4, pcov_4 = curve_fit(func,luz_4,val_4/exp_4,p0=(1,290,0.1),absolute_sigma=True,sigma=std_4/exp_4)

# Plotear los datos

# Plotear los ajustes
