# -*- coding: utf-8 -*-
"""
Created on Mon May  9 15:32:47 2022

@author: User
"""

# =============================================================================
# Cargamos las librerias necesarias
import pandas as pd
import re
import string
from tabulate import tabulate
import geopy.distance

# from math import sin, cos, sqrt, atan2, radians

# Cargamos las librerias necesarias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

## Librerias necesarias para la imputación de valores faltantes
import numpy as np
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.linear_model import LinearRegression

## Librerias para la normalización de los datos
from sklearn.preprocessing import normalize

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
hoteles = pd.read_pickle(DATASETS_DIR + 'HotelesPreprocesados.pkl')
hoteles = hoteles.dropna(subset=['precios'], axis=0)
# -----------------------------------------------------------------------------
# Cargamos el csv con las distancias
distancias = pd.read_csv(DATASETS_DIR + 'DistanciaHoteles.csv', encoding="UTF-8", sep = ";")

# =============================================================================
# Unimos las bases de datos
hotelesDist = pd.merge(hoteles, distancias,  how = "left", on = 'Hotel')

# =============================================================================
# Guardamos en formato de pickle
hotelesDist.to_pickle(DATASETS_DIR + "HotelesModelos.pkl")
hotelesDist.to_csv(DATASETS_DIR + "HotelesModelos.csv",sep=';')

# =============================================================================
### N1. NORMALIZAR DATOS 
# crear matriz numerica 
datan = hotelesDist.drop(['Hotel','ratioDescr'], axis = 1) 
# Base de datos que debemos de imputar
datanm = datan[['Plantas','habitaciones']]

#-----------------------------------------------------------------------
# Creamos el estimador lineal
lr = LinearRegression()
imp = IterativeImputer(estimator = lr, missing_values = np.nan, 
                       max_iter = 30, verbose = 2, 
                       imputation_order = 'roman', random_state = 0)
X = imp.fit_transform(datanm)
X[:, 0] = np.around(X[:, 0], decimals = 0)
X[:, 1] = np.round(X[:, 1], decimals = 0)

#-----------------------------------------------------------------------
# introducir X en datan como 'Plantas', 'habitaciones', 'ratioHabPlanta'
datan['Plantas'] = X[:, 0]
datan['habitaciones'] = X[:, 1]
datan['ratioHabPlanta'] = datan['habitaciones']/datan['Plantas']

#quitar los datos omitidos (RATIO)
#quitar nan en datan
datan = datan.dropna()

# =============================================================================
# Añadimos las dos variables faltantes a nuestro datan
datan['Hotel'] = hoteles['Hotel']
datan['ratioDescr'] = hoteles['ratioDescr']

# =============================================================================
# Guardamos en formato de pickle la base de datos 
datan.to_pickle(DATASETS_DIR + "HotelesImputados.pkl")
datan.to_csv(DATASETS_DIR + "HotelesImputados.csv",";")

# =============================================================================
## NORMALIZAR DATOS 
data_scaled = datan.drop(['Hotel','ratioDescr'], axis = 1) 
columnas = data_scaled.columns
data_scaled = normalize(data_scaled)
data_scaled = pd.DataFrame(data_scaled, columns = columnas)
data_scaled.head()

## Calculamos la correlación de los datos
corr = data_scaled.corr()

# =============================================================================
# Guardamos la base de datos normalizada
data_scaled.to_pickle(DATASETS_DIR + "HotelesNormalizados.pkl")
data_scaled.to_csv(DATASETS_DIR + "HotelesNormalizados.csv", ";")

# =============================================================================


