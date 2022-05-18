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
#Load the data and look at the first few rows
PATH = "C:\\Users\marcl\\Desktop\\TFG\\GITHUB TFG\\"
DATASETS_DIR = PATH + "data\\"

# =============================================================================
# Cargamos la base de datos
hotelesNorm = pd.read_pickle(DATASETS_DIR + 'HotelesNormalizados.pkl')
hoteles = pd.read_pickle(DATASETS_DIR + 'HotelesImputados.pkl')

trainingSet = Dataset.load_from_df(hoteles, reader=Reader(name=None, line_format=u'user item rating', sep=None, rating_scale=(1, 5), skip_lines=0))

#==============================================================================
# recommender.py
# To use item-based cosine similarity
sim_options = {
    "name": "cosine", #metrica de similutd a utilizar 
    "user_based": False,  #False = basado en el item
}
algo = KNNWithMeans(sim_options=sim_options)
trainingSet = Dataset.load_from_df(hoteles, reader=Reader(name=None, line_format=u'user item rating', sep=None, rating_scale=(1, 5), skip_lines=0))
#no va
algo.fit(trainingSet)
prediction = algo.predict(hoteles['Hotel'],hoteles['distancia'])#pero no se que poner 
prediction.est

#------------------------------------------------------------------------------
###Tuning the Algorithm Parameters

##For SVD (Model based)

#data = Dataset.load_builtin("ml-100k")

param_grid = {
    "n_epochs": [5, 10],
    "lr_all": [0.002, 0.005],
    "reg_all": [0.4, 0.6]
}
gs = GridSearchCV(SVD, param_grid, measures=["rmse", "mae"], cv=3)

gs.fit(hoteles)

print(gs.best_score["rmse"])
print(gs.best_params["rmse"])
