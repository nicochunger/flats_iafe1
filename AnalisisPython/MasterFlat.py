# -*- coding: utf-8 -*-
"""
Crea MasterFlats para el telescopio IAFE1 (Yessy)

Creado Diciembre 2017
@author: Nico (nicounger94@gmail.com)
"""
import subprocess
import sys
import numpy as np
from astropy.io import fits

s_bias='bias' #Subfijo que tienen los bias
s_flat='sky'  #Subfijo que tienen los flats

#Eso da el directorio desde donde se llama al programa
dir_entrada = subprocess.check_output('pwd',shell=True).strip('\n')+'/'
dir_salida = dir_entrada

# Primero intenta de buscar imegenes flats con el subfijo indicado.
# Si no hay, corta todo y tira un mensaje de error.
try:
    # Busca todas las imagenes que empiezen con el nombre de s_flat
    flats = subprocess.check_output('ls '+dir_entrada+s_flat+'*',shell=True).replace(dir_entrada,'').split('\n')
    flats = filter(None, flats) # Saca todos los elementos vacios
    fecha = flats[0].split('_')[4][:-6] # Fecha de las imagenes
    filtros = [] # Letras que identifican a cada filtro
    # Busca que filtros se usaron
    for archivo in flats[:-1]:
        if archivo[3] not in filtros:
            filtros.append(archivo[3])
except:
    # Si no existen imagenes con ese nombre corta todo y tira un error
    sys.exit('No hay imagenes flats por analizar en '+dir_entrada)

def imcombine(imagenes, ifflat):
    ''' Funcion que combina muchas imagenes tomando las mediana de todas
    pixel a pixel. Si se trata de flats entonces ifbias=True y
    ademas las reduce por bias y las divide por el valor medio.

    (list) imagenes: lista con los nombres de las imagenes a combinar.
    (bool) reduc_bias: booleano que indica si hay que reducirlas por bias.
    '''

    img2d = [] # Lista donde voy a ir guardando los arrays de todas las fotos
    for img in imagenes:
        c = fits.open(img) # Abro la imagen
        datos = c[0].data # Extraigo los datos en forma de numpy array
        if ifflat:
            reduc_bias(datos,bias,check_bias) # Resto el Bias
            datos = datos/np.mean(datos) # Normalizo la imagen con el promedio
        img2d.append(datos) # Agrego los datos a mi lista de bias2d
        c.close() # Cierro la imagen
    img2d = tuple(img2d) # Convierto la lista a un tuple
    img3d = np.dstack(img2d) # Junto todas las imagenes en una matrix 3d
    masterimg = np.median(img3d, axis=2) # Creo el MasterBias
    return masterimg

def master_bias(dir_entrada,dir_salida):
    ''' Crea un archivo Master_Bias que es un promedio de todos los bias.

    (str) dir_entrada: directorio donde estan las imagenes bias
    (str) dir_salida: directorio donde se guarda el Master Bias '''
    try:
        haymasterbias = subprocess.check_output('ls '+dir_salida+'MasterBias*',shell=True).replace('.fits\n','')
        print 'Ya hay un MasterBias. No hace falta hacerlo devuelta.'
        return True, haymasterbias # Ya hay un MasterBias
    except: #Trata de hacer eso, si sale un error (Es que no hay imagenes), sigue para adelante
        try:
            #Busca todos los archivos en la carpeta que se llaman bias*, los acomododa en una lista
            bias = subprocess.check_output('ls '+dir_entrada+s_bias+'*',shell=True).replace(dir_entrada,'').split('\n')
            bias = filter(None, bias) # Saca todos los elementos vacios
            # Combina las imagenes buscando la mediana.
            masterbias = imcombine(bias, False)
            # Guardo el masterbias en una nueva imagen .fits
            fits.writeto(dir_salida+'MasterBias_'+fecha+'.fits',masterbias)

            print 'MasterBias creado para la fecha '+fecha+' y guardado en '+dir_salida
            return True,dir_salida+'MasterBias_'+fecha
        except:
            # Devuelve falso si no pudo crear un master bias
            return False


def reduc_bias(flat_entrada,master_bias,realizar):
    ''' Esta funcion se usa para corregir flats por bias.
    Agarra la imagen flat y le resta el masterbias. Con eso se eliminan efectos
    de corriente oscura que aparece intrisicamente del ccd.

    (np.array) flat_entrada: matriz del flat a corregir
    (str) master_bias: archivo master de los bias
    (bool) realizar: boolean que dice si hay un master bias '''

    if realizar: #Si la variable realizar es verdadera (Esa es basicamente si hay un master bias)
        b = fits.open(master_bias+'.fits') #Abro el Masterbias
        datos_bias = b[0].data # Abro los datos del Bias
        flat_entrada = flat_entrada-datos_bias # Resto el bias al flat
        b.close() # Cierro el bias


def master_flat(dir_entrada,dir_salida,filtro):
    ''' Crea un archivo Master_Flat que combina todos los flats ya reducidos por
    Bias.

    (str) dir_entrada: directorio donde estan las imagenes flat
    (str) dir_salida: directorio donde se guarda el Master Flat
    (str) filtro: letra que indica para que filtro va a ser el MasterFlat'''

    # Combina las imagenes reduciendolas por bias
    masterflat = imcombine(flats, True)

    # Guardo el masterflat en una nueva imagen .fits
    fits.writeto(dir_salida+'MasterFlat_'+filtro+'_'+fecha+'.fits',masterflat)

    print 'Master Flat creado para el filtro %s y guardado en %s' % (filtro, dir_salida)

#Crea el master bias, y los master flats
check_bias,bias = master_bias(dir_entrada,dir_salida)
for filtro in filtros:
    master_flat(dir_entrada,dir_salida,filtro)
