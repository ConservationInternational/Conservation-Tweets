setwd('D:/Documents and Settings/mcooper/GitHub/Conservation-Tweets/analyze/temporal/from-baseline')

library(plyr)
library(dplyr)
library(ggplot2)

getFreq <- function(str){
  df <- read.csv(paste0(str, '.csv'), col.names=c('date', 'count', 'total', 'freq'))
  count <- sum(df$count)
  count
}

data <- data.frame(keyword=c('climate change', 'recycling', 'pesticides', 
                            'mass extinction', 'biodiversity', 'conservation international',
                           'deforestation', 'sdgs'))

data$keyword <- factor(data$keyword, levels=c('climate change', 'recycling', 'sdgs', 'biodiversity', 'pesticides', 'deforestation', 'mass extinction', 'conservation international'))

data$frequency <- sapply(X = data$keyword, FUN=getFreq)

ggplot(data, aes(x=keyword, y=frequency)) + geom_bar(stat='identity', aes(fill=keyword)) + 
  theme_bw() + ggtitle("Total tweets between 11-16 and 12-07") + 
  scale_x_discrete(labels=c('climate change'='climate\nchange',
                            'recycling'='recycling', 
                            'pesticides'='pesticides', 
                            'mass extinction'='mass\nextinction', 
                            'biodiversity'='biodiversity', 
                            'conservation international'='conservation\ninternational',
                            'deforestation'='deforestation', 
                            'sdgs'='SDGs'))+
  theme(legend.position="none")

ggsave('frequency.png')



