setwd('D:/Documents and Settings/mcooper/GitHub/Conservation-Tweets/analyze/Sentiment-Analysis')

library(dplyr)
library(ggplot2)
library(Hmisc)

eng_dd_range <- read.csv('eng_dd_range.csv', col.names = c('score', 'count'), header=F) %>%
  mutate(lang='English', key='palm')
eng_base_range <- read.csv('eng_base_dd_range.csv', col.names = c('score', 'count'), header=F) %>%
  mutate(lang='English', key='base')
ind_dd_range <- read.csv('ind_dd_range.csv', col.names = c('score', 'count'), header=F) %>%
  mutate(lang='Bahasa', key='palm')
ind_base_range <- read.csv('ind_base_dd_range.csv', col.names = c('score', 'count'), header=F) %>%
  mutate(lang='Bahasa', key='base')

all <- Reduce(bind_rows, list(eng_dd_range, eng_base_range, ind_dd_range, ind_base_range)) %>%
  #filter(score !=0) %>%
  mutate(class=ifelse(score == 1, 'Positive',
                      ifelse(score == -1, 'Negative',
                             ifelse(score > 1, 'Very Positive',
                                  ifelse(score < -1, 'Very Negative', 
                                         ifelse(score == 0, 'Neutral', '')))))) %>%
  group_by(class, lang, key) %>%
  dplyr::summarize(count = sum(count))

allsum <- all %>% group_by(lang, key) %>%
  dplyr::summarize(total = sum(count)) %>%
  merge(all) %>%
  mutate(freq = count/total, class =  factor(class, levels=c('Very Negative', 'Negative', 'Neutral', 'Positive', 'Very Positive')))

ggplot(allsum %>% filter(key=='palm')) + 
  geom_bar(aes(x='', y=freq, fill=class), position='stack', stat='identity', width=1) + 
  coord_polar('y', start=0) + 
  facet_grid(.~lang) +
  scale_fill_manual(values=c("#76342e", "#AD4D43", "#7d9fb8", "#7DAD43", '#55762e')) + theme_bw() +
  theme(axis.text = element_blank(),
        axis.ticks = element_blank(),
        panel.grid  = element_blank()) +
  xlab('') + ylab('') + 
  guides(fill=guide_legend(title="Tweet Sentiment"))

ggsave('PalmOilPie.png')
