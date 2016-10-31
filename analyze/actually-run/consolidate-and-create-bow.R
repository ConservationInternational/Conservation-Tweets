library(dplyr)

readCSV <- function(t){
  chrs <- readChar(t, file.info(t)$size)
  chrs <- gsub('\r', ' ', chrs)
  out <- read.csv(text=chrs, stringsAsFactors=F, quote=NULL)
  out
}

textToBagOfWords <- function(str){
  if(is.na(str)){
    return('')
  }
  
  clean <- gsub('[^[:alnum:] @#]', '', str)
  
  words <- tolower(strsplit(clean, ' ')[[1]])
  
  #turn urls to 'http'
  inds <- unlist(gregexpr('http', words))
  if (sum(inds[inds>0]) > 0){
    words <- c(words[which(inds!=1)], 'http')
  }
  
  words <- unique(words[words!=''])
  
  words <- paste(words, collapse=';')
  
  words
}

dates <- c(paste0('2016-09-', substr(100+seq(09,30),2,3)),
           paste0('2016-10-', substr(100+seq(24,25),2,3)))

for (d in dates){
  print(d)
  system("sudo mkdir temp")
  system(paste0('sudo aws s3 cp s3://ci-tweets temp --recursive --exclude=* --include="', d, '*"'))

  files <- paste0('temp/', list.files('temp'))
  
  tables <- lapply(X = files, FUN=readCSV)
  
  bound <- bind_rows(tables)
  
  bound$id_str <- 100000000000000000 + 
                  as.numeric(substr(d,6,7))*10000000000 + 
                  as.numeric(substr(d,9,10))*100000000 +
                  as.numeric(rownames(bound))
  
  print("writing changes")
  write.csv(bound, paste0('temp/v1-', d, '-all.csv'), row.names=F)
  system(paste0("sudo aws s3 cp temp/v1-", d, "-all.csv s3://ci-tweets"))
  
  print("Making Bag of Words")
  bound$BoW <- sapply(X=bound$text, FUN=textToBagOfWords)
  write.csv(bound[ , c('id_str', 'BoW')], paste0('temp/v1-', d, '-BoW.csv'), row.names=F)
  system(paste0("sudo aws s3 cp temp/v1-", d, "-BoW.csv s3://ci-tweets"))
  
  
  system("sudo rm -r temp") 
}