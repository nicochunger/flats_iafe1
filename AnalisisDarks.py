# -*- coding: utf-8 -*-

import numpy as np
from astropy.io import fits
import subprocess

# Directorio actual desde donde se corre el programa
path_archivos = subprocess.check_output('pwd',shell=True).strip('\n')+'/'
archivos = 'dark' # Nombre de los flats
#Busca todos los archivos en la carpeta que se llaman dark*, los acomododa en una lista
darks = subprocess.check_output('ls '+path_archivos+archivos+'*',shell=True).replace(path_archivos,'').split('\n')

def anotar(archivo,texto,f):
    ''' Escribe texto sobre un archivo.

    (str) archivo: nombre del archivo donde se quiere escribir
    (str) texto: texto que se va a escribir
    (str) f: permiso del archivo (escritura: w, leer: r, etc) '''
    c = open(archivo, f) # Abre el archivo
    c.write(texto+'\n') # Escribe el texto sobre el archivo y crea una nueva linea
    c.close() # Cierra el archivo

anotar(path_archivos+'resultados_'+archivos,'Archivo,Tiempo de exp,Valor medio,Desviacion estandar','w')

for line in darks:
    if 'fits' in line: # Checkea que el archivo sea una imagen .fits
        line = line.replace(path_archivos,'') # Nombre del archivo
        c = fits.open(path_archivos+line) # Abre la imagen
        datos = c[0].data # Extrae los valores de cuentas de cada pixel
        c.close() # Cierra la imagen
        linea = line.split('_') # Separa el nombre del archivo en cada cosa
        seg = linea[3].strip('s') # Tiempo de exposicion
        std = str(np.std(datos)) # Desviacion estandar de las cuentas de todos los pixeles
        mean = str(np.mean(datos)) # Valor medio de las cuentas
        # Guarda los resultados
        anotar(path_archivos+'resultados_'+archivos,line+','+seg+','+mean+','+std,'a')
