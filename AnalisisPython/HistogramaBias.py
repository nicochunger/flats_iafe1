# -*- coding: utf-8 -*-

import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt

imagen = '/home/nunger/flats_iafe1/Imagenes/MasterBias_20171123.fits'

b = fits.open(imagen)
bias = b[0].data
b.close()
bias_1d = bias.flatten()

n, bins, patches = plt.hist(bias_1d, bins=90, range=(1250, 1340))
plt.title('Cantidad de cuentas en una imagen Bias', fontsize=20)
plt.xlabel('Cantidad de cuentas por pixel', fontsize=18)
plt.ylabel('Ocurrencias', fontsize=18)
plt.show()
