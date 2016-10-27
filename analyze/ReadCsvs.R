source('llaves.R')

library(aws.s3)

Sys.setenv("AWS_ACCESS_KEY_ID" = aws_access_key_id,
           "AWS_SECRET_ACCESS_KEY" = aws_secret_access_key,
           "AWS_DEFAULT_REGION" = "us-east-1")





files <- list.files()

t <- files[1]





readCSV <- function(t){
  chrs <- readChar(t, file.info(t)$size)
  chrs <- gsub('\r', ' ', chrs)
  out <- read.csv(text=chrs, stringsAsFactors=F, quote=NULL)
}

textToBagOfWords <- function(str){
  
  clean <- gsub('[^[:alnum:] @#]', '', str)
  
  words <- strsplit(clean, ' ')[[1]]
  
  #turn urls to 'http'
  inds <- unlist(gregexpr('http', words))
  if (sum(inds[inds>0]) > 0){
    words <- c(words[which(inds!=1)], 'http')
  }
  
  words <- unique(words[words!=''])
  
  words
}

sum(c(20, 40, 60, 80, 100, 120, 140, 140, 140)*0.0314)
