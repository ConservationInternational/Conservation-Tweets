library(twitteR)
library(dplyr)

#Sets up the directory you will work from
setwd('D:\\Documents and Settings\\mcooper\\Documents\\Conservation Tweets')

#look for a file called "keys.R", with the 4 key variables in it
source('Credentials.R')

setup_twitter_oauth(consumerKey, consumerSecret, accessToken, accessSecret)

#Create a list of words to search for
IndWordList <- c('kebakaran hutan', 'kahutla', 'sampah', 'terumbu karang', 'pari manta', 'harimau', 'gajah', 'perubahan iklim', 'gas rumah kaca', 'hiu paus', 'Orangutan')

IndResultsAll <- data.frame()
repeat{
  for (i in IndWordList){
    try({
    IndResults <- searchTwitter(searchString=' ', n=100000, retryOnRateLimit=10, lang='en')
    IndResultsDf <- twListToDF(IndResults)
    })
    IndResultsDf$key <- i
    IndResultsAll <- unique(bind_rows(IndResultsAll, IndResultsDf[ , c('key', 'text', 'latitude', 'longitude', 'created')]))
    print(i)
    Sys.sleep(15)
  }
  print(paste0("We've got ", nrow(IndResultsAll), " Bahasa tweets"))
  write.csv(IndResultsAll, 'IndResultsAll.csv', row.names=F)
}
