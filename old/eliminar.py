# -*- coding: utf-8 -*-
"""
Created on Thu May  5 17:50:45 2022

@author: marcl
"""

import pandas as pd


data = pd.read_csv('hotelesIbiza_JULAGO.csv',sep = ';')

#eliminamos todas las columnas no deseadas 

data.drop(['lugaresInteres', 'Transporte','entradaSalida','documentacion','mascotas','internet','aparcamiento','AmmenitiesAlojamiento','AmmenitiesHabitacion'], axis = 'columns', inplace=True)
