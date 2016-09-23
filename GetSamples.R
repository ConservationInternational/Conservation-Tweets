library(twitteR)
library(dplyr)

setwd('D:/Documents and Settings/mcooper/GitHub/Conservation-Tweets')

source('llaves.R')

setup_twitter_oauth(consumerKey, consumerSecret, accessToken, accessSecret)

IndWordList <- c('kebakaran hutan', 'kahutla', 'sampah', 'terumbu karang', 'pari manta', 'harimau', 'gajah', 'perubahan iklim', 'gas rumah kaca', 'hiu paus')

#Started at 1:07pm
IndResultsAll <- data.frame()
repeat{
  for (i in IndWordList){
    try({IndResults <- searchTwitter(searchString=i, n=1000, retryOnRateLimit=10, geocode='-2.755964,120.8247856,1000mi')
    IndResultsDf <- twListToDF(IndResults)})
    IndResultsDf$key <- i
    IndResultsAll <- unique(bind_rows(IndResultsAll, IndResultsDf[ , c('key', 'text', 'latitude', 'longitude')]))
    print(i)
    Sys.sleep(15)
  }
  print(paste0("We've got ", nrow(IndResultsAll), " Bahasa tweets"))
  plot(IndResultsAll$longitude, IndResultsAll$latitude)
  write.csv(IndResultsAll, 'IndResultsAll.csv', row.names=F)
}
