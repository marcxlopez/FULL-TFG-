# -*- coding: utf-8 -*-
"""
Created on Thu May  5 18:00:49 2022

@author: marcl
"""

import pandas as pd
import numpy as np
data = pd.read_csv('hotelesIbiza_JULAGO.csv',sep = ';')

#
i= 1
listlist = []
tamanyo= pd.DataFrame()
while i<15:
    
    str = data.tamanyo[i]
    
    app = ([int(s) for s in str.split() if s.isdigit()])
    listlist.extend(app)
    
    i = i+1 
    
#lista de las habitaciones

nhabitaciones = []






i2 = 0
while i2<15:
    
    nhabitaciones.append(listlist[i2])
    i2= i2+2

