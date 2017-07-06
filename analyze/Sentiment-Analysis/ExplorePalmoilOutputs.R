setwd('D://Documents and Settings/mcooper/GitHub/Conservation-Tweets/analyze/Sentiment-Analysis/')

library(dplyr)
library(ggplot2)
library(tidyr)

ind <- read.csv('ind_dd_bigram.csv', header=F, col.names = c('class', 'count')) %>%
  mutate(freq=count/sum(count), lang='indonesian', tweets='palm')
ind_base <- read.csv('ind_base_dd_bigram.csv', header=F, col.names = c('class', 'count')) %>%
  mutate(freq=count/sum(count), lang='indonesian', tweets='base')
eng <- read.csv('eng_dd.csv', header=F, col.names = c('class', 'count')) %>%
  mutate(freq=count/sum(count), lang='english', tweets='palm')
eng_base <- read.csv('eng_base_dd.csv', header=F, col.names = c('class', 'count')) %>%
  mutate(freq=count/sum(count), lang='english', tweets='base')

all <- Reduce(f = rbind, x=list(ind, ind_base, eng, eng_base))

ggplot(all) + geom_bar(aes(x=class, y=freq, fill=lang, color=tweets), stat='identity', position='dodge') + 
  facet_wrap(lang~tweets)

dif <- all %>% 
  mutate(count=NULL) %>% 
  spread(tweets, freq) %>%
  mutate(diff=palm-base)

ggplot(dif) + geom_bar(aes(x=class, y=diff, fill=lang), stat='identity', position='dodge')
