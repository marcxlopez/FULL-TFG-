# -*- coding: utf-8 -*-
"""
Created on Wed May 11 16:50:50 2022

@author: Marc Lopez
"""

# Cargamos las librerias necesarias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

## Librerias para los clusters
import scipy.cluster.hierarchy as shc
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score


# =============================================================================
# Parámetros del modelo: 
PATH = "E:\\DOCENCIA\\TFG Alumnos\\MARC LOPEZ\\REPOSITORIO\\"
DATASETS_DIR = PATH + "data\\"

#-----------------------------------------------------------------------
#Load the data and look at the first few rows
PATH = "C:\\Users\marcl\\Desktop\\TFG\\GITHUB TFG\\"
DATASETS_DIR = PATH + "data\\"

# =============================================================================
# Cargamos la base de datos
hotelesNorm = pd.read_pickle(DATASETS_DIR + 'HotelesNormalizados.pkl')
hoteles = pd.read_pickle(DATASETS_DIR + 'HotelesImputados.pkl')

# =============================================================================
#Let’s first draw the dendrogram to help us 
#decide the number of clusters for this particular problem

plt.figure(figsize=(10, 7))  
plt.title("Dendrograms")  
dend = shc.dendrogram(shc.linkage(hotelesNorm, method='ward'))

silluete = []
kden = range(2, 7)

for k in kden:
    print("Realizamos agrupación de k = " + str(k))
    
    # Calculamos la clasificación con el número k 
    cluster = AgglomerativeClustering(n_clusters = k, affinity = 'euclidean', 
                                      linkage = 'ward')  
    # Predecimos el número de clases
    cluster.fit_predict(hotelesNorm)

    # Gráficamos el corte del dendograma
    plt.figure(figsize=(10, 7))  
    plt.title("Dendograma para k = " + str(k))  
    dend = shc.dendrogram(shc.linkage(hotelesNorm, method = 'ward', 
                                      metric = 'euclidean'), labels = cluster.labels_)
    plt.axhline(y = 6, color = 'r', linestyle = '--')

    # Graficamos dicho corte en las variables precio vs. distnacia en la variable original
    # plt.figure(figsize = (10, 7))  
    # plt.scatter(hotelesNorm['precio'], hotelesNorm['distancia'], 
    #            c = cluster.labels_) 
    # plt.xlabel('precios')
    # plt.ylabel('distancia')
    # plt.title('Clustering Jerárquico con k =' + str(k))
    # plt.legend(range(1, k + 1))

    # Calculamos el estadístico de sillhouete para ver cual es la mejor agrupación
    silluete.append(silhouette_score(hotelesNorm, cluster.labels_, metric = 'euclidean', 
                     random_state = 0))
    
# Graficamos el estadistico de la sillhouete
plt.plot(kden, silluete, '--bo', label = 'Sillhouette')

# Seleccionamos el mejor
kOptima = kden[np.argmax(silluete)]

# Calculamos la clasificación con el número k 
cluster = AgglomerativeClustering(n_clusters = kOptima, affinity = 'euclidean', 
                                  linkage = 'ward')  
# Predecimos el número de clases
cluster.fit_predict(hotelesNorm)

# Graficamos los valores de la mejor clasificación
plt.figure(figsize = (10, 7))  
plt.scatter(hotelesNorm['precio'], hotelesNorm['distancia'], 
            c = cluster.labels_) 
plt.xlabel('precios')
plt.ylabel('distancia')
plt.title('Clustering Jerárquico con k =' + str(kOptima))
plt.legend(range(1, kOptima + 1))

# =============================================================================

        
