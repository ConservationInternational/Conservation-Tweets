library(ggplot)
library(ggrepel)

#Climate
setwd('D:/Documents and Settings/mcooper/GitHub/Conservation-Tweets/analyze/PMI')

pre <- read.csv('climatechange-pre_results.csv', col.names = c('word', 'prePMI', 'preCount'))
post <- read.csv('climatechange-post_results.csv', col.names = c('word', 'postPMI', 'postCount'))

pre <- pre[pre$preCount > 100 & pre$prePMI > 0, ]
post <- post[post$postCount > 100 & post$postPMI > 0, ]

cc <- merge(pre, post)

write.csv(cc, 'climate_election.csv', row.names=F)

new <- read.csv('climate_election.csv')
new <- new[which(new$keep==1), ]

max <- max(c(new$prePMI[new$keep==1], new$postPMI[new$keep==1]))
df_poly1 <- data.frame(
  x=c(-0.5, max + 0.5, -0.5),
  y=c(-0.5, max + 0.5, max + 0.5)
)
df_poly2 <- data.frame(
  x=c(-0.5, max + 0.5, max + 0.5),
  y=c(-0.5, -0.5, max + 0.5)
)

new$wt <- new$preCount + new$postCount
new$wt <- new$wt/max(new$wt)
new$wt <- cut(new$wt, breaks=c(0,.075,.5,0.75,1))

ggplot(new, aes(prePMI, postPMI)) + geom_text_repel(aes(label=word, size=wt), segment.alpha=0) +
  scale_size_manual(values=c(3,4.5,6,10)) +
  geom_polygon(data=df_poly1, aes(x, y), fill="blue", alpha=0.1) +
  geom_polygon(data=df_poly2, aes(x, y), fill="orange", alpha=0.1) + 
  xlim(-0.5, max + 0.5) + ylim(-0.5, max + 0.5) + 
  theme_bw() + 
  scale_x_continuous(expand = c(0, 0)) + scale_y_continuous(expand = c(0, 0)) + 
  xlab('Before Election') + ylab('After Election') + 
  theme(legend.position="none")
ggsave('climate-bivariate.png')




#Vegetarian-Vegan
# setwd('D:/Documents and Settings/mcooper/GitHub/Conservation-Tweets/analyze/PMI')
# 
# vegan <- read.csv('vegan_results.csv', col.names = c('word', 'veganPMI', 'veganCount'))
# vegetarian <- read.csv('vegetarian_results.csv', col.names = c('word', 'vegetarianPMI', 'vegetarianCount'))
# 
# vegan <- vegan[vegan$veganCount > 100 & vegan$veganPMI > 0, ]
# vegetarian <- vegetarian[vegetarian$vegetarianCount > 100 & vegetarian$vegetarianPMI > 0, ]
# 
# cc <- merge(vegan, vegetarian)
# 
# write.csv(cc, 'veg.csv', row.names=F)
# 
# new <- read.csv('veg.csv')
# new <- new[which(new$keep==1), ]
# 
# ggplot(new, aes(veganPMI, vegetarianPMI)) + geom_text(aes(label=word))
# ggsave('veg-bivariate.png')
# 



#Climate Change; Global Warming
setwd('D:/Documents and Settings/mcooper/GitHub/Conservation-Tweets/analyze/PMI')

climate <- read.csv('climate.change.csv', col.names = c('word', 'climateCount', 'climatePMI'))
global <- read.csv('global.warming.csv', col.names = c('word', 'globalCount', 'globalPMI'))

climate <- climate[climate$climateCount > 100 & climate$climatePMI > 0, ]
global <- global[global$globalCount > 100 & global$globalPMI > 0, ]

cc <- merge(climate, global)

write.csv(cc, 'cc_gw.csv', row.names=F)

new <- read.csv('cc_gw.csv')
new <- new[which(new$keep==1), ]

max <- max(c(new$climatePMI[new$keep==1], new$globalPMI[new$keep==1]))
df_poly1 <- data.frame(
  x=c(-0.5, max + 0.5, -0.5),
  y=c(-0.5, max + 0.5, max + 0.5)
)
df_poly2 <- data.frame(
  x=c(-0.5, max + 0.5, max + 0.5),
  y=c(-0.5, -0.5, max + 0.5)
)

new$wt <- new$climateCount + new$globalCount
new$wt <- new$wt/max(new$wt)
new$wt <- cut(new$wt, breaks=c(0,.01,.1,0.75,1))

ggplot(new, aes(climatePMI, globalPMI)) + geom_text_repel(aes(label=word, size=wt), segment.alpha=0) +
  scale_size_manual(values=c(3,4.5,6,10)) +
  geom_polygon(data=df_poly1, aes(x, y), fill="blue", alpha=0.1) +
  geom_polygon(data=df_poly2, aes(x, y), fill="orange", alpha=0.1) + 
  xlim(-0.5, max + 0.5) + ylim(-0.5, max + 0.5) + 
  theme_bw() + 
  scale_x_continuous(expand = c(0, 0)) + scale_y_continuous(expand = c(0, 0)) + 
  xlab('Climate Change') + ylab('Global Warming') + 
  theme(legend.position="none")
ggsave('cc_gw.png')

#CI vs TNC
# 
# tnc <- read.csv('tnc.csv', col.names = c('word', 'tncCount', 'tncPMI'))
# ci <- read.csv('conservation.international.csv', col.names = c('word', 'ciCount', 'ciPMI'))
# 
# leaders <- merge(tnc, ci)
# 
# write.csv(leaders, 'leaders.csv', row.names=F)
# 
# new <- read.csv('leaders.csv')
# new <- new[which(new$keep==1), ]
# 
# ggplot(new, aes(tncPMI, ciPMI)) + geom_text(aes(label=word))
# ggsave('orgs.png')
