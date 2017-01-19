library(ggplot2)
library(reshape2)

setwd('D:/Documents and Settings/mcooper/GitHub/Conservation-Tweets/analyze/tabulation/')

table <- read.csv('Word_Tablulation.csv')
tab <- melt(table, value.name = 'X')
names(tab) <- c('Keyword', 'Co-Occuring Word', 'PMI')

count <- read.csv('Count.csv')
count <- melt(count, value.name = 'X')
names(count) <- c('Keyword', 'x', 'count')

tab$WordCount <- count$count


ggplot(tab, aes(`Co-Occuring Word`, Keyword)) + geom_tile(aes(fill=PMI), width=0.9, height=0.9) + 
  geom_text(data=tab, aes(`Co-Occuring Word`, Keyword, label = signif(WordCount, digits=2)), color="black", size=rel(4.5)) +
  scale_fill_gradient(low = "white", high = "red", space = "Lab", na.value = "gray90", guide = "colourbar") +
  scale_x_discrete(expand = c(0, 0), position = "top") +
  scale_y_discrete(expand = c(0, 0)) +
  xlab("") + 
  ylab("") +
  theme(panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        panel.border = element_rect(fill=NA,color="gray90", size=0.5, linetype="solid"),
        axis.line = element_blank(),
        axis.ticks = element_blank(),
        panel.background = element_rect(fill="gray90"),
        plot.background = element_rect(fill="gray90"),
        axis.text = element_text(color="black", size=14), 
        axis.text.x = element_text(angle = 90, hjust = 1))

ggsave('output.png')
