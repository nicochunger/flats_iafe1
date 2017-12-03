''' Crea un grafico con el valor medio de cuentas de una imagen Dark en funcion
 del tiempo de exposicion'''

import numpy as np
import matplotlib.pyplot as plt

path = '/home/nunger/flats_iafe1/Resultados/'

darks = np.loadtxt(path+'resultados_dark', delimiter=',', usecols=(1,2,3), skiprows=1)

texp = darks[:,0]
mean = darks[:,1]
std = darks[:,2]

plt.errorbar(texp, mean, std, fmt='.')
plt.xlabel('Tiempo de exposicion (s)',fontsize=18)
plt.ylabel('Valor medio de cuentas',fontsize=18)
plt.title('Darks')
plt.grid(b='on',color='grey')
plt.show()
