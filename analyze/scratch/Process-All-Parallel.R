library(dplyr)
library(doParallel)
library(foreach)
library(parallel)

keys <- read.csv('/home/ubuntu/keywords.txt', header=F, stringsAsFactors=F)
keys <- unique(keys)

system("sudo aws s3 ls s3://ci-tweets/ALL/ >> files.txt")

files <- read.csv('files.txt', header=F)
files <- substr(files$V1, 32, length(files$V1))

files <- files[grepl('all', files)]

system("sudo rm files.txt")

cleanTweet <- function(str){
  if(is.null(str)){
    return('')  
  }else if(is.na(str)){
    return('')
  }
  
  clean <- gsub('[^[:alnum:] @#]', '', str)
  
  words <- tolower(clean)
}

##########################
##Get Keywords
##########################

no_cores <- detectCores() - 1
cl <- makeCluster(no_cores)
registerDoParallel(cl)

cat("Reading in Files")

out <- foreach(f=files) %dopar%{
  
  cat("processing ", f)
  
  system(paste0("sudo aws s3 cp s3://ci-tweets/ALL/", f, " /home/ubuntu/", f))
  df <- read.csv(f, quote=NULL, stringsAsFactors=F)
  system(paste0("sudo rm ", f))
  
  df$text <- cleanTweet(df$text)
  
  for (k in keys$V1){
    pat <- paste0(k, '|', gsub(' ', '', k))
    df[ ,k] <- grepl(pattern = pat, x = df$text)
  }
  
  df
  
}

cat("All Files read in and combined")

keysdf <- bind_rows(out)
rm(out)


write.csv(keysdf, "keysdf.csv", row.names=F)
system("sudo aws s3 cp keysdf.csv s3://ci-tweets/")
system("sudo rm keysdf.csv")


stopCluster(cl)


#summarize a df
#report <- data.frame(key=keys$V1, count=colSums(df[ , names(df) %in% keys$V1]))

##################
##Get Matches for Other Words
##################

cat("Getting unique words")

words <- sapply(keysdf$BoW, split=';', FUN=strsplit) %>% unlist %>% table
words <- names(head(words[order(words)], n=1000))

cat("Top 1000 Unique words gotten")

wordsdf <- keysdf[ , c('id_str', 'BoW')]

  
no_cores <- detectCores() - 1
cl <- makeCluster(no_cores)
registerDoParallel(cl)

cat("Getting words df")

out <- foreach(w=words) %dopar%{
  
  cat("Looking at occurances of word ", w)
  
  grepl(paste0(';', w, ';'), wordsdf$BoW)
  
}

names(out) <- gsub('@', 'AT', gsub('#', 'HSH', words))

wordsdf <- cbind(wordsdf, as.data.frame(out))


stopCluster(cl)
  


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