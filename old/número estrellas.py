# -*- coding: utf-8 -*-
"""
Created on Mon May  2 17:15:09 2022

@author: marcl
"""
import pandas as pd



data = pd.read_csv('hotelesIbiza_JULAGO.csv',sep = ';')



nestrellas = data.Estrellas.str.extract('(\d+(?:\.\d+)?)')

nRatio = data.Ratio.str.extract('(\d+(?:\.\d+)?)')



data['Estrellas'] = [re.sub(' estrella',  r'', x) for x in data['Estrellas']]
data['Estrellas'] = [re.sub('s',  r'', x) for x in data['Estrellas']]