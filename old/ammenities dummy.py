# -*- coding: utf-8 -*-
"""
Created on Tue May  3 15:58:24 2022

@author: marcl"""

import pandas as pd

data = pd.read_csv('hotelesIbiza_JULAGO.csv',sep = ';')

damen = data.Ammenities



#bucle para crear lista de listas 

i = 1
amen = []


while i<39:
    amen.append(damen[i].split('\n'))
    i = i + 1 
    

#aplanar lista 
flat_list = [item for sublist in amen for item in sublist]


#quedarnos con los valores ñunicos 
unique_list = []
[unique_list.append(x) for x in flat_list if x not in unique_list]


#crear dummy 

dummy_ammenities = pd.get_dummies(unique_list)



