# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 16:03:05 2022

@author: marcl
"""

import pandas as pd
import glob
import os

# PARAMETROS MARC:
PATH = "C:\\Users\marcl\\Desktop\\TFG\\GITHUB TFG\\"
DATASETS_DIR = PATH + "data\\"
hoteles = pd.read_pickle(DATASETS_DIR + 'HotelesIBIZA.pkl')
hoteles2 = pd.read_pickle(DATASETS_DIR + 'HotelesIBIZA2.pkl')
hoteles3 = pd.read_pickle(DATASETS_DIR + 'HotelesIBIZA3.pkl')
hoteles4 = pd.read_pickle(DATASETS_DIR + 'HotelesIBIZA4.pkl')

HOTELES = [hoteles, hoteles2, hoteles3, hoteles4]
hoteles = pd.concat(HOTELES)

# Guardamos en csv los datos
#hoteles.to_csv(DATASETS_RAW_DIR + '.csv', sep = ";", decimal = ".")
hoteles.to_csv(r'C:\Users\marcl\Desktop\TFG\GITHUB TFG\data\HotelesDATA.csv', sep=";", decimal = ".")
# Guardamos en formato de pickle
hoteles.to_pickle(r'C:\Users\marcl\Desktop\TFG\GITHUB TFG\data\HotelesDATA.pkl')
