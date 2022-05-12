# -*- coding: utf-8 -*-
"""
Created on Thu May 12 10:34:35 2022

@author: marcl
"""

import xgboost as xgb
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
# =============================================================================
# PARAMETROS SERGI:
#PATH = "E:\\DOCENCIA\\TFG Alumnos\\MARC LOPEZ\\REPOSITORIO\\"
#DATASETS_DIR = PATH + "data\\"
#OUTPUT_DIR = PATH + "output\\"

# PARAMETROS MARC:
PATH = "C:\\Users\marcl\\Desktop\\TFG\\GITHUB TFG\\"
DATASETS_DIR = PATH + "data\\"
OUTPUT_DIR = PATH + "output\\"

#cargamos base de datos
hoteles = pd.read_pickle(DATASETS_DIR + 'HotelesImputados.pkl')

#==============================================================================
#separamos Y del resto de datos 
y = hoteles['precios']
X = hoteles.drop(['Hotel','ratioDescr'], axis=1)

#convert the dataset into an optimized data structure called Dmatrix
#  that XGBoost supports 
data_dmatrix = xgb.DMatrix(data=X,label=y)

#Divide dataset intro TRAIN and TEST 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)

###Regresor XGBOOST------------------------------------------------
xg_reg = xgb.XGBRegressor(objective ='reg:linear', colsample_bytree = 0.3, learning_rate = 0.1,
                max_depth = 5, alpha = 10, n_estimators = 10)

#Fit the regressor to the training set and make predictions on the test set
xg_reg.fit(X_train,y_train)
preds = xg_reg.predict(X_test)

#Compute the rmse by invoking the mean_sqaured_error function
rmse = np.sqrt(mean_squared_error(y_test, preds))
print("RMSE: %f" % (rmse))


#==============================================================================

###k-fold Cross Validation using XGBoost
#to build more robust models, it is common to do a k-fold cross validation
# where all the entries in the original training dataset are used for both training as well as validation
params = {"objective":"reg:linear",'colsample_bytree': 0.3,'learning_rate': 0.1,
                'max_depth': 5, 'alpha': 10}

cv_results = xgb.cv(dtrain=data_dmatrix, params=params, nfold=3,
                    num_boost_round=50,early_stopping_rounds=10,metrics="rmse", as_pandas=True, seed=123)

print((cv_results["test-rmse-mean"]).tail(1))

#==============================================================================
###Visualize Boosting Trees and Feature Importance
xg_reg = xgb.train(params=params, dtrain=data_dmatrix, num_boost_round=10)

#Plotting the first tree
#xgb.plot_tree(xg_reg,num_trees=0)
#plt.rcParams['figure.figsize'] = [50, 10]
#plt.show()
#module 'graphviz.backend' has no attribute 'ENCODING'


###examine the importance of each feature column in the original dataset
xgb.plot_importance(xg_reg)
plt.rcParams['figure.figsize'] = [5, 5]
plt.show()