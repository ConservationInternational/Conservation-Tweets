setwd('D:/Documents and Settings/mcooper/Documents/Conservation Tweets/Sample Data')

files <- list.files()

t <- files[1]

out <- read.csv(t)

f <- readLines(t)

#START including uuids in tweets
#START removing \n from tweets

#etymology of the word handle?
#Hand in swahili?

readCSV <- function(t){
  f <- readLines(t)
  header <- strsplit(f[1], ',')[[1]]
  commaCounts <- sapply(f[2:length(f)], FUN=commaCount)
  
}

commaCount <- function(x){
  length(gregexpr(',', x)[[1]])
}

parse14 <- function(l, header){
  line <- strsplit(l, ',')
  df <- data.frame(as.list(line[[1]]))
  names(df) <- header
  df
}



## try a different method by gsubbing \n and parsing that