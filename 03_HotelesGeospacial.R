# ===========================================================
# Cargamos los paquetes necesarios
list.of.packages = c("tmap", "ggmap", "tmaptools", "sp", 
                     "sf", "ggplot2", "redlistr") 
new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if(length(new.packages) > 0) {
  install.packages(new.packages)
}
lapply(list.of.packages, require, character.only = T)
rm(list.of.packages, new.packages)

# ===========================================================
# Parámetros necesarios
DATADIR <- 'E:/DOCENCIA/TFG Alumnos/MARC LOPEZ/REPOSITORIO/data/'
SHAPEFILEDIR <- 'E:/DOCENCIA/TFG Alumnos/MARC LOPEZ/REPOSITORIO/input/seccionado_2022/España_Seccionado2022_ETRS89H30/'

# ===========================================================
# Cargamos la base de datos
hoteles <- read.csv(paste0(DATADIR, 'HotelesPreprocesados.csv'))

# ===========================================================
# Cargamos el mapa de secciones censales
fichero_mapa <- paste0(SHAPEFILEDIR, "SECC_CE_20220101.shp")
mapa <- rgdal::readOGR(paste0(fichero_mapa))
mapa <- spTransform(mapa, CRS("+proj=longlat +ellps=WGS84 +datum=WGS84"))

# -----------------------------------------------------------
# Nos quedamos con la provincia de islas balerares
codigoIbiza <- c('07026', '07050', '07046', '07048', '07054')
mapaIbiza <- mapa[which(substr(mapa$CUSEC, 1, 5) %in% codigoIbiza), ]
plot(mapaIbiza)

# ===========================================================
# Convertimos los puntos de los hoteles
spHotels <- SpatialPoints(hoteles[,c("longitud", "latitud")])
CRS(spHotels) <- "+proj=longlat +ellps=WGS84 +datum=WGS84"
HotelesSP <- SpatialPointsDataFrame(spHotels, data.frame(hoteles$Hotel))

# -----------------------------------------------------------
# Graficamos los puntos en el mapa para detectar si estan todos dentro del poligono
plot(mapaIbiza, col = "grey90")
plot(HotelesSP, pch = 20, cex = 1, col = "violetred3", add = TRUE)

# ===========================================================
# Calculamos la distancia
mapaSF <- st_union(st_as_sf(mapaIbiza, crs = st_crs(4326)))
puntos <- st_as_sf(HotelesSP, crs = st_crs(4326))
st_crs(puntos) <- st_crs(mapaSF)
distancia <- st_distance(puntos, mapaSF)
distanciaKm <- distancia/1000

# -----------------------------------------------------------
## Otra forma de encontrar la distancia al poligono:
# mapaIbizaSimple <- maptools::unionSpatialPolygons(mapaIbiza, IDs = rep(1, 74))
# apply(rgeos::gDistance(HotelesSP, mapaIbizaSimple, byid=TRUE),2,min)

# ===========================================================
# Grafiquem les distnacies als punts
ggplot() + 
  geom_sf(data = st_nearest_points(puntos, mapaSF)) + 
  geom_sf(data = mapaSF) +
  geom_sf(data = puntos) +
  coord_sf(xlim = c(0, 3), ylim = c(37, 40))


eoo.A <- mapaIbiza %>% makeEOO()


