setwd('D:/Documents and Settings/mcooper/Documents/Conservation Tweets/Sample Data')

library(dplyr)

keys <- read.csv('D:/Documents and Settings/mcooper/GitHub/Conservation-Tweets/analyze/keywords.csv', header=F, stringsAsFactors=F)
keys <- unique(keys)


files <- list.files()

readCSV <- function(t){
  chrs <- readChar(t, file.info(t)$size)
  chrs <- gsub('\r', ' ', chrs)
  out <- read.csv(text=chrs, stringsAsFactors=F, quote=NULL)
  if(!'id_str' %in% names(out)){
    out$id_str <- paste0(f, row.names(out))
  }
  out
}

cleanTweet <- function(str){
  if(is.na(str)){
    return('')
  }
  
  clean <- gsub('[^[:alnum:] @#]', '', str)
  
  words <- tolower(clean)
}

bagOfWords <- function(cleanedTweet){
  words <- strsplit(cleanedTweet, ' ')[[1]]
  
  inds <- unlist(gregexpr('http', words))
  if (sum(inds[inds>0]) > 0){
    words <- c(words[which(inds!=1)], 'http')
  }
  
  words <- unique(words[words!=''])
  
  words <- paste(words, collapse=';')
  
  words
}

system.time({
  
accum.df <- data.frame()
for (f in files[1:5]){

  df <- readCSV(f)
  df$text <- cleanTweet(df$text)
  df$BoW <- sapply(X=df$text, FUN=bagOfWords)
  
  for (k in keys$V1){
    pat <- paste0(k, '|', gsub(' ', '', k))
    df[ ,k] <- grepl(pattern = pat, x = df$text)
  }

  accum.df <- bind_rows(accum.df, df)  

}

})
#user  system elapsed 
#208.73    0.36  211.19 

#summarize a df
report <- data.frame(key=keys$V1, count=colSums(df[ , names(df) %in% keys$V1]))
