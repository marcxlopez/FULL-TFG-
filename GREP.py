# -*- coding: utf-8 -*-
"""
Created on Mon May  2 14:44:09 2022

@author: marcl
"""

import pandas as pd
import numpy as np
import datetime



data = pd.read_csv('hotelesIbiza_JULAGO.csv',sep = ';')

#nos aseguramos de que omisiones no generen error 
fechaIn = pd.to_datetime(data.checkIn, format='%Y-%m-%d', errors = 'coerce')
fechaOut = pd.to_datetime(data.checkOut, format='%Y-%m-%d', errors = 'coerce')

#asignamos las dos variables de check in

day_cin = fechaIn.dt.day
month_cin = fechaIn.dt.month

#creamos las dos variables de check out 

day_cout= fechaOut.dt.day
month_cout = fechaOut.dt.month
