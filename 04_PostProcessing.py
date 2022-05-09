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

# =============================================================================
# PARAMETROS SERGI:
PATH = "E:\\DOCENCIA\\TFG Alumnos\\MARC LOPEZ\\REPOSITORIO\\"
DATASETS_DIR = PATH + "data\\"
OUTPUT_DIR = PATH + "output\\"

# PARAMETROS MARC:
# PATH = "C:\\Users\marcl\\Desktop\\TFG\\GITHUB TFG\\"
# DATASETS_DIR = PATH + "data\\"
# OUTPUT_DIR = PATH + "output\\"

# =============================================================================
# Cargamos los datos que hemos scrappeado
hoteles = pd.read_pickle(DATASETS_DIR + 'HotelesPreprocesados.pkl')

# -----------------------------------------------------------------------------
# Cargamos el csv con las distancias
distancias = pd.read_csv(DATASETS_DIR + 'DistanciaHoteles.csv', encoding="UTF-8", sep = ";")

# =============================================================================
# Unimos las bases de datos
hotelesDist = pd.merge(hoteles, distancias,  how = "left", on = 'Hotel')

# =============================================================================
# Guardamos en formato de pickle
hotelesDist.to_pickle(DATASETS_DIR + "HotelesModelos.pkl")
hotelesDist.to_csv(DATASETS_DIR + "HotelesModelos.csv")

# =============================================================================
