setwd('D:/Documents and Settings/mcooper/GitHub/Conservation-Tweets/analyze/temporal/from-baseline')

library(lubridate)
library(dplyr)
library(reshape2)
library(ggplot2)

terms <- c('palm oil','deforestation', 'degradation')

getData <- function(i){
  csv <- read.csv(paste0(i, '.csv'), col.names = c('time', 'count', 'baseline', 'frequency'))
  csv$time <- ymd_hms(csv$time) %>% date
  csv <- csv %>% group_by(time) %>% summarize(count=sum(count), baseline=sum(baseline))
  csv$frequency <- csv$count/csv$baseline
  csv <- csv[ , c('time', 'frequency')]
  names(csv)[2] <- paste0(make.names(i))
  csv
}

plotTerms <- function(terms){
  data <- Map(getData, terms) %>% Reduce(f=merge) %>% melt(id.vars='time')
  
  names(data) <- c('Date', 'Keyword', 'Frequency')
  
  ggplot(data, aes(x=Date, y=Frequency, color=Keyword)) + 
    geom_line(size=1.5) + theme_bw()
  
  ggsave(paste0(paste(terms, collapse='_'), '.png'))
}
  