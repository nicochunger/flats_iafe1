# Toma todos los datos de los flats y analiza el flujo de cuentas

import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import pprint

# Abro los archivos (tiene en cuenta distintos filtros)
filtros = ['c', 'u', 'b', 'v', 'r', 'i']
datos = {} # Diccionario que va a tener todos los datos para todos los filtros
path = 'Resultados/resultados2_sky'
for filtro in filtros:
    datos[filtro] = np.loadtxt(path+filtro,delimiter=',',usecols=(3,4,5,6),skiprows=1)

# col 0: Tiempo de exposicion
# col 1: Valor medio de cuentas
# col 2: Desviacion estandar de cuentas
# col 3: Valor de Luz

# Elimino imagenes que esten saturadas o hayan sido tomadas con muy poca luz
# Considero solo imagenes con un valor medio de cuentas menor a 55.000
# y valor de luz menor a 15.000
for filtro in filtros:
    mask = [] # Mascara que va a tener las filas a eliminar
    for idx in range(len(datos[filtro])):
        row = datos[filtro][idx,:]
        if row[1] > 55000 or row[3] > 15000:
            mask.append(idx)
    datos[filtro] = np.delete(datos[filtro], mask, 0)

# Funcion para realizar los ajustes a los datos
def func(x,a,b,c):
    return a*10e5/(x-c) + b
# Misma funcino sin el 'c'.. para probar nomas
#def func(x,a,b):
#    return (a*10e5/x) + b

ajustes = {} # Diccionario con los ajustes de cada filtro

# Hago el ajuste y grafico al mismo tiempo
plt.figure(figsize=(11.6,8.3))
plt.hold
xfit=np.linspace(0,15000,15000)
#colores = [(1.0,1.0,1.0), (0.5,0.5,0.5), (0,0,1), (0.5,0.5,0.5), (1,0,0), (0.5,0,0)]

def get_color():
    # Pone los colores para cada filtro
    # Clear: negro; Ultravioleta: violeta; Blue: azul;
    # Red: rojo; Visible: gris; Infrared: rojo oscuro
    for item in [(0,0,0), (0.5,0,0.5), (0,0,1), (0.5,0.5,0.5), (1,0,0), (0.5,0,0)]:
        yield item

colores = get_color()

for filtro in filtros:
    t_exp = datos[filtro][:,0] # Tiempo de exposicion
    mean = datos[filtro][:,1] # Valor medio de cuentas
    std = datos[filtro][:,2] # Desviacion estandar
    luz = datos[filtro][:,3] # Valor de luz
    popt, pcov = curve_fit(func, luz, mean/t_exp, p0=(100,290,0), absolute_sigma=True,sigma=std/t_exp)
    ajustes[filtro] = [popt, pcov]
    acolor = next(colores) # Color de los datos y ajuste
    plt.errorbar(luz, mean/t_exp, std/t_exp,fmt='.',color=acolor, label="Filtro "+filtro)
    plt.plot(xfit[np.ceil(popt[2]):], func(xfit[np.ceil(popt[2]):], *ajustes[filtro][0]), color=acolor)

pprint.pprint(ajustes)

plt.ylim((0,70000))
plt.xlim((0,15000))
plt.title(r'$f(x)=\frac{a10^{5}}{x-c} +b$',fontsize=22)
plt.xlabel('Valor de luz dado por el AAG',fontsize=18)
plt.ylabel('Cuentas / Segundo',fontsize=18)
plt.legend(prop={'size': 18})
plt.grid(b='on',color='grey')
plt.show()
