# Programa para tomar flats de YESSY

import csv
import pprint
from datetime import datetime
import matplotlib.pyplot as plt

fecha = []
horario = []
luz = []

f = open("CloudWatcher.csv", 'r')
data = csv.reader(f)

for row in data:
    if len(row) < 20:
        continue
    else:
        fecha.append(row[0])
        horario.append(row[1])
        luz.append(row[8])

while 'Brightness Value' in luz:
    luz.remove('Brightness Value')

while 'Date' in fecha:
    fecha.remove('Date')

while 'Time' in horario:
    horario.remove('Time')
luz = [int(i) for i in luz]

fecha_hora = []
for i in range(len(horario)):
    fecha_hora.append(datetime.strptime(fecha[i]+' '+horario[i],'%Y-%m-%d %H:%M:%S'))

plt.plot(fecha_hora, luz)
plt.show()
#pprint.pprint(zip(fecha_hora, luz))
