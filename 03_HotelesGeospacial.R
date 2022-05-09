# ===========================================================
# Cargamos los paquetes necesarios
list.of.packages = c("tmap", "ggmap", "tmaptools", "sp", 
                     "sf", "ggplot2") 
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

mapaBaleares <- mapa[which(mapa$CPRO == '07'), ]
# plot(mapaBaleares)

# -----------------------------------------------------------
# Nos quedamos con la provincia de islas balerares
codigoIbiza <- c('07026', '07050', '07046', '07048', '07054', '07024')
mapaIbiza <- mapa[which(substr(mapa$CUSEC, 1, 5) %in% codigoIbiza), ]
plot(mapaIbiza)

# ===========================================================
# Convertimos los puntos de los hoteles
spHotels <- SpatialPoints(hoteles[,c("longitud", "latitud")])
# CRS(spHotels) <- "+proj=longlat +ellps=WGS84 +datum=WGS84"
HotelesSP <- SpatialPointsDataFrame(spHotels, data.frame(hoteles$Hotel))

# -----------------------------------------------------------
# Graficamos los puntos en el mapa para detectar si estan todos dentro del poligono
plot(mapaIbiza, col = "grey90")
plot(HotelesSP, pch = 20, cex = 1, col = "violetred3", add = TRUE)

# ===========================================================
# Cambiamos a formato sf
mapaSF <- st_union(st_as_sf(mapaIbiza, crs = st_crs(4326)))
puntos <- st_as_sf(HotelesSP, crs = st_crs(4326))
st_crs(puntos) <- st_crs(mapaSF)

# ===========================================================
# Grafiquem les distancies als punts
# ggplot() + 
#   geom_sf(data = st_nearest_points(puntos, mapaSF)) + 
#   geom_sf(data = mapaSF) +
#   geom_sf(data = puntos) +
#   coord_sf(xlim = c(0, 3), ylim = c(37, 40))

# ===========================================================
# Creo un cuadrado con las dimensiones para insertar dentro el mapa
## Calculo las coordenadas necesarias
xmin = floor(st_bbox(mapaSF)[1])
xmax = round(st_bbox(mapaSF)[3], 0) + 0.5
ymin = floor(st_bbox(mapaSF)[2])
ymax = round(st_bbox(mapaSF)[4], 0) + 0.5

# Genero el mapa cuadrado coincidente con la isla
mapacuadrado <- as(raster::extent(xmin, xmax, ymin, ymax), "SpatialPolygons")
proj4string(mapacuadrado) <- "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs"

## Paso de fichero sp a sf
mapacuadrado <- st_as_sf(mapacuadrado, crs = st_crs(4326))

## Calculo la diferencia entre los dos poligonos: mapaCuadrado - mapaIsla
mapaDif <- st_difference(mapacuadrado, mapaSF)
# Graficamos el mapa obtenido viendo en azul la parte que nos quedamos y en blaco 
# la parte que es vacia
plot(mapaDif, col = "blue")

# ------------------------------------------------------------------------------
# Le insertamos a los puntos el mismo CRS que el mapa calculado anteriormente
st_crs(puntos) <- st_crs(mapaDif)

# ===========================================================
# Calculamos la distancia
# distancia <- st_distance(puntos, mapaSF)
hoteles['distancia'] <- st_distance(puntos, mapaDif)
hoteles['distanciaKm'] <- hoteles$distancia/1000
# -----------------------------------------------------------
## Otra forma de encontrar la distancia al poligono:
# mapaIbizaSimple <- maptools::unionSpatialPolygons(mapaIbiza, IDs = rep(1, 74))
# apply(rgeos::gDistance(HotelesSP, mapaIbizaSimple, byid=TRUE),2,min)

# ===========================================================
# Guardamos el fichero en csv para insertarlo en el python posteriormente
hoteles <- hoteles[, c("Hotel", "distancia", "distanciaKm")]
write.csv2(hoteles, file = paste0(DATADIR, 'DistanciaHoteles.csv'), row.names = FALSE)
