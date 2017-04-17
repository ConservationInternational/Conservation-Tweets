library(aws.s3)
library(jsonlite)
library(lubridate)
library(dplyr)

if (Sys.info()["sysname"]=='Windows'){
  setwd('D://Documents and Settings/mcooper/GitHub/Conservation-Tweets/analyze/Sentiment-Analysis/')
  
  source('../../S3_keys.R')
  
  Sys.setenv("AWS_ACCESS_KEY_ID" = key,
             "AWS_SECRET_ACCESS_KEY" = secret_key)
}else{
  aws.signature::use_credentials()
}

bucket <- get_bucket("ci-tweets-sentiment")

keys <- NULL
for (b in bucket){
  keys <- c(keys, b$Key)
}

getCoord <- function(str, coord){
  coords <- NA
  try(coords <- fromJSON(gsub('  ', ', ', gsub("'", '"', gsub("u'", "'", str))))$coordinates, silent=T)
  if (coord == 'lat'){
    return(coords[2])
  }
  if (coord == 'long'){
    return(coords[1])
  }
}

ts_df <- data.frame()
geo_df <- data.frame()
for (k in keys[2:length(keys)]){
  print(k)
  temp <- read.csv(text=rawToChar(get_object(k, bucket='ci-tweets-sentiment')), stringsAsFactors = F)
  temp$long_exact <- sapply(temp$coordinates, FUN=getCoord, coord='long')
  temp$lat_exact <- sapply(temp$coordinates, FUN=getCoord, coord='lat')
  
  temp$day <- floor_date(parse_date_time(temp$created_at, '%a %b %d! %H!:%M!:%S! %z!* %Y!'), 'day')
  
  ts_df <- bind_rows(ts_df, temp[ , c('day', 'max', 'keyword')])
  
  geo_df <- bind_rows(geo_df, temp[!is.na(temp$latitude) | !is.na(temp$lat_exact), c('latitude', 'longitude', 'lat_exact', 'long_exact', 'max', 'keyword')])
}

geo_df_exact <- geo_df %>% filter(!is.na(geo_df$lat_exact)) %>% 
  group_by(lat_exact, long_exact, keyword, max) %>%
  summarize(count=n()) %>% 
  select(latitude=lat_exact, longitude=long_exact, class=max, keyword)

geo_df_est <- geo_df %>% filter(!is.na(latitude)) %>%
  group_by(latitude, longitude, keyword, max) %>%
  summarize(count=n()) %>%
  select(latitude, longitude, keyword, count, class=max)

ts_df_sum <- ts_df %>%
  group_by(day, max, keyword) %>%
  summarize(count=n())

write.csv(ts_df_sum, 'timeseries_sentiment_climate.csv', row.names=F)
write.csv(geo_df_exact, 'spatial_sentiment_climate_exact.csv', row.names=F)
write.csv(geo_df_est, 'spatial_sentiment_climate_estimate.csv', row.names=F)