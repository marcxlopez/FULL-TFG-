# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 13:01:39 2022
https://www.cienciadedatos.net/documentos/py10-regresion-lineal-python.html
@author: marcl
"""

# Tratamiento de datos
# ==============================================================================
import pandas as pd
import numpy as np


# Gráficos
# ==============================================================================
import matplotlib.pyplot as plt
from matplotlib import style
import seaborn as sns

# Preprocesado y análisis
# ==============================================================================
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
import pingouin as pg
from scipy import stats as stats 
from scipy.stats import pearsonr
from sklearn.model_selection import train_test_split
from scipy.stats import pearsonr
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm
from scipy import stats
# Configuración matplotlib
# ==============================================================================
plt.style.use('ggplot')

# Configuración warnings
# ==============================================================================
import warnings
warnings.filterwarnings('ignore')
# PARAMETROS SERGI:
#PATH = "E:\\DOCENCIA\\TFG Alumnos\\MARC LOPEZ\\REPOSITORIO\\"
#DATASETS_DIR = PATH + "data\\"
#OUTPUT_DIR = PATH + "output\\"
## PARAMETROS MARC:
PATH = "C:\\Users\marcl\\Desktop\\TFG\\GITHUB TFG\\"
DATASETS_DIR = PATH + "data\\"
hoteles = pd.read_pickle(DATASETS_DIR + 'HotelesModelos.pkl')
hoteles = hoteles.dropna(subset=['precios'], axis=0)
#X = pd.DataFrame(hoteles, columns=['Estrellas','distancia','Prox_Dalt Vila','Prox_Ses Salines',
#'Prox_Sant Antoni de Portmany',"Prox_Cala d'Hort",'Prox_Puerto de Ibiza',
#'Prox_Santa Eulária des Riu','Prox_Cala Benirrás','Prox_Sant Joan de Labritja','Prox_Cala Portinatx',
#'Prox_Sant Josep de sa Talaia','Prox_Aeropuerto de Ibiza','Prox_Cala Comte','Prox_Cala de Sant Vicent'])
##Correlacion Heatmap matriz de correlaciones
# ==============================================================================

####### Correlación lineal entre las dos variables
# ==============================================================================

corr_test = pearsonr(x =hoteles['Estrellas'], y = hoteles['precios'])
print("Coeficiente de correlación de Pearson: ", corr_test[0])
print("P-value: ", corr_test[1])
corr_test = pearsonr(x =hoteles['distancia'], y = hoteles['precios'])
print("Coeficiente de correlación de Pearson: ", corr_test[0])
print("P-value: ", corr_test[1])
corr_test = pearsonr(x =hoteles['Prox_Ses Salines'], y = hoteles['precios'])
print("Coeficiente de correlación de Pearson: ", corr_test[0]) 
print("P-value: ", corr_test[1])
#Observamos que la proximidad a Ses salines es NO ES SIGNIFICATIVA para el modelo. En cambio, la variable distancia SI lo es. 
#Variables demasiado correlacionadas

##Gráfico de NORMALIDAD 
fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(10, 4))

axs[0].hist(x=hoteles.distancia, bins=20, color="#3182bd", alpha=0.5)
axs[0].plot(hoteles.distancia, np.full_like(hoteles.distancia, -0.01), '|k', markeredgewidth=1)
axs[0].set_title('Distribución distancias')
axs[0].set_xlabel('Distancias')
axs[0].set_ylabel('counts')

axs[1].hist(x=hoteles.precios, bins=20, color="#3182bd", alpha=0.5)
axs[1].plot(hoteles.precios, np.full_like(hoteles.precios, -0.01), '|k', markeredgewidth=1)
axs[1].set_title('Distribución precio')
axs[1].set_xlabel('precio')
axs[1].set_ylabel('counts')

# Normalidad de los residuos Shapiro-Wilk test
# ==============================================================================
shapiro_test = stats.shapiro(hoteles.precios)
print(f"Variable height: {shapiro_test}")
shapiro_test = stats.shapiro(hoteles.distancia)
print(f"Variable weight: {shapiro_test}")
shapiro_test = stats.shapiro(hoteles.Estrellas)
print(f"Variable height: {shapiro_test}")
plt.tight_layout();

###############################################################################
###############################################################################
###REVISAR##
# División de los datos en train y test
# ==============================================================================
X = hoteles[['Estrellas','distancia']]
#X.to_numpy()
y = hoteles[['precios']]

X_train, X_test, y_train, y_test = train_test_split( X.values.reshape(-1,2),
                                        y.values.reshape(-1,1),
                                        
                                        train_size   = 0.8,
                                        random_state = 1234,
                                        shuffle      = True
                                    )
#X_train.values.reshape()
# Creación del modelo
# ==============================================================================
modelo = LinearRegression()
modelo.fit(X = X_train.reshape(-1,2), y = y_train) #fallo 
# Información del modelo
# ==============================================================================
print("Intercept:", modelo.intercept_)
#print("Coeficiente:", list(zip(X.columns, modelo.coef_.flatten(), )))
print("Coeficiente de determinación R^2:", modelo.score(X, y))
# Error de test del modelo 
# ==============================================================================
predicciones = modelo.predict(X = X_test)
print(predicciones[0:3,])

rmse = mean_squared_error(
        y_true  = y_test,
        y_pred  = predicciones,
        squared = False
       )
print("")
print(f"El error (rmse) de test es: {rmse}")

###############################################################################
###############################################################################
###############################################################################

# Creación del modelo utilizando matrices como en scikitlearn
# ==============================================================================
# A la matriz de predictores se le tiene que añadir una columna de 1s para el intercept del modelo
X_train = sm.add_constant(X_train, prepend=True)
modelo = sm.OLS(endog=y_train, exog=X_train,)
modelo = modelo.fit()
print(modelo.summary())

# Intervalos de confianza para los coeficientes del modelo
# ==============================================================================
modelo.conf_int(alpha=0.05)
# Predicciones con intervalo de confianza del 95%
# ==============================================================================
predicciones = modelo.get_prediction(exog = X_train).summary_frame(alpha=0.05)
predicciones.head(4)

# Predicciones con intervalo de confianza del 95%
# ==============================================================================
predicciones = modelo.get_prediction(exog = X_train).summary_frame(alpha=0.05)
predicciones['x'] = X_train[:,1]
predicciones['y'] = y_train
predicciones = predicciones.sort_values('x')

# Gráfico del modelo
# ==============================================================================
fig, ax = plt.subplots(figsize=(6, 3.84))

ax.scatter(predicciones['x'], predicciones['y'], marker='o', color = "gray")
ax.plot(predicciones['x'], predicciones["mean"], linestyle='-', label="OLS")
ax.plot(predicciones['x'], predicciones["mean_ci_lower"], linestyle='--', color='red', label="95% CI")
ax.plot(predicciones['x'], predicciones["mean_ci_upper"], linestyle='--', color='red')
ax.fill_between(predicciones['x'], predicciones["mean_ci_lower"], predicciones["mean_ci_upper"], alpha=0.1)
ax.legend();
# Error de test del modelo 
# ==============================================================================
X_test = sm.add_constant(X_test, prepend=True)
predicciones = modelo.predict(exog = X_test)
rmse = mean_squared_error(
        y_true  = y_test,
        y_pred  = predicciones,
        squared = False
       )
print("")
print(f"El error (rmse) de test es: {rmse}")

###############################################################################
# Diagnóstico errores (residuos) de las predicciones de entrenamiento
# ==============================================================================
#y_train = y_train.flatten()
prediccion_train = modelo.predict(exog = X_train)
residuos_train   = prediccion_train - y_train
#Inspección visual
# Gráficos
# ==============================================================================
fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(9, 8))

axes[0, 0].scatter(y_train, prediccion_train, edgecolors=(0, 0, 0), alpha = 0.4)
axes[0, 0].plot([y_train.min(), y_train.max()], [y_train.min(), y_train.max()],
                'k--', color = 'black', lw=2)
axes[0, 0].set_title('Valor predicho vs valor real', fontsize = 10, fontweight = "bold")
axes[0, 0].set_xlabel('Real')
axes[0, 0].set_ylabel('Predicción')
axes[0, 0].tick_params(labelsize = 7)

axes[0, 1].scatter(list(range(len(y_train))), residuos_train,
                   edgecolors=(0, 0, 0), alpha = 0.4)
axes[0, 1].axhline(y = 0, linestyle = '--', color = 'black', lw=2)
axes[0, 1].set_title('Residuos del modelo', fontsize = 10, fontweight = "bold")
axes[0, 1].set_xlabel('id')
axes[0, 1].set_ylabel('Residuo')
axes[0, 1].tick_params(labelsize = 7)

sns.histplot(
    data    = residuos_train,
    stat    = "density",
    kde     = True,
    line_kws= {'linewidth': 1},
    color   = "firebrick",
    alpha   = 0.3,
    ax      = axes[1, 0]
)

axes[1, 0].set_title('Distribución residuos del modelo', fontsize = 10,
                     fontweight = "bold")
axes[1, 0].set_xlabel("Residuo")
axes[1, 0].tick_params(labelsize = 7)


sm.qqplot(
    residuos_train,
    fit   = True,
    line  = 'q',
    ax    = axes[1, 1], 
    color = 'firebrick',
    alpha = 0.4,
    lw    = 2
)
axes[1, 1].set_title('Q-Q residuos del modelo', fontsize = 10, fontweight = "bold")
axes[1, 1].tick_params(labelsize = 7)

axes[2, 0].scatter(prediccion_train, residuos_train,
                   edgecolors=(0, 0, 0), alpha = 0.4)
axes[2, 0].axhline(y = 0, linestyle = '--', color = 'black', lw=2)
axes[2, 0].set_title('Residuos del modelo vs predicción', fontsize = 10, fontweight = "bold")
axes[2, 0].set_xlabel('Predicción')
axes[2, 0].set_ylabel('Residuo')
axes[2, 0].tick_params(labelsize = 7)

# Se eliminan los axes vacíos
fig.delaxes(axes[2,1])

fig.tight_layout()
plt.subplots_adjust(top=0.9)
fig.suptitle('Diagnóstico residuos', fontsize = 12, fontweight = "bold");

# Normalidad de los residuos Shapiro-Wilk test
# ==============================================================================
shapiro_test = stats.shapiro(residuos_train)
shapiro_test