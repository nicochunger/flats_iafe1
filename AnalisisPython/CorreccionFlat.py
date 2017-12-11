# -*- coding: utf-8 -*-
"""
Toma una imagen .fits y la corrige por Bias y FLATS

Creado por: Nico (nicounger94@gmail.com)
"""

import numpy as np
import subprocess
from astropy.io import fits
import sys

s_imagen = 'estrellas' # Subfijo de la/s imagenes a corregir

# Directorios de entrada y salida
dir_entrada = subprocess.check_output('pwd', shell=True).strip('\n')+'/'
dir_salida = dir_entrada

# Crea una lista con todas las imagenes que queres corregir
imagenes = subprocess.check_output('ls '+dir_entrada+s_imagen+'*', shell=True).replace(dir_entrada,'').split('\n')
imagenes = filter(None, imagenes) # Saca los elementos vacios

# Busca si hay MasterFLats y MasterBias. Si no hay corta el programa y tira un error.
try:
    masterbias = subprocess.check_output('ls '+dir_entrada+'MasterBias*', shell=True).replace(dir_entrada,'').strip('\n')
    masterflat = subprocess.check_output('ls '+dir_entrada+'MasterFlat*', shell=True).replace(dir_entrada,'').strip('\n')
except:
    sys.exit('No hay Flats y/o Bias presentes para usar como correccion.')

# Extrae los datos de los masterbias y masterflat
f = fits.open(masterflat)
flat = f[0].data
f.close()
b = fits.open(masterbias)
bias = b[0].data
b.close()

for imagen in imagenes:
    i = fits.open(imagen)
    img = i[0].data
    i.close()

    # Correccion por FLATS
    corregida = (img-bias)/flat
    corregida = np.rint(corregida) # Toma el valor entero de cada pixel

    fits.writeto(dir_salida+imagen.strip('.fits')+'_corregida.fits',corregida)
    print 'Se creo la imagen corregida de '+imagen
