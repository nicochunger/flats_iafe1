# -*- coding: utf-8 -*-
"""
Toma una imagen .fits y la corrige por Bias y FLATS

Creado por: Nico (nicounger94@gmail.com)
"""

import numpy as np
import subprocess
from astropy.io import fits
import sys

s_imagen = 'prueba' # Subfijo de la/s imagenes a corregir

# Directorios de entrada y salida
dir_entrada = subprocess.check_output('pwd', shell=True).strip('\n')+'/'
dir_salida = dir_entrada

imagen = subprocess.check_output('ls '+dir_entrada+s_imagen+'*', shell=True).replace(dir_entrada,'').strip('\n')
try:
    masterbias = subprocess.check_output('ls '+dir_entrada+'MasterBias*', shell=True).replace(dir_entrada,'').strip('\n')
    masterflat = subprocess.check_output('ls '+dir_entrada+'MasterFlat*', shell=True).replace(dir_entrada,'').strip('\n')
except:
    sys.exit('No hay Flats y/o Bias presentes para usar como correccion.')

f = fits.open(masterflat)
flat = f[0].data
f.close()
b = fits.open(masterbias)
bias = b[0].data
b.close()

i = fits.open(imagen)
img = i[0].data
print img
print ' '
i.close()

# Correccion por FLATS
corregida = (img-bias)/flat
corregida = np.rint(corregida)
print corregida

fits.writeto(dir_salida+imagen.strip('.fits')+'_corregida.fits',corregida)
print 'Se creo la imagen corregida de '+imagen
