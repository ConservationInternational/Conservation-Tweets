setwd('D:/Documents and Settings/mcooper/Documents/Conservation Tweets/Sample Data')

files <- list.files()

t <- files[1]


#START including uuids in tweets
#START removing \n from tweets

#etymology of the word handle?
#Hand in swahili?

readCSV <- function(t){
  lines <- readLines(t)
  commaCounts <- sapply(lines, FUN=commaCount)
  clean <- paste(lines[commaCounts==14], collapse='\n')
  df <- read.csv(textConnection(clean))
  
  #deal with bad lines
  sel <- lines[commaCounts!=14]
  tweet <- ''
  for (i in sel){
    if(tweet==''){
      tweet<-i
    }else{
      tweet <- paste0(tweet, i)
    }
    
    if(length(gregexpr(',', tweet)[[1]])==14){
      out <- parse14(tweet, names(df))
      df <- rbind(df, out)
      tweet <- ''
    }
  }
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

## try a different method by gsubbing \n and parsing that