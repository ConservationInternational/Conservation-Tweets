setwd('D://Documents and Settings/mcooper/GitHub/Conservation-Tweets/analyze/geo/')

library(sp)
library(rgdal)
library(raster)
library(dplyr)

load('IDN_adm2.Rdata')


dat <- list.files('data')

lang <- read.csv('../lang.csv')

ind <- NULL
for (d in dat){
  l <- lang$lang[lang$file==d]
  if (l == 'in'){
    ind <- c(ind, d)
  }
}

setwd('data')

for (f in ind){
  df <- read.csv(f, stringsAsFactors = F)

  df$latitude <- as.numeric(df$latitude)
  df$longitude <- as.numeric(df$longitude)
  
  df <- df[!is.na(df$latitude) & df$geo=='None', ]
  
  print(f)
  print(nrow(df))
  
  # if (nrow(df) > 100){
  #sp <- df[ , c('gps_longitude', 'gps_latitude')] %>% SpatialPoints
  # 
  # 
}