library(ggplot2)
library(lubridate)

setwd('D://Documents and Settings/mcooper/GitHub/Conservation-Tweets/analyze/Sentiment-Analysis/')

df <- read.csv('timeseries_sentiment_climate.csv')

df$day <- ymd(df$day)

df <- df[df$keyword=='global.warming', ]

df <- df %>% group_by(day, max) %>%
  summarize(count = sum(count))

dfsum <- df %>% group_by(day) %>%
  summarize(total = sum(count))

df <- merge(df, dfsum)

df$prop <- df$count/df$total

ggplot(df, aes(x=day, y=prop, fill=max)) + geom_area()
