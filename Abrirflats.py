
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 12:55:48 2015

@author: joel
"""

import numpy as np

#########################Metodo viejo

#sky1=np.loadtxt('1.csv',delimiter=',',usecols = (1,2,3,4),skiprows=1)	
#sky2=np.loadtxt('2.csv',delimiter=',',usecols = (1,2,3,4),skiprows=1)
#sky3=np.loadtxt('3.csv',delimiter=',',usecols = (1,2,3,4),skiprows=1)
sky4=np.loadtxt('4.csv',delimiter=',',usecols = (1,2,3,4),skiprows=1)
sky5=np.loadtxt('5.csv',delimiter=',',usecols = (1,2,3,4),skiprows=1)


#exp_1=sky1[:,0]
#val_1=sky1[:,1]
#std_1=sky1[:,2]
#luz_1=sky1[:,3]
#del sky1

#exp_2=sky2[:,0]
#val_2=sky2[:,1]
#std_2=sky2[:,2]
#luz_2=sky2[:,3]
#del sky2
#
#exp_3=sky3[:,0]
#val_3=sky3[:,1]
#std_3=sky3[:,2]
#luz_3=sky3[:,3]
#del sky3
#
exp_4=sky4[:,0]
val_4=sky4[:,1]
std_4=sky4[:,2]
luz_4=sky4[:,3]
del sky4

exp_5=sky5[:,0]
val_5=sky5[:,1]
std_5=sky5[:,2]
luz_5=sky5[:,3]
del sky5



#%%                             Ajuste las curvas
from scipy.optimize import curve_fit

def func(x,a,b,c):
    return a*10e5/(x-c) + b
#popt_1, pcov_1 = curve_fit(func,luz_1,val_1/exp_1,p0=(1,290,0.1),absolute_sigma=True,sigma=std_1/exp_1)
#popt_2, pcov_2 = curve_fit(func,luz_2,val_2/exp_2,p0=(1,290,0.1),absolute_sigma=True,sigma=std_2/exp_2)
#popt_3, pcov_3 = curve_fit(func,luz_3,val_3/exp_3,p0=(1,290,0.1),absolute_sigma=True,sigma=std_3/exp_3)
popt_4, pcov_4 = curve_fit(func,luz_4,val_4/exp_4,p0=(1,290,0.1),absolute_sigma=True,sigma=std_4/exp_4)
popt_5, pcov_5 = curve_fit(func,luz_5,val_5/exp_5,p0=(1,290,0.1),absolute_sigma=True,sigma=std_5/exp_5)

#%%                      JUNTAR FILTROS

#exp=np.concatenate((exp_1,exp_2,exp_3,exp_5))
#val=np.concatenate((val_1,val_2,val_3,val_5))
#std=np.concatenate((std_1,std_2,std_3,std_5))
#luz=np.concatenate((luz_1,luz_2,luz_3,luz_5))
#
#popt_j, pcov_j = curve_fit(func,luz,val/exp,p0=(1,290,0.1),absolute_sigma=True,sigma=std/exp)


#%% PLOT


import matplotlib.pyplot as plt
plt.figure(figsize=(11.6,8.3))
plt.hold
#
##                              Plotea los datos

#plt.errorbar(luz_1,val_1/exp_1,std_1/exp_1,fmt='.k',label='Filtro 1')
##plt.errorbar(luz_2,val_2/exp_2,std_2/exp_2,fmt='.b',label='Filtro 2')
##plt.errorbar(luz_3,val_3/exp_3,std_3/exp_3,fmt='.g',label='Filtro 3')
plt.errorbar(luz_4,val_4/exp_4,std_4/exp_4,fmt='.y',label='Filtro 4')
plt.errorbar(luz_5,val_5/exp_5,std_5/exp_5,fmt='.r',label='Filtro 5')
#plt.errorbar(luz,val/exp,std/exp,fmt='.k',label='Filtros 1,2,3,5')
#
##                                Plotea los ajustes
#
##
xfit=np.linspace(0,15000,6000)
##plt.plot(xfit,func(xfit,* popt_1),'k')
##plt.plot(xfit,func(xfit,* popt_2),'b')
##plt.plot(xfit,func(xfit,* popt_3),'g')
plt.plot(xfit,func(xfit,* popt_4),'y')
plt.plot(xfit,func(xfit,* popt_5),'r')
##plt.plot(xfit,func(xfit,* popt_1)+func(xfit,* popt_3)+func(xfit,* popt_2)+func(xfit,* popt_5),'grey',label='Suma de los ajustes de 1 2 3y 5')
#
#plt.plot(xfit,func(xfit,* popt_j), 'r')
#
##                           Plotea el texto
##plt.text(8000,12000,'a=%0.4f , b=%0.0f ,c=%0.2f' % (popt_1[0],popt_1[1],popt_1[2]),color='k')
##plt.text(8000,13000,'a=%0.4f , b=%0.0f, c=%0.2f' % (popt_2[0],popt_2[1],popt_2[2]),color='b')
##plt.text(8000,11000,'a=%0.4f , b=%0.0f ,c=%0.2f' % (popt_3[0],popt_3[1],popt_3[2]),color='g')
plt.text(8000,10000,'a=%0.4f , b=%0.0f ,c=%0.2f' % (popt_4[0],popt_4[1],popt_4[2]),color='r')
plt.text(8000,14000,'a=%0.4f , b=%0.0f, c=%0.2f' % (popt_5[0],popt_5[1],popt_5[2]),color='y')
#plt.text(8000,14000,'a=%0.4f , b=%0.0f, c=%0.2f' % (popt_j[0],popt_j[1],popt_j[2]),color='r')
#
##                                 Ajusta el grafico

plt.ylim((0,20000))
plt.xlim((0,15000))
plt.title(r'$f(x)=\frac{a10^{5}}{x-c} +b$',fontsize=18)
plt.xlabel(r'Valor de luz dado por el AAG')
plt.ylabel('Cuentas / Segundo')
plt.legend()
plt.grid(b='on',color='grey')
plt.show()


#%%                       Guarda el grafico
#plt.savefig('/home/joel/Documentos/Laboratorio/Imagenes/FiltrosI.png',dpi=380,bbox_inches='tight')