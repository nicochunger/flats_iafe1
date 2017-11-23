#!/usr/bin/env python

# -*- coding: utf-8 -*-
"""
Created on Sat May 16 14:22:33 2015

@author: Belen (belenareal@gmail.com) y Joel (joel.acosta@outlook.com)
@adaptacion para IAFE1: Nico (nicounger94@gmail.com)
"""
################################################################################
####								                                        ####
####								                                        ####
####	       	LECTOR DE LUZ PARA TELESCOPIO IAFE1 (Yessy)	                ####
####								                                        ####
####		        Estacion meteorologica CloudWatcher		                ####
####								                                        ####
####								                                        ####
################################################################################
""" El progrma requiere que se defina un alias para poder introducir argumentos:
ln -s Leerluz_iafe1.py Leerluz_iafe1
Al hacer esto, se puede llamar desde una consola como ./Leerluz.py n b donde n
es el numero de filtro con el que se va a medir y b es el bineo, el programa
entonces usa la curva de luz ajustada para ese filtroy bineo. """

import numpy as np
import sys
import subprocess

cuentas_max = 35000     # Numero maximo de cuentas del flat
mucha_luz = 100         # Valor de resistencia en el que consideramos que hay mucha luz como para tomar flats.
poca_luz = 12000	    # Valor de resistencia en el que consideramos que hay muy poca luz como para tomar flats.
# (Estos valores pueden modificarse sin problema, dependiendo de lo que se requiera.)
texp_max = 20	        # Tiempo de exposicion maximo que van a tener los flats.
# Esto tambien es a gusto del consumidor. En general se activa esta condicion antes que la de poca luz.

""" Estos son los valores para cada filtro y bineo de los ajustes realizados por
las curvas de luz en funcion de la resistencia, se considero un ajuste de la
forma f=a/(x-b)+c. La variable "valores" es un diccionario entre los numeros
11,12,...,(la decena es el bineo,y la unidad es el filtro) y los valores de
(a,b,c) que se van a utilizar. """

# Ajustes para el MATE
#valores = {'11':(2.904,-245,45.08), '12':(2.03,28.48,62.12), '13':(6.33,445,55.72),
#           '14':(9.08,-285,-18.34), '15':(2.98,-180,-56.19), '25':(5.6524,-440,-17.02),
#           '24':(12.46,3980,-86.63), '23':(7.1937,202,44.17), '22':(5.8980,-60,54.75),
#           '21':(5.7519,-209,64.08)}

# Ajustes para Yessy (IAFE1)
valores = {'2clear':(196.440, -8506.497, 290.096), '2u':(3.886, 184.786, 1.265),
           '2b':(27.424, -645.459, -11.508), '2v':(30.801, -793.607, 82.935),
           '2r':(39.896, -812.121, 172.621), '2i':(30.664, -838.903, 60.059)}

#Esto se encarga de agarrar los valores de filtro y bineo que se introducen al llamar al programa Leerluz.py
filtro, bineo = sys.argv[1:]

""" Aca es donde lee el valor de resistencia, esto se puede hacer de muchas
formas, en este caso el programa ofrecido por el fabricante de la estacion
metereologica guarda los valores que mide cada 10 segundos en un archivo csv,
ubicado en '/home/telescopio/CloudWatcher.csv' (esto tambien es lo mas usual).
Lo que hacemos nosotros es abrir el archivo, leer la ultima linea y todo lo que
viene abajo es para extraer de la ultima linea del archivo (que tiene todos los
valores que mide la estacion) el valor de resistencia (lo llamamos valor de luz)
que necesitamos. """

ultima = file('/home/telescopio/CloudWatcher.csv', "r").readlines()[-2]
ultima = ultima.replace('",','_')
Datos = ultima.split('_')
valor_luz = Datos[8]
valor_luz = valor_luz.replace('"','')
valor_luz = np.float(valor_luz)

#################################################
""" Otra posibiliad es leer automaticamente los datos de la estacion via el
protocolo de comunicacion correspondiente
(en nuestro caso http://www.aagware.eu/aag/cloudwatcherNetwork/TechInfo/)
que se implementaria mas o menos asi: """

# import serial
# ser=serial.Serial(port='/dev/ttyEstacion',baudrate=9600,timeout=.1)   #Abre el puerto de la estacion
# ser.write('!C')                                                       #Envia el comando para que la estacion lea la resistencia
# l=ser.readline().replace('!\x11            0','')                     #Lee lo que la estacion devuelve, y elimina el '!\x11            0' que aparece siempre en todas las lecturas
# l=l.split('!')[2].split(' ')[-1]                                      #Del string que queda, lo separa, reordean y agarra el valor que nos interesa.
#if float(l) > 1022:                                                    #Luego se convierte ese valor en resistencia, (tal como indica el link anterior)
#        l=1022                                                         #Finalmente, light es el valor de resistencia que nos importa.
#    if float(l)<1:
#        l=1
#    light=int(56/float((1023/float(l))-1))
#################################################

""" Esta funcion nos dice cuanto es el flujo medio de cuentas que esperamos
tener en las imagenes que tomemos en ese momento, con ese valor de luz , filtro y bieno. """
def flujo(x,filtro,bineo):
    a, b, c = valores[bineo+filtro]
    return a*10e5/(x-c) + b

#Calcula el tiempo de exposicion neceseraio para tener cuentas_max como valor medio de cuentas por pixel
texp = cuentas_max/flujo(valor_luz,filtro,bineo)

""" Luego decidimos que hacer con ese tiempo de exposicion. Si el valor de
resistencia es mas chico que mucha_luz (Lo que significa que hay mucha luz para
toamar flat) El programa devuelve 0. Si el tiempo de exposicion es mas grande
que el que seteamos al principio, o ya esta muy oscuro, devuelve -1. En todos
los otros casos (momentos aceptables para tomar flat) el programa redondea el
tiempo de exposicion a multiplos de 0.2 seg. Estos valores se usan en la rutina
de medicion.
Al finalizar el programa, una vez ejecutado ./Leerluz.py n b este puede devolver
3 cosas. 0 si hay mucha luz, en ese caso habra que esperar un poco, -1 si hay
poca luz, en ese caso ya no es momento para tomar flats y se continua con las
rutinas normales de observacion, y un numero entre 0.2 y 20 que debe usarse como
tiempo de exposicion en la captura de flats para que su valor medio de cuentas
por pixel sea aproximadamente cuentas_max. """

if valor_luz <= mucha_luz:
    texp = 0
elif texp > texp_max or valor_luz > poca_luz:
    texp = -1
else:
    texp = texp-np.mod(texp,0.2)
print(texp)

#################################################################
