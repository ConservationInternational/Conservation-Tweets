library(ggplot2)
library(lubridate)

setwd('D://Documents and Settings/mcooper/GitHub/Conservation-Tweets/analyze/Sentiment-Analysis/')

df <- read.csv('timeseries_sentiment_climate.csv')

df$day <- ymd(df$day)

#filter
df <- df[df$day > '2016-11-18', ]
df <- df[df$max != '', ]
df$max <- factor(df$max, levels=c('t', 'a', 'f'), labels=c('True', 'Ambiguous', 'False'))

#Refit and sort
df <- df %>% group_by(day, max) %>%
  summarize(count = sum(count))

dfsum <- df %>% group_by(day) %>%
  summarize(total = sum(count))

df_prop <- merge(df, dfsum)

df_prop$prop <- df_prop$count/df_prop$total

ggplot(df_prop, aes(x=day, y=prop, fill=max)) + geom_area(alpha=.75) + 
  scale_x_date(expand = c(0, 0)) +
  scale_y_continuous(expand = c(0, 0)) + 
  theme_bw() + 
  scale_fill_manual(values=c("#7DAD43", "#A8A8A8", "#AD4D43"), 
                      name="Category") +
  ylab('Proportion of Tweets') + xlab('Date') + 
  ggtitle('Propotion of Tweets Assuming Climate Change is True or False')

ggplot(df, aes(x=day, y=count, fill=max)) + geom_area() +  
  scale_x_date(expand = c(0, 0)) +
  scale_y_continuous(limits = c(0, 230000), expand = c(0, 0)) + 
  theme_bw() + 
  scale_fill_manual(values=c("#7DAD43", "#A8A8A8", "#AD4D43"), 
                    name="Category") +
  ylab('Number of Tweets') + xlab('Date') + 
  ggtitle('Number of Tweets Assuming Climate Change is True or False')
