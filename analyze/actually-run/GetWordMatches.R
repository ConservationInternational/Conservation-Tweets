library(dplyr)
library(doParallel)
library(foreach)
library(parallel)

system("sudo aws s3 ls s3://ci-tweets/BoW-v1/ >> files.txt")

files <- read.csv('files.txt', header=F, stringsAsFactors=F)
files <- substr(files$V1, 32, nchar(files$V1))
files <- files[grepl('.csv', files)]

system("sudo rm files.txt")

for (f in files){
  if (!f %in% list.files()){
    system(paste0("sudo aws s3 cp s3://ci-tweets/BoW-v1/", f, " /home/ubuntu/", f))
  }
}

##################
##Get Matches for Other Words
##################


words <- sapply(keysdf$text, split=' ', FUN=strsplit) %>% unlist %>% table
words <- names(head(words[order(words)], n=1000))


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

