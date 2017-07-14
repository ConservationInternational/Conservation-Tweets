setwd('D://Documents and Settings/mcooper/GitHub/Conservation-Tweets/analyze/Sentiment-Analysis/palm processing results/')

library(dplyr)
library(tidyr)
library(lubridate)

dat <- read.csv('PalmSawitDailyTotals.csv') %>%
  filter(Key=='sawit') %>%
  select(Date, Positive=IndPos, Negative=IndNeg, Total) %>%
  mutate(Neutral = Total - (Positive + Negative)) %>%
  select(Date, Positive, Negative, Neutral) %>%
  gather(Sentiment, Count, -Date)

dat$Date <- ymd(dat$Date)  

dat <- dat %>%
  filter(Date > '2016-11-18')

ggplot(dat, aes(x=Date, y=Count, fill=Sentiment)) + geom_area(alpha=.75) + 
  scale_x_date(expand = c(0, 0)) +
  scale_y_continuous(expand = c(0, 0)) + 
  theme_bw() + 
  scale_fill_manual(values=c("#AD4D43", "#A8A8A8", "#7DAD43"), 
                    name="Category") +
  ylab('Number of Tweets') + xlab('Date') + 
  ggtitle('Number of Bahasa Tweets Containinig the Word "Sawit" By Sentiment Category')
ggsave('Bahasa_Count_Timeline.png')

datsum <- dat %>% group_by(Date) %>%
  summarize(Total = sum(Count))

dat_prop <- merge(dat, datsum)

dat_prop$Proportion <- dat_prop$Count/dat_prop$Total

ggplot(dat_prop, aes(x=Date, y=Proportion, fill=Sentiment)) + geom_area(alpha=.75) + 
  scale_x_date(expand = c(0, 0)) +
  scale_y_continuous(expand = c(0, 0)) + 
  theme_bw() + 
  scale_fill_manual(values=c("#AD4D43", "#A8A8A8", "#7DAD43"), 
                    name="Category") +
  ylab('Proportion of Tweets') + xlab('Date') + 
  ggtitle('Proportion of Bahasa Tweets Containinig the Word "Sawit" In Each Sentiment Category')
ggsave('Bahasa_Proportion_Timeline.png')


ggplot(dat %>% filter(Sentiment=='Positive'), aes(x=Date, y=Count, fill=Sentiment)) + geom_area(alpha=.75) + 
  scale_x_date(expand = c(0, 0)) +
  scale_y_continuous(expand = c(0, 0)) + 
  theme_bw() + 
  scale_fill_manual(values=c("#7DAD43"), 
                    name="Category") +
  ylab('Number of Tweets') + xlab('Date') + 
  ggtitle('Number of Positive Bahasa Tweets Containinig the Word "Sawit" By Sentiment Category')
ggsave('Bahasa_Count_Timeline_Positive.png')


ggplot(dat %>% filter(Sentiment=='Negative'), aes(x=Date, y=Count, fill=Sentiment)) + geom_area(alpha=.75) + 
  scale_x_date(expand = c(0, 0)) +
  scale_y_continuous(expand = c(0, 0)) + 
  theme_bw() + 
  scale_fill_manual(values=c("#AD4D43"), 
                    name="Category") +
  ylab('Number of Tweets') + xlab('Date') + 
  ggtitle('Number of Negative Bahasa Tweets Containinig the Word "Sawit" By Sentiment Category')
ggsave('Bahasa_Count_Timeline_Negative.png')
