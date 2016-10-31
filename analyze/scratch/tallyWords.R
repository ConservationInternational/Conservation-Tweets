library(foreach)
library(doParallel)

dates <- c(paste0('v1-2016-09-', substr(100+seq(6,30),2,3)),
           paste0('v1-2016-10-', substr(100+seq(1,26),2,3)),
           paste0('v2-2016-10-', substr(100+seq(24,26),2,3)))

keywords <- read.csv('keywords.csv')

infunc <- function(wd, vec){
  wd %in% vec
}

matchWords <- function(bags, w, k){
  k <- tolower(gsub(' ', '&', k))
  sum(sapply(X=bags, wd=w, FUN=infunc) & sapply(X=bags, wd=k, FUN=infunc))
}



no_cores <- detectCores() - 1
cl <- makeCluster(no_cores)


for (d in dates){
  system(paste0("sudo aws s3 cp s3://ci-tweets/", d, "-BoW.csv ."))
  f <- read.csv(paste0(d, "-BoW.csv"), stringsAsFactors = F)
  
  bags <- sapply(f$BoW, split=';', FUN=strsplit)

  words <- unique(unlist(bags))
  
  keys <- read.csv('keywords.txt', header=F, stringsAsFactors = F)
  system.time(
  
  #Try this with parSapply
  out <- parSapply(cl, FUN=matchWords, bags=bags, words[1:100], keys$V1[1:10])
  )
  
  out <- sapply(FUN=matchWords, bags=bags, words[1:10], keys$V1[1:5])
  
  write.csv(out, paste0('summarize-', d, '.csv'), row.names=F)
  
  system(paste0("sudo rm ", d, "-BoW.csv ."))
  system(paste0("sudo aws s3 cp summarize-", d, ".csvs3://ci-tweets/"))
  system(paste0("sudo rm summarize-", d, ".csv ."))
  )
}