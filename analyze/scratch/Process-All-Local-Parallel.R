setwd('D:/Documents and Settings/mcooper/Documents/Conservation Tweets/Sample Data')

library(dplyr)
library(doParallel)
library(foreach)
library(parallel)

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
  
  words <- paste(c('', words, ''), collapse=';')
  
  words
}

##########################
##Get Keywords
##########################

system.time({

no_cores <- detectCores() - 1
cl <- makeCluster(no_cores)
registerDoParallel(cl)


out <- foreach(f=files[1:5]) %dopar%{
  
  df <- readCSV(f)
  df$text <- cleanTweet(df$text)
  df$BoW <- sapply(X=df$text, FUN=bagOfWords)
  
  for (k in keys$V1){
    pat <- paste0(k, '|', gsub(' ', '', k))
    df[ ,k] <- grepl(pattern = pat, x = df$text)
  }
  
  df
  
}

keysdf <- bind_rows(out)

stopCluster(cl)

})

#summarize a df
#report <- data.frame(key=keys$V1, count=colSums(df[ , names(df) %in% keys$V1]))

##################
##Get Matches for Other Words
##################

words <- sapply(keysdf$BoW, split=';', FUN=strsplit) %>% unlist %>% table
words <- names(head(words[order(words)], n=500))

wordsdf <- keysdf[ , c('id_str', 'BoW')]

system.time({
  
no_cores <- detectCores() - 1
cl <- makeCluster(no_cores)
registerDoParallel(cl)


out <- foreach(w=words) %dopar%{
  
  grepl(paste0(';', w, ';'), wordsdf$BoW)
  
}

names(out) <- gsub('@', 'AT', gsub('#', 'HSH', words))

wordsdf <- cbind(wordsdf, as.data.frame(out))


stopCluster(cl)
  
})

#########################
##Tabulate Co-Occurances
#########################

#Try to tabulate by tweet, then sum
system.time({
  
  no_cores <- detectCores() - 1
  cl <- makeCluster(no_cores)
  registerDoParallel(cl)
  
  wordsel <- make.names(gsub('@', 'AT', gsub('#', 'HSH', words)))
  
  out <- foreach(id=wordsdf$id_str[1:5000]) %dopar%{
    
    keys_bin <- keysdf[keysdf$id_str==id, keys$V1]
    words_bin <- wordsdf[wordsdf$id_str==id, wordsel]
    sapply(words_bin, '&', keys_bin)

  }
  
  tabulation <- Reduce('+', out)
  
  colnames(tabulation) <- wordsel
  rownames(tabulation) <- keys$V1
    
  #Get margin totals too!
  
  stopCluster(cl)
  
})


jointCount <- function(vec1, vec2){
  
}


#Try to mergeDfs, then tabulate all
system.time({
  
  no_cores <- detectCores() - 1
  cl <- makeCluster(no_cores)
  registerDoParallel(cl)
  
  wordsel <- make.names(gsub('@', 'AT', gsub('#', 'HSH', words)))
  
  mergedf <- merge(keysdf, wordsdf, by='id_str')
  
  out <- foreach(id=wordsdf$id_str[1:50]) %dopar%{
    
    keys_bin <- keysdf[keysdf$id_str==id, keys$V1]
    words_bin <- wordsdf[wordsdf$id_str==id, wordsel]
    sapply(words_bin, '&', keys_bin)
    
  }
  
  stopCluster(cl)
  
})