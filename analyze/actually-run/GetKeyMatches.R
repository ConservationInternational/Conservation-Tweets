library(dplyr)

keys <- read.csv('/home/ubuntu/keywords.txt', header=F, stringsAsFactors=F)
keys <- unique(keys)

system("sudo aws s3 ls s3://ci-tweets/ALL/ >> files.txt")

files <- read.csv('files.txt', header=F, stringsAsFactors=F)
files <- substr(files$V1, 32, nchar(files$V1))
files <- files[grepl('.csv', files)]

system("sudo rm files.txt")

for (f in files){
  if (!f %in% list.files()){
    system(paste0("sudo aws s3 cp s3://ci-tweets/ALL/", f, " /home/ubuntu/", f))
  }
}

cleanTweet <- function(str){
  str[is.null(str)] <- ''
  str[is.na(str)] <- ''
  
  clean <- gsub('[^[:alnum:] @#]', '', str)
  
  words <- tolower(clean)
}

##########################
##Get Keywords
##########################

files <- files[15:52]
keysdf <- read.csv('keysdf.csv')
for(f in files){
  
  cat("processing ", f)
  
  df <- read.csv(f, quote=NULL, stringsAsFactors=F)
  
  names(df) <- c("coordinates", "created_at", "facorite_count", "favorited",
                 "geo", "place", "retweet_count", "retweeted", "text", "user.favorited_count",
                 "user.friends_count", "user.geo_enabled", "user.location", "user.name",
                 "user.statuses_count", "id_str")
  
  if('text' %in% names(df)){
    df$text <- cleanTweet(df$text)
  } else {
    cat("No column text in ", f)
  }
  
  for (k in keys$V1){
    pat <- paste0(k, '|', gsub(' ', '', k))
    df[ ,k] <- grepl(pattern = pat, x = df$text)
  }
  
  keysdf <- bind_rows(keysdf, df)
  
  write.csv(keysdf, 'keysdf.csv', row.names=F)
  
}

