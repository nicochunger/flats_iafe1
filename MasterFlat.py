# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 11:42:12 2015

@author: Belén y Joel
"""
import subprocess
import numpy as np
from pyraf import iraf
from astropy.io import fits

s_bias='b' #Subfijo que tienen los bias
s_flat='sky'  #Subfijo que tienen los bias
#dir_salida='/home/belen/Escritorio/'   #En que carpeta se guardan los master bias y flats
filtros=['1','2','3','5'] #Filtros
#dir_entrada='/home/belen/Escritorio/Datos/' #En que carpeta estan los bias y sky para analizar

#Eso da el directorio desde donde se llama al programa
dir_entrada = subprocess.check_output('pwd',shell=True).strip('\n')+'/'
dir_salida = dir_entrada

def master_bias(dir_entrada,dir_salida):
    ''' Crea un archivo Master_Bias que es un promedio de todos los bias.

    (str) dir_entrada: directorio donde estan las imagenes bias
    (str) dir_salida: directorio donde se guarda el Master Bias '''
    try: #Trata de hacer eso, si sale un error (Es que no hay imagenes), sigue para adelante
        bias=subprocess.check_output('ls '+dir_entrada+s_bias+'*',shell=True).replace(dir_entrada,'').split('\n')
        #Busca todos los archivos en la carpeta que se llaman bias*, los acomododa en una lista
        archivos=','.join(x for x in bias if '.fits' in x)
        #Junta todos los datos que sean .fits de la lista. Pone comas en el medio
        fecha=bias[0].split('_')[4][:-6]
        #Lee la fecha de las imagenes
        boolean=True #Se usa despues para ver si encontro archivos o no.
    except:
        boolean=False  #Si no encontro archivos deja la variable en False
    if boolean==True:  #Si Encontro archivos crea un master bias, si no sigue para adelante
        iraf.cd(dir_entrada)
        #cambia la carpeta en la que iraf analiza cosas
        iraf.imcombine(input=archivos,output=dir_salida+'Master_Bias_'+fecha,combine='median')
        #combina las imagenes y le llama Master_Bias_fecha
        return True,dir_salida+'Master_Bias_'+fecha
        #Devuelve verdadero su pudo crear un master bias
    else:
        return False
        #Devuelve falso si no pudo crear un master bias

def reduc_bias(flat_entrada,master_bias,realizar,salida): #Esto se usa para corregir flats por bias
    ''' Esta funcion se usa para corregir flats por bias.

    (str) flat_entrada: archivo del flat a corregir
    (str) master_bias: archivo master de los bias
    (bool) realizar: boolean que dice si hay un master bias
    (str) salida: directorio y nombre de la imagen corregida '''
    if realizar is True: #Si la variable realizar es verdadera (Esa es basicamente si hay un master bias)
        iraf.imarith(flat_entrada,'-',master_bias,salida) #Le resta los bias a los flats
        iraf.imdel(flat_entrada) #Elimina la imagen de entrada



def master_flat(dir_entrada,dir_salida,filtro,check_bias,bias):
    try: #trata de hacer lo siguiente
        flat=subprocess.check_output('ls '+dir_entrada+s_flat+filtro+'*',shell=True).replace(dir_entrada,'').split('\n')
        #Se fija los archivos que son flats de cada filtro, los acomoda.
        archivos=','.join( x for x in flat if '.fits' in x )
        #Acomoda todos los flas que encuentras
        fecha=flat[1].split('_')[4][:-6]
        #Busca la fecha
        bolean=True
        #Si todo esto funciono sigue
    except:
        bolean=False
        #Si no funciono nada de esto sale
    if bolean==True:
        #cambia a la carpeta para analizar
        iraf.cd(dir_entrada)
        iraf.imcombine(input=archivos,output=dir_salida+'temp',combine='median')
        #Combina imagenes de flats
        reduc_bias(dir_salida+'temp.fits',bias,check_bias,dir_salida+'temp2')
        #Lo reduce por bias
        c=fits.open(dir_salida+'temp2.fits')
        datos=c[0].data
        c.close()
        #Busca el valor medio de la imagenes y finalmente normaliza el master flat para que tenga valor medio 1
        mean=np.mean(datos)
        iraf.cd(dir_salida)
        iraf.imarith('temp2.fits','/',mean,'Master_flat_'+filtro+'_'+fecha)
        iraf.imdel('temp2.fits')
        #Elimina la imagen temporaria
        #return 'Master Flat creado para el filtro '+filtro+' y guardado en '+dir_salida
        return 'Master Flat creado para el filtro %s y guardado en %s' % (filtro, dir_salida)
    else:
        return 'No se encuentran flats suficientes para el filtro '+filtro+' en '+dir_entrada

#Crea el master bias, y los master flats
check_bias,bias=master_bias(dir_entrada,dir_salida)
#for i in filtros:
#    master_flat(dir_entrada,dir_salida,i,check_bias,bias)
