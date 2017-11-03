# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 18:32:04 2015

@author: belen
"""

import numpy as np
from astropy.io import fits

import subprocess


path_archivos=raw_input('Introducir directorio de los flats: ')
archivos=raw_input('Introducir nombre de los flats: ')
Luz='/home/telescopio/DATOS/DatosClima/CloudWatcher/'
b=subprocess.check_output('ls '+path_archivos+archivos,shell=True)
b=b.split('\n')


def anotar(archivo,texto,f):
    c = open(archivo, f)
    c.write(texto+'\n')
    c.close()
    

########################     Valor de Luz  ######################


def luz(Hora,Dia):
    try:
        
        a=Dia[6:8]+Dia[4:6]+'-'+Dia[0:4]
        f=open(Luz+a,'r')
        lineas=f.readlines()
        f.close()
        
        for line in lineas[1:]:
            d=float(line.split(',')[1].replace('"','').replace(':',''))
            if d >= float(Hora):
                return line.split(',')[8].replace('"','')
                break
    except:
        return '?'

##################################################################


anotar(path_archivos+'resultados_'+archivos,'Archivo,Dia,Hora,Tiempo de exp,Valor medio,Desviacion estandar, Valor luz','w')

for line in b:
    if 'fits' in line:
        line=line.replace(path_archivos,'')        
        c=fits.open(path_archivos+line)
        datos=c[0].data
        c.close()
        linea=line.split('_')
        seg=linea[3].strip('s')
        std=str(np.std(datos))
        mean= str(np.mean(datos))
        hora=linea[4][-6:]
        dia=linea[4][:8]
        datoluz=luz(hora,dia)
        anotar(path_archivos+'resultados_'+archivos,line+','+dia+','+hora+','+seg+','+mean+','+std+','+datoluz,'a')


#################################################################
