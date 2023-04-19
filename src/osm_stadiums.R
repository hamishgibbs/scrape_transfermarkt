suppressPackageStartupMessages({
  library(data.table)
  library(ggplot2)
  library(osmdata)
  library(sf)
})

if (interactive()){
  .args <- c(
    "data/stadiums.csv",
    "data/geo/osm_stadium_name_lookup.csv",
    "data/geo/stadiums.geojson"
  )
} else {
  .args <- commandArgs(trailingOnly = T)
}

stadiums <- fread(.args[1])
osm_name_lu <- fread(.args[2])

stadiums[osm_name_lu, on="name", osm_name := osm_name]

stadiums$key <- 'leisure'
stadiums$value <- 'stadium'

stadiums$city[which(stadiums$city == "Bournemouth")] <- "Dorset"

stadiums$key[which(stadiums$osm_name == "Turf Moor")] <- "club"
stadiums$value[which(stadiums$osm_name == "Turf Moor")] <- "sport"

stadiums_geo <- list()

for (i in 1:nrow(stadiums)) {
  
  osm_features <- opq(bbox = paste0(stadiums[i, "city"], ", UK")) %>%
    add_osm_feature(key = stadiums$key[i], value = stadiums$value[i]) %>% 
    osmdata_sf()
  
  stadium_polygon <- subset(osm_features$osm_polygons, osm_features$osm_polygons$name == stadiums$osm_name[i])
  stadium_multi_polygon <- subset(osm_features$osm_multipolygons, osm_features$osm_multipolygons$name == stadiums$osm_name[i])
  
  if (nrow(stadium_polygon)){
    stadium_geo <- stadium_polygon
  } else {
    stadium_geo <- stadium_multi_polygon
  }
  
  validation_fn <- paste0("data/geo/validation/", stadiums[i, "osm_name"], ".png")
  
  p <- ggplot() + 
    geom_sf(data=stadium_geo)
  
  ggsave(validation_fn, p, width=5, height=5, units = "in")
  
  stadium_geo <- stadium_geo[, c("osm_id", "name")]
  
  stadium_geo$team <- stadiums$team[i]
  stadium_geo$city <- stadiums$city[i]
  stadium_geo$capacity <- stadiums$capacity[i]
  stadium_geo$seats <- stadiums$seats[i]
  
  stadiums_geo[[i]] <- stadium_geo[, c("osm_id", "name", "team", "city", "capacity", "seats")]
  
}

st_write(do.call(rbind, stadiums_geo), tail(.args, 1), delete_dsn = T)

