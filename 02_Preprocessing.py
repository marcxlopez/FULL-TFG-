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
<<<<<<< HEAD
####### Ponemos un ejemplo: Ayuntamiento de Ibiza
lugares_interes = pd.DataFrame(columns=['nombre', 'latitud', 'longitud'])

## Añadir estos valores en el data frame lugares_interes
# nombre = "Ayuntamiento"
# latitud = 38.9070794
# longitud = 1.4292239
=======
#create a data frarames de lugares de interes y distancia de hotel 
lugares_interes = pd.DataFrame(column = [ 'nombre','latitud', 'longitud'])
luga
hotel_distance = pd.DataFrame(column = ['hotel', 'nombre', 'distance'])
#i = 0 and z = 1 and t = 2 x = 0
#lat1 will be lugares_interes [i][z] and lon1 will be lugares_interes [i][t]
#lat2 will be hotelPR['latitud'][x] and lon2 will be hotelPR['longitud'][x]
i = 0
z = 1
t = 2
x = 0
R = 6373.0

distance = pd.DataFrame()
while x < len(hotelPR):
    
    lat1 = radians(lugares_interes [i][z])
    lon1 = radians(lugares_interes [i][t])
    lat2 = radians(hotelPR['latitud'][x])
    lon2 = radians(hotelPR['longitud'][x])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    i = i + 1
    #add information to hotel_distance
    hotel_distance.loc[x] = [hotelPR['hotel'][x], lugares_interes ['nombre'][i], distance]
    
  
>>>>>>> 227d9f6ddc234fcb1fe218fc8a3965669a0a661d



for j in range(0, lugares_interes.shape[0]):
    distancia = []    
    # Realizamos el bucle para todos los hoteles de la base de datos
    coordComparar = (lugares_interes.latitud[j], lugaresInteres.longitud[j])
    for i in range(0, hoteles.shape[0]):
        coords_2 = (hoteles.latitud[i], hoteles.longitud[i])
        distancia.append(geopy.distance.geodesic(coordComparar, coords_2).km)

    # Añadimos las distancias calculadas al dataframe de distancias
    hotelPR['Prox_' + lugaresInteres.nombre[j]] <- distancia

# -----------------------------------------------------------------------------
### precio
hotelPR['precio'] = [float(re.sub(" €", "", pr)) if pr != '' else float("nan") for pr in hoteles['precio']]

# =============================================================================
# Guardamos en formato de pickle
hotelPR.to_pickle(DATASETS_DIR + "HotelesPreprocesados.pkl")
hotelPR.to_csv(DATASETS_DIR + "HotelesPreprocesados.csv")

# =============================================================================


