setwd('D:/Documents and Settings/mcooper/GitHub/Conservation-Tweets/analyze/Sentiment-Analysis')

library(dplyr)

files <- list.files(pattern='.csv')

bel    <- data.frame()
disbel <- data.frame()
ambig  <- data.frame()

for (f in files){
  file <- read.csv(f)
  
  if (sum(file$belief=='0.5') > 0){
    file$belief[file$belief=='0.5'] <- '?'
  }
  
  bel_s    <- file[file$belief=='1', 'text', drop=F]
  disbel_s <- file[file$belief=='0', 'text', drop=F]
  ambig_s  <- file[file$belief=='?', 'text', drop=F]

  bel    <- bind_rows(bel, unique(bel_s))
  disbel <- bind_rows(disbel, unique(disbel_s))
  ambig  <- bind_rows(ambig, unique(ambig_s))
  
  print(f)
}

write.csv(bel, 'believes.csv', row.names=F)
write.csv(disbel, 'disbelieves.csv', row.names=F)
write.csv(ambig, 'ambiguous.csv', row.names=F)