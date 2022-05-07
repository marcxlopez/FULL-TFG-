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

# =============================================================================
# PARAMETROS:
PATH = "E:\\DOCENCIA\\TFG Alumnos\\MARC LOPEZ\\REPOSITORIO\\"
DATASETS_DIR = PATH + "data\\"
OUTPUT_DIR = PATH + "output\\"

# =============================================================================
# Cargamos los datos que hemos scrappeado
hoteles = pd.read_pickle(DATASETS_DIR + 'HotelesIBIZA.pkl')
hoteles.columns







# -----------------------------------------------------------------------------

# =============================================================================
# Realizamos el PREPROCESSING:
### 'Hotel', 
### 'Estrellas', 
'Ratio', 
'Ratio_descr', 
'Direcciones',
           'Ammenities', 
           'Servicios_Principales', 
           'CaractFamilias',
           'lugaresInteres', 
           'Transporte', 
           'tamanyo', 
           'mascotas', 
           'internet',
           'aparcamiento', 
           'masHab', 
           'ocioInstalaciones', 
           'ocioCercanias',
           'habitaciones', 
           'coordenadas', 
           'precio'