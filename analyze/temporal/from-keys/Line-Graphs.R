
#Run the following command
#aws s3 ls s3://ci-tweets/ByKeyword --recursive > Keywords.txt

#than copy that file into your working directory

setwd('D:/Documents and Settings/mcooper/GitHub/Conservation-Tweets/analyze/temporal/from-keys')

library(dplyr)
library(ggplot2)
library(lubridate)

df <- read.table('Keywords.txt', stringsAsFactors = F)
names(df) <- c('Date.Written', 'Time.Written', 'Size', 'Path')

df$date <- substr(df$Path, nchar(df$Path)-13, nchar(df$Path)-4)
df$key <- substr(df$Path, 11, nchar(df$Path)-15)

df$date <- ymd(df$date)

df <- df[df$date > ymd('2016-11-10'), ]

all_days_keys <- names(table(df$key)[table(df$key) > 100])

sel_keys <- c(all_days_keys)

df <- df[df$key %in% sel_keys, ]

daily_total <- df %>% group_by(date) %>% summarize(Total = sum(Size))

df <- merge(df, daily_total)

df$Daily_Perc <- df$Size/df$Total

simpleCap <- function(x) {
  s <- strsplit(x, " ")[[1]]
  paste(toupper(substring(s, 1,1)), substring(s, 2),
        sep="", collapse=" ")
}

plotit <- function(df, words){
  title <- strsplit(words, 'OR', fixed=T)[[1]]
  keys <- gsub('#', '', title)
  
  if (length(keys) == 1){
    sel <- df[df$key==keys, ]
  }
  if (length(keys) > 1){
    sel <- df[df$key %in% keys, ]
    sel <- sel %>% group_by(date) %>% summarize(Daily_Perc=sum(Daily_Perc))
  }
  
  main = simpleCap(paste0('percent of collected tweets containing ', paste0(gsub('.', ' ', title, fixed=T), collapse = ' or ')))
  
  ggplot(sel, aes(x=ymd(date), y=Daily_Perc)) + geom_line() + theme_bw() + 
    geom_smooth(method="loess", size=1.5) + 
    labs(title=main, x='Date', y='Frequency of Tweets') + 
    scale_x_date(expand=c(0,0))
  
  ggsave(paste0(words, '.png'))
}

for (i in all_days_keys){
  plotit(df, i)
}



