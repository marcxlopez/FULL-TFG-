# -*- coding: utf-8 -*-
"""
Created on Wed May 11 16:50:50 2022

@author: marcl
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

#Load the data and look at the first few rows
PATH = "C:\\Users\marcl\\Desktop\\TFG\\GITHUB TFG\\"
DATASETS_DIR = PATH + "data\\"

data = pd.read_csv(DATASETS_DIR + 'HotelesModelos.csv',sep=';')
#-----------------------------------------------------------------------
###N1. NORMALIZAR DATOS 
#crear matriz numerica 
datan = data.drop(['Hotel','ratioDescr'],axis=1) 
datanm = datan[['Plantas','habitaciones','ratioHabPlanta']]

##FILL NAN WITH MICE 

import numpy as np
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.linear_model import LinearRegression

lr = LinearRegression()
imp = IterativeImputer(estimator=lr,missing_values=np.nan, max_iter=30, verbose=2, imputation_order='roman',random_state=0)
X=imp.fit_transform(datanm)
X[:,0] = np.around(X[:,0], decimals=0)
X[:,1] = np.round(X[:,1],decimals=0)
# introducir X en datan como 'Plantas', 'habitaciones', 'ratioHabPlanta'
datan['Plantas'] = X[:,0]
datan['habitaciones'] = X[:,1]
datan['ratioHabPlanta'] = X[:,2]

#quitar los datos omitidos (RATIO)
#quitar nan en datan
datan = datan.dropna()


##NORMALIZAR DATOS 
from sklearn.preprocessing import normalize
data_scaled = normalize(datan)
data_scaled = pd.DataFrame(data_scaled, columns=datan.columns)
data_scaled.head()

corr = data_scaled.corr()

#Let’s first draw the dendrogram to help us 
#decide the number of clusters for this particular problem

import scipy.cluster.hierarchy as shc
plt.figure(figsize=(10, 7))  
plt.title("Dendrograms")  
dend = shc.dendrogram(shc.linkage(data_scaled, method='ward'))



###Ahora queremos separar dos grupos 
#así conseguiremos dos clusters
plt.figure(figsize=(10, 7))  
plt.title("Dendrograms")  
dend = shc.dendrogram(shc.linkage(data_scaled, method='ward'))
plt.axhline(y=6, color='r', linestyle='--')



#cluster jerárquico para dos grupos

from sklearn.cluster import AgglomerativeClustering
cluster = AgglomerativeClustering(n_clusters=2, affinity='euclidean', linkage='ward')  
cluster.fit_predict(data_scaled)

plt.figure(figsize=(10, 7))  
plt.scatter(data_scaled['precios'], data_scaled['distancia'], c=cluster.labels_) 

##cluster para tres grupos 

cluster = AgglomerativeClustering(n_clusters=3, affinity='euclidean', linkage='ward')  
cluster.fit_predict(data_scaled)

plt.figure(figsize=(10, 7))  
plt.scatter(data_scaled['precios'], data_scaled['distancia'], c=cluster.labels_) 
plt.xlabel('precios')
plt.ylabel('distancia')
plt.title('Hierarchical Clustering')
#cluster para cuatro grupos 

cluster = AgglomerativeClustering(n_clusters=4, affinity='euclidean', linkage='ward')  
cluster.fit_predict(data_scaled)

plt.figure(figsize=(10, 7))  
plt.scatter(data_scaled['precios'], data_scaled['distancia'], c=cluster.labels_) 
plt.xlabel('precios')
plt.ylabel('distancia')
plt.title('Hierarchical Clustering')
#cluster para cinco grupos 

cluster = AgglomerativeClustering(n_clusters=5, affinity='euclidean', linkage='ward')  
cluster.fit_predict(data_scaled)

plt.figure(figsize=(10, 7))  
plt.scatter(data_scaled['precios'], data_scaled['distancia'], c=cluster.labels_) 
#'precios' for x axis, 'distancia' for y axis
plt.xlabel('precios')
plt.ylabel('distancia')
plt.title('Hierarchical Clustering')




        
