# -*- coding: utf-8 -*-
"""
Created on Fri May 13 11:36:28 2022
https://www.analyticsvidhya.com/blog/2020/09/how-dbscan-clustering-works/
@author: marcl
"""
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import matplotlib
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors

#Load the data and look at the first few rows
PATH = "C:\\Users\marcl\\Desktop\\TFG\\GITHUB TFG\\"
DATASETS_DIR = PATH + "data\\"

# =============================================================================
# Cargamos la base de datos
hotelesNorm = pd.read_pickle(DATASETS_DIR + 'HotelesNormalizados.pkl')
hoteles = pd.read_pickle(DATASETS_DIR + 'HotelesImputados.pkl')

###DBSCAN Clustering
dbscan_opt=DBSCAN(eps=10,min_samples=2)
dbscan_opt.fit(hotelesNorm)
df_DBSCAN['DBSCAN_opt_labels']=dbscan_opt.labels_
df_DBSCAN['DBSCAN_opt_labels'].value_counts()

#Nos aparecen todos los puntos como ruido
#Therefore, we need to find the value of epsilon and minPoints and then train our model again.
#For epsilon, I am using the K-distance graph. 
#For plotting a K-distance Graph,
neigh = NearestNeighbors(n_neighbors=2)
nbrs = neigh.fit(hotelesNorm)
distances, indices = nbrs.kneighbors(hotelesNorm)

#Let’s plot our K-distance graph and find the value of epsilon. Use the following syntax:
# Plotting K-distance Graph
distances = np.sort(distances, axis=0)
distances = distances[:,1]
plt.figure(figsize=(20,10))
plt.plot(distances)
plt.title('K-distance Graph',fontsize=20)
plt.xlabel('Data Points sorted by distance',fontsize=14)
plt.ylabel('Epsilon',fontsize=14)
plt.show()

dbscan_opt=DBSCAN(eps=30,min_samples=3)
dbscan_opt.fit(hotelesNorm)
hotelesNorm['DBSCAN_opt_labels']=dbscan_opt.labels_
hotelesNorm['DBSCAN_opt_labels'].value_counts()
# Plotting the resulting clusters
#plt.figure(figsize=(10,10))
#plt.scatter(df[0],df[1],c=hotelesNorm['DBSCAN_opt_labels'],cmap=matplotlib.colors.ListedColormap(colors),s=15)
#plt.title('DBSCAN Clustering',fontsize=20)
#plt.xlabel('Feature 1',fontsize=14)
#plt.ylabel('Feature 2',fontsize=14)
#plt.show()