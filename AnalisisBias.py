# Programa que analiza los Bias

import numpy as np
from astropy.io import fits
import subprocess
import matplotlib.pyplot as plt

path_archivos = subprocess.check_output('pwd',shell=True).strip('\n')+'/'
archivos = 'bias'

cuentas = []

imagenes = subprocess.check_output('ls '+path_archivos+archivos'*',shell=True).split('\n')
for img in imagenes:
    img = img.replace(path_archivos,'') # Nombre del archivo
    c = fits.open(path_archivos+img) # Abre la imagen
    datos = c[0].data # Extrae los valores de cuentas de cada pixel
    cuentas.append(datos)

hist = np.histogram(cuentas, bins=20)

plt.plot(hist)
plt.show()
