# -*- coding: utf-8 -*-
"""
Toma una imagen .fits y la corrige por Bias y FLATS

Creado por: Nico (nicounger94@gmail.com)
"""

import numpy as np
import subprocess
from astropy.io import fits

s_imagen = 'estrellas' # Subfijo de la/s imagenes a corregir

# Directorios de entrada y salida
dir_entrada = subprocess.check_output('ls '+s_imagen+'*', shell=True).replace('\n','')
dir_salida = dir_entrada
