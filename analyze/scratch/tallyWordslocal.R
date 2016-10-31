library(foreach)
library(doParallel)

setwd('D:/Documents and Settings/mcooper/GitHub/Conservation-Tweets/analyze/BagsOfWords')

dates <- list.files(pattern='BoW.csv$')

keywords <- read.csv('../keywords.csv')

matchWords <- function(bags, w, k){
  k <- tolower(gsub(' ', '&', k))
  sum(grepl(X=bags, wd=w) & sapply(X=bags, wd=k, FUN=infunc))
}

#grepl two words:
#"(?=.*conservation)(?=.*international)"

no_cores <- detectCores() - 1
cl <- makeCluster(no_cores)


#t(apply(names, str_detect, pattern=slices))
#out(names, slices, str_detect)
#sapply(slices, grepl, names)


for (d in dates){
  #system(paste0("sudo aws s3 cp s3://ci-tweets/", d, "-BoW.csv ."))
  f <- read.csv(d, stringsAsFactors = F)
  
  bags <- sapply(f$BoW, split=';', FUN=strsplit)

  words <- unique(unlist(bags))
  
  keys <- read.csv('../keywords.csv', header=F, stringsAsFactors = F)
  
  system.time(
  #Try this with parSapply
  out <- parSapply(cl, FUN=matchWords, bags=bags, words[1:100], keys$V1[1:10])
  )
  
  out <- sapply(FUN=matchWords, bags=bags, words[1:10], keys$V1[1:5])
  
  write.csv(out, paste0('summarize-', d, '.csv'), row.names=F)
  
  system(paste0("sudo rm ", d, "-BoW.csv ."))
  system(paste0("sudo aws s3 cp summarize-", d, ".csvs3://ci-tweets/"))
  system(paste0("sudo rm summarize-", d, ".csv ."))
}