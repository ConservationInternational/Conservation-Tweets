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

##################################################
##Test values based on range with bigram dataset
##################################################
ind <- read.csv('ind_dd_range.csv', header=F, col.names = c('class', 'count')) %>%
  mutate(freq=count/sum(count), lang='indonesian', tweets='palm')
ind_base <- read.csv('ind_base_dd_range.csv', header=F, col.names = c('class', 'count')) %>%
  mutate(freq=count/sum(count), lang='indonesian', tweets='base')
eng <- read.csv('eng_dd_range.csv', header=F, col.names = c('class', 'count')) %>%
  mutate(freq=count/sum(count), lang='english', tweets='palm')
eng_base <- read.csv('eng_base_dd_range.csv', header=F, col.names = c('class', 'count')) %>%
  mutate(freq=count/sum(count), lang='english', tweets='base')

all <- Reduce(f = rbind, x=list(ind, ind_base, eng, eng_base))

ggplot(all) + geom_bar(aes(x=class, y=freq), stat='identity', position='dodge') + 
  xlim(c(-5, 5)) + 
  facet_wrap(lang~tweets)

#Difference between base and sawit in bahasa
ind_base_dist <- mapply(FUN=rep, x=ind_base$class, times=ind_base$count) %>% unlist
ind_dist <- mapply(FUN=rep, x=ind$class, times=ind$count) %>% unlist

ks.test(ind_base_dist, ind_dist)

#Difference between base and palm oil in english
eng_base_dist <- mapply(FUN=rep, x=eng_base$class, times=eng_base$count) %>% unlist
eng_dist <- mapply(FUN=rep, x=eng$class, times=eng$count) %>% unlist

ks.test(eng_base_dist, eng_dist)

#Both are significantly different

#Try categorizing, and do a chi-sq test
all$cat[all$class < 0] <- 'negative'
all$cat[all$class > 0] <- 'positive'
all$cat[all$class == 0] <- 'neutral'

all$freq <- NULL

ind <- all %>% 
  filter(lang=='indonesian') %>%
  group_by(tweets, cat) %>%
  summarize(count=sum(count)) %>%
  spread(tweets, count) %>%
  data.frame
row.names(ind) <- ind$cat
ind$cat <- NULL

chisq.test(ind)

ind <- all %>% 
  filter(lang=='indonesian') %>%
  group_by(tweets, cat) %>%
  summarize(count=sum(count)) %>%
  spread(tweets, count) %>%
  data.frame
row.names(ind) <- ind$cat
ind$cat <- NULL

chisq.test(ind)

