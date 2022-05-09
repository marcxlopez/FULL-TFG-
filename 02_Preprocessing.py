# -*- coding: utf-8 -*-
"""
Created on Sat May  7 11:57:13 2022

@author: Marc Lopez y Sergi Ramírez
"""


# =============================================================================
# Cargamos las librerias necesarias
import pandas as pd
import re
import string
from tabulate import tabulate
import geopy.distance

# from math import sin, cos, sqrt, atan2, radians
# =============================================================================
# PARAMETROS SERGI:
#PATH = "E:\\DOCENCIA\\TFG Alumnos\\MARC LOPEZ\\REPOSITORIO\\"
#DATASETS_DIR = PATH + "data\\"
#OUTPUT_DIR = PATH + "output\\"

# PARAMETROS MARC:
PATH = "C:\\Users\marcl\\Desktop\\TFG\\GITHUB TFG\\"
DATASETS_DIR = PATH + "data\\"
OUTPUT_DIR = PATH + "output\\"

# =============================================================================
# Cargamos los datos que hemos scrappeado
hoteles = pd.read_pickle(DATASETS_DIR + 'HotelesIBIZA.pkl')

# =============================================================================
# Realizamos el PREPROCESSING:
### Hotel 
hotelPR = pd.DataFrame(hoteles.Hotel)

# -----------------------------------------------------------------------------
### CheckIn
# nos aseguramos de que omisiones no generen error 
fechaIn = pd.to_datetime(data.checkIn, format='%Y-%m-%d', errors = 'coerce')
fechaOut = pd.to_datetime(data.checkOut, format='%Y-%m-%d', errors = 'coerce')

day_cin = fechaIn.dt.weekday
month_cin = fechaIn.dt.month

#creamos las dos variables de check out 

#### Calcular dia de la semana
data['LaboralEntrada'] = [meses[i] for i in month_cin]

#### Calcular el mes
data['MesEntrada'] = [days[x] for x in day_cin]

# -----------------------------------------------------------------------------
### CheckOut
day_cout = fechaOut.dt.weekday
month_cout = fechaOut.dt.month

#### Calcular dia de la semana
hotelPR['CheckOutSem'] = [days[x] for x in day_cin]

#### Calcular el mes
hotelPR['CheckOutMes'] = [meses[i] for i in month_cin]

# -----------------------------------------------------------------------------
### Estrellas
estrellas = [re.sub(" estrellas| estrella", "", estr) for estr in hoteles['Estrellas']]
hotelPR['Estrellas'] = [float(estr) if estr != '' else float("nan") for estr in estrellas ]

# -----------------------------------------------------------------------------
### Ratio 
ratio = [re.sub("\n.", "", rat) for rat in hoteles['Ratio']]
hotelPR['Ratio'] = [float(re.sub(",", "", rat)) if rat != '' else float("nan") for rat in ratio]

# -----------------------------------------------------------------------------
### Ratio_descr 
print(tabulate(pd.crosstab(index = hoteles['Ratio_descr'], columns = "count"), 
               headers = 'firstrow', tablefmt = 'fancy_grid'))
hotelPR['ratioDescr'] = hoteles['Ratio_descr']

# -----------------------------------------------------------------------------
### Direcciones
#### No lo vamos a utilizar

# -----------------------------------------------------------------------------
### Ammenities 
ammenities = [am.split("\n") for am in hoteles['Ammenities']]
df = pd.get_dummies(pd.DataFrame(ammenities))
df.columns = df.columns.str.split("_").str[-1]
df = df.groupby(df.columns.map(string.capwords), axis=1).sum()
hotelPR = pd.concat([hotelPR, df], axis = 1)

# -----------------------------------------------------------------------------
### Servicios_Principales 
# servPrincipales = [am.split("\n") for am in hoteles['Servicios_Principales']]
# df = pd.get_dummies(pd.DataFrame(servPrincipales))
# df.columns = df.columns.str.split("_").str[-1]
# df = df.groupby(df.columns.map(string.capwords), axis=1).sum()
# hotelPR = pd.concat([hotelPR, df], axis = 1)

### SR: Aquí se debería de hacer mediante match buscando aquella información que queramos escoger

# -----------------------------------------------------------------------------
### CaractFamilias
#### No lo vamos a utilizar

# -----------------------------------------------------------------------------
### lugaresInteres 
lugaresInteres = [am.split("\n") for am in hoteles['lugaresInteres']]
lugaresInteres = [am.split(":")[0] for ams in lugaresInteres for am in ams]
lugaresInteres = list(set(lugaresInteres))

### SR: En caso de que no sepas lugares de interés, aquí teemos una lista de 182: lugaresInteres

# -----------------------------------------------------------------------------
### Transporte 
#### No lo vamos a utilizar

# -----------------------------------------------------------------------------
### tamanyo 
#### plantas
plantas = [re.findall(r'[0-9]+ planta', x) for x in hoteles['tamanyo']]
plantas = [re.sub(" planta|\[|\]|\'", "", str(p)) for p in plantas]
hotelPR['Plantas'] = [int(plt) if plt != '' else float("nan") for plt in plantas]

habitaciones = [re.findall(r'[0-9]+ habita', x) for x in  hoteles['tamanyo']]
habitaciones = [re.sub(" habita|\[|\]|\'", "", str(h)) for h in habitaciones]
hotelPR['habitaciones'] = [int(hab) if hab != '' else float("nan") for hab in habitaciones]

hotelPR['ratioHabPlanta'] = hotelPR['habitaciones']/hotelPR['Plantas']
        
# -----------------------------------------------------------------------------
### mascotas 
#### SR: Por ahora no se como realizarla

# -----------------------------------------------------------------------------
### internet
#### SR: Por ahora no se como realizarla

# -----------------------------------------------------------------------------
### aparcamiento 
#### SR: Por ahora no se como realizarla

# -----------------------------------------------------------------------------
### masHab 
#### SR: Por ahora no se como realizarla

# -----------------------------------------------------------------------------
### ocioInstalaciones 
#### SR: Por ahora no se como realizarla

# -----------------------------------------------------------------------------
### ocioCercanias
#### SR: Por ahora no se como realizarla

# -----------------------------------------------------------------------------
### habitaciones 
#### SR: Por ahora no se como realizarla

# -----------------------------------------------------------------------------
### coordenadas 
hotelPR['latitud'] = [float(hot[0].split(",")[0]) for hot in hoteles['coordenadas']]
hotelPR['longitud'] = [float(hot[0].split(",")[1]) for hot in hoteles['coordenadas']]

#### Calculamos la distancia entre puntos de interes
#creamos DataFrame con los lugares de interes
nombre = ['Dalt Vila','Ses Salines',
'Sant Antoni de Portmany',"Cala d'Hort",'Puerto de Ibiza',
'Santa Eulária des Riu','Cala Benirrás','Sant Joan de Labritja','Cala Portinatx',
'Sant Josep de sa Talaia','Aeropuerto de Ibiza','Cala Comte','Cala de Sant Vicent']
latitud = [38.906613,38.5030,38.9806800,38.890,38.9089,38.9833,39.107,39.0778,39.1104253,38.9217,38.87294785,38.9634,39.0433]
longitud = [1.436293,1.2318,1.3036200,1.2235,1.43238,1.51667,1.5374,1.51227,1.5181252, 1.29344,1.370372,1.2246, 1.3524]



#crear dataframe lugares_interes con los datos de nombre, latitud y longitud
lugares_interes = pd.DataFrame({'nombre':nombre,'latitud':latitud,'longitud':longitud})


## Añadir estos valores en el data frame lugares_interes
# nombre = "Ayuntamiento"
# latitud = 38.9070794
# longitud = 1.4292239
lugares_interes = lugares_interes.append({'nombre': 'Ayuntamiento', 'latitud': 38.9070794, 'longitud': 1.4292239}, ignore_index=True)

for j in range(0, lugares_interes.shape[0]): #realizar bucle tantas veces como lugares de interes haya
    distancia = []    
    # Realizamos el bucle para todos los hoteles de la base de datos
    coordComparar = (lugares_interes.latitud[j], lugares_interes.longitud[j])
    for i in range(0, hoteles.shape[0]): #realizar bucle tantas veces como hoteles haya 
        coords_2 = (hoteles.latitud[i], hoteles.longitud[i])
        distancia.append(geopy.distance.geodesic(coordComparar, coords_2).km)

    # Añadimos las distancias calculadas al dataframe de distancias ( me falta saber que qu)
    hotelPR['Prox_' + lugaresInteres.nombre[j]] = distancia
    
# -----------------------------------------------------------------------------
### precio
hotelPR['precio'] = [float(re.sub(" €", "", pr)) if pr != '' else float("nan") for pr in hoteles['precio']]

# =============================================================================
# Guardamos en formato de pickle
hotelPR.to_pickle(DATASETS_DIR + "HotelesPreprocesados.pkl")
hotelPR.to_csv(DATASETS_DIR + "HotelesPreprocesados.csv")

# =============================================================================


