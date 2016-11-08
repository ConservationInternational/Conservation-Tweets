setwd('D:/Documents and Settings/mcooper/Documents/Conservation Tweets/ALL')

files <- list.files()

keys <- read.csv('../keys-11-7.csv', header=F, stringsAsFactors=F)$V1

for (f in files){
  df <- read.csv(f, stringsAsFactors=F)
  
  siku <- substr(f, nchar(f)-17, nchar(f)-8)
  
  for (k in keys){
    if (grepl('&', k)){
      ks <- paste0('^(?=.*\\b', paste(strsplit(k, '&')[[1]], collapse='\\b)(?=.*\\b'), '\\b)')
    } else{
      ks <- k
    }
    
    idx <- grepl(ks, df$text, ignore.case=T, perl=T)
    if(sum(idx)>0){
      sel <- df[idx, ]
      
      if(nrow(sel)!=length(unique(sel$id_str))){
        sel$id_str <- sapply(1:nrow(sel), FUN=function(x)paste0(sample(c(letters, LETTERS, 1:10), 18), collapse=''))
      }
      
      k <- gsub(' ', '.', k)
      
      write.csv(sel, paste0('../ByKeys/', k, '-', siku, '.csv'), row.names=F)
    }
  }
}