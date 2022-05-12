# -*- coding: utf-8 -*-
"""
Created on Thu May 12 17:31:23 2022

@author: marcl
"""

#Import libraries:
import pandas as pd
import numpy as np
import xgboost as xgb
from xgboost.sklearn import XGBClassifier
from sklearn.model_selection import train_test_split
#from sklearn import cross_validation, metrics   #Additional scklearn functions
#from sklearn.grid_search import GridSearchCV   #Perforing grid search
import matplotlib.pylab as plt
%matplotlib inline
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 12, 4


# PARAMETROS MARC:
PATH = "C:\\Users\marcl\\Desktop\\TFG\\GITHUB TFG\\"
DATASETS_DIR = PATH + "data\\"
OUTPUT_DIR = PATH + "output\\"

#cargamos base de datos
hoteles = pd.read_pickle(DATASETS_DIR + 'HotelesImputados.pkl')

#train = pd.read_csv('train_modified.csv')
#target = 'Disbursed'
#Dcol = 'ID'

#separamos Y del resto de datos  
target = hoteles['precios']
Dcol = hoteles.drop(['Hotel','ratioDescr'], axis=1)

#Divide dataset intro TRAIN and TEST 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)

#-------------------------------------------------------------------------------
def modelfit(alg, dtrain, predictors,useTrainCV=True, cv_folds=5, early_stopping_rounds=50):
    
    if useTrainCV:
        xgb_param = alg.get_xgb_params()
        xgtrain = xgb.DMatrix(dtrain[predictors].values, label=dtrain[target].values)
        cvresult = xgb.cv(xgb_param, xgtrain, num_boost_round=alg.get_params()['n_estimators'], nfold=cv_folds,
            metrics='auc', early_stopping_rounds=early_stopping_rounds, show_progress=False)
        alg.set_params(n_estimators=cvresult.shape[0])
    
    #Fit the algorithm on the data
    alg.fit(dtrain[predictors], dtrain['Disbursed'],eval_metric='auc')
        
    #Predict training set:
    dtrain_predictions = alg.predict(dtrain[predictors])
    dtrain_predprob = alg.predict_proba(dtrain[predictors])[:,1]
        
    #Print model report:
    #print("\nModel Report")
    #print("Accuracy : %.4g" + metrics.accuracy_score(dtrain['Disbursed'].values, dtrain_predictions)
    #print("AUC Score (Train): %f" + metrics.roc_auc_score(dtrain['Disbursed'], dtrain_predprob)
                    
    feat_imp = pd.Series(alg.booster().get_fscore()).sort_values(ascending=False)
    feat_imp.plot(kind='bar', title='Feature Importances')
    plt.ylabel('Feature Importance Score')
    
    
    
 #=============================================================================   
###Step 1: Fix learning rate and number of estimators for tuning tree-based parameters
#Choose all predictors except target & IDcols
predictors = [x for x in hoteles.columns if x not in [target, Dcol]]
xgb1 = XGBClassifier(
 learning_rate =0.1,
 n_estimators=1000,
 max_depth=5,
 min_child_weight=1,
 gamma=0,
 subsample=0.8,
 colsample_bytree=0.8,
 objective= 'binary:logistic',
 nthread=4,
 scale_pos_weight=1,
 seed=27)
modelfit(xgb1, hoteles, predictors)
    
    
    
