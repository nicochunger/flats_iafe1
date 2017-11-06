# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 18:32:04 2015

@author: belen
modificado por: nico
"""

import numpy as np
from astropy.io import fits
import subprocess


path_archivos = raw_input('Introducir directorio de los flats: ')
archivos = raw_input('Introducir nombre de los flats: ')
Luz = '/home/telescopio/FLATS/DatosClima/CloudWatcher/'
imagenes = subprocess.check_output('ls '+path_archivos+archivos,shell=True).split('\n')


def anotar(archivo,texto,f):
    ''' Escribe texto sobre un archivo.

    (str) archivo: nombre del archivo donde se quiere escribir
    (str) texto: texto que se va a escribir
    (str) f: permiso del archivo (escritura: w, leer: r, etc) '''
    c = open(archivo, f) # Abre el archivo
    c.write(texto+'\n') # Escribe el texto sobre el archivo y crea una nueva linea
    c.close() # Cierra el archivo


########################     Valor de Luz  ######################


def luz(Hora,Dia):
    ''' Extrae el valor de luz para un dia y horario especificado.

    (int) Hora: horario
    (int) Dia: fecha '''
    try:
        a = Dia[6:8] + Dia[4:6] + '-' + Dia[0:4]
        # Convierte la fecha en un formato que se pueda leer
        f = open(Luz+a,'r')
        # Abre el archivo de la estacion meteorologica de la fecha correspondiende
        lineas = f.readlines() # Lee el archivo
        f.close() # Cierra el archivo

        for line in lineas[1:]:
            hora = float(line.split(',')[1].replace('"','').replace(':',''))
            # Extre el horario de cada linea
            if hora >= float(Hora): # Compara con la hora que queremos ver
                '''Si llega a un horario que sea posterior al que queremos ver
                   extre el valor de luz lo devuelve y corta el loop. '''
                return line.split(',')[8].replace('"','')
                break
    except:
        return '?' # Si no puede leer el archivo con los datos de luz

##################################################################


anotar(path_archivos+'resultados_'+archivos,'Archivo,Dia,Hora,Tiempo de exp,Valor medio,Desviacion estandar, Valor luz','w')

for line in imagenes:
    if 'fits' in line: # Checkea que el archivo sea una imagen .fits
        line = line.replace(path_archivos,'') # Nombre del archivo
        c = fits.open(path_archivos+line) # Abre la imagen
        datos = c[0].data # Extrae los valores de cuentas de cada pixel
        c.close() # Cierra la imagen
        linea = line.split('_') # Separa el nombre del archivo en cada cosa
        seg = linea[3].strip('s') # Tiempo de exposicion
        std = str(np.std(datos)) # Desviacion estandar de las cuentas de todos los pixeles
        mean = str(np.mean(datos)) # Valor medio de las cuentas
        hora = linea[4][-6:] # Horario de la imagen
        dia = linea[4][:8] # Dia de la imagen
        datoluz = luz(hora,dia) # Valor de luz en ese momento
        # Guarda los resultados
        anotar(path_archivos+'resultados_'+archivos,line+','+dia+','+hora+','+seg+','+mean+','+std+','+datoluz,'a')


#################################################################
