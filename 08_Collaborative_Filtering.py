# -*- coding: utf-8 -*-
"""
Created on Wed May 18 18:11:01 2022

@author: marcl
"""
from surprise import KNNWithMeans
from surprise import SVD
from surprise.model_selection import GridSearchCV
import pandas as pd
from surprise import Dataset
from surprise import Reader
from scipy import spatial
import pandas as pd 

#Load the data and look at the first few rows
PATH = "C:\\Users\marcl\\Desktop\\TFG\\GITHUB TFG\\"
DATASETS_DIR = PATH + "data\\"

# =============================================================================
# Cargamos la base de datos
hotelesNorm = pd.read_pickle(DATASETS_DIR + 'HotelesNormalizados.pkl')
hoteles = pd.read_pickle(DATASETS_DIR + 'HotelesImputados.pkl')
i = 0
distancia_R = []
dist_R = 100
#crear una funcion que recoja la variable distancia 
def recomender(dist_R):
    i = 0
    while i<701:
        #append spatial.distance.euclidean(hoteles['distancia'][i], dist_R) in hoteles['Euclidean_d']
        try: 
            distancia_R.append(spatial.distance.euclidean(hoteles['distancia'][i], dist_R))
            i = i + 1
        except KeyError:
            i = i + 1
    Recomender = pd.DataFrame()            
    Recomender['Distancia_R'] = distancia_R
    Recomender['Nombre'] = hoteles['Hotel']
    #ordenar Recomender['Distancia_R'] de menor a mayor 
    Recomender = Recomender.sort_values(by=['Distancia_R'])    

