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

ggplot(new, aes(prePMI, postPMI)) + geom_text(aes(label=word))
ggsave('climate-bivariate.png')

#Vegetarian-Vegan
setwd('D:/Documents and Settings/mcooper/GitHub/Conservation-Tweets/analyze/PMI')

vegan <- read.csv('vegan_results.csv', col.names = c('word', 'veganPMI', 'veganCount'))
vegetarian <- read.csv('vegetarian_results.csv', col.names = c('word', 'vegetarianPMI', 'vegetarianCount'))

vegan <- vegan[vegan$veganCount > 100 & vegan$veganPMI > 0, ]
vegetarian <- vegetarian[vegetarian$vegetarianCount > 100 & vegetarian$vegetarianPMI > 0, ]

cc <- merge(vegan, vegetarian)

write.csv(cc, 'veg.csv', row.names=F)

new <- read.csv('veg.csv')
new <- new[which(new$keep==1), ]

ggplot(new, aes(veganPMI, vegetarianPMI)) + geom_text(aes(label=word))
ggsave('veg-bivariate.png')

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

ggplot(new, aes(climatePMI, globalPMI)) + geom_text(aes(label=word))
ggsave('cc_gw.png')

#CI vs TNC

tnc <- read.csv('tnc.csv', col.names = c('word', 'tncCount', 'tncPMI'))
ci <- read.csv('conservation.international.csv', col.names = c('word', 'ciCount', 'ciPMI'))

leaders <- merge(tnc, ci)

write.csv(leaders, 'leaders.csv', row.names=F)

new <- read.csv('leaders.csv')
new <- new[which(new$keep==1), ]

ggplot(new, aes(tncPMI, ciPMI)) + geom_text(aes(label=word))
ggsave('orgs.png')
