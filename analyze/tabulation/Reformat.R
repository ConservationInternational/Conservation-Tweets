setwd('D://Documents and Settings/mcooper/GitHub/Conservation-Tweets/analyze/tabulation/')

library(dplyr)

users <- read.csv('users.csv', header = F, col.names=c('user', 'count'), quote="", stringsAsFactors=F)

users$user <- gsub(':', '', users$user)

users <- users %>%
  group_by(user) %>%
  summarize(count=sum(count))

write.csv(users, 'users_clean.csv', row.names = F)

keywords <- read.csv('keywords.csv', quote="", stringsAsFactors=F)

keywords <- rename(keywords, TOTAL=RT.1)

RTsum <- keywords %>% group_by(RT) %>%
  summarize(reefs = sum(reefs),
            illness = sum(illness),
            ENERGY = sum(ENERGY),
            livestock = sum(livestock),
            battery = sum(battery),
            money = sum(money),
            fish = sum(fish),
            redd = sum(redd),
            fund = sum(fund),
            pandemic = sum(pandemic),
            market = sum(market),
            ecosystems = sum(ecosystems),
            navy = sum(navy),
            extinct = sum(extinct),
            air = sum(air),
            died = sum(died),
            investment = sum(investment),
            terror = sum(terror),
            finance = sum(finance),
            TOTAL = sum(TOTAL),
            death = sum(death),
            malaria = sum(malaria),
            dying = sum(dying),
            army = sum(army),
            nuclear = sum(nuclear),
            NATURE = sum(NATURE),
            frack = sum(frack),
            hydropower = sum(hydropower),
            industry = sum(industry),
            sick = sum(sick),
            health = sum(health),
            adapt = sum(adapt),
            reforestation = sum(reforestation),
            vegtarian = sum(vegtarian),
            HEALTH = sum(HEALTH),
            energy = sum(energy),
            conflict = sum(conflict),
            forest = sum(forest),
            fight = sum(fight),
            mitigat = sum(mitigat),
            oil = sum(oil),
            transportation = sum(transportation),
            fossil = sum(fossil),
            power = sum(power),
            nature = sum(nature),
            food = sum(food),
            cars = sum(cars),
            peat = sum(peat),
            burn = sum(burn),
            gas = sum(gas),
            vegan = sum(vegan),
            degradation = sum(degradation),
            water = sum(water),
            fuel = sum(fuel),
            geothermal = sum(geothermal),
            restoration = sum(restoration),
            poverty = sum(poverty),
            sink = sum(sink),
            solar = sum(solar),
            syria = sum(syria),
            mangrove = sum(mangrove),
            renewable = sum(renewable),
            resilien = sum(resilien),
            FINANCE = sum(FINANCE),
            land = sum(land),
            isis = sum(isis),
            war = sum(war),
            efficiency = sum(efficiency),
            ecosystem = sum(ecosystem),
            coral = sum(coral),
            disease = sum(disease),
            ocean = sum(ocean),
            tech = sum(tech),
            CONFLICT = sum(CONFLICT),
            clean = sum(clean),
            die = sum(die),
            military = sum(military),
            security = sum(security),
            stock = sum(stock),
            rehabilitation = sum(rehabilitation),
            wind = sum(wind),
            electri = sum(electri))


Datesum <- keywords %>% group_by(date) %>%
  summarize(reefs = sum(reefs),
            illness = sum(illness),
            ENERGY = sum(ENERGY),
            livestock = sum(livestock),
            battery = sum(battery),
            money = sum(money),
            fish = sum(fish),
            redd = sum(redd),
            fund = sum(fund),
            pandemic = sum(pandemic),
            market = sum(market),
            ecosystems = sum(ecosystems),
            navy = sum(navy),
            extinct = sum(extinct),
            air = sum(air),
            died = sum(died),
            investment = sum(investment),
            terror = sum(terror),
            finance = sum(finance),
            TOTAL = sum(TOTAL),
            death = sum(death),
            malaria = sum(malaria),
            dying = sum(dying),
            army = sum(army),
            nuclear = sum(nuclear),
            NATURE = sum(NATURE),
            frack = sum(frack),
            hydropower = sum(hydropower),
            industry = sum(industry),
            sick = sum(sick),
            health = sum(health),
            adapt = sum(adapt),
            reforestation = sum(reforestation),
            vegtarian = sum(vegtarian),
            HEALTH = sum(HEALTH),
            energy = sum(energy),
            conflict = sum(conflict),
            forest = sum(forest),
            fight = sum(fight),
            mitigat = sum(mitigat),
            oil = sum(oil),
            transportation = sum(transportation),
            fossil = sum(fossil),
            power = sum(power),
            nature = sum(nature),
            food = sum(food),
            cars = sum(cars),
            peat = sum(peat),
            burn = sum(burn),
            gas = sum(gas),
            vegan = sum(vegan),
            degradation = sum(degradation),
            water = sum(water),
            fuel = sum(fuel),
            geothermal = sum(geothermal),
            restoration = sum(restoration),
            poverty = sum(poverty),
            sink = sum(sink),
            solar = sum(solar),
            syria = sum(syria),
            mangrove = sum(mangrove),
            renewable = sum(renewable),
            resilien = sum(resilien),
            FINANCE = sum(FINANCE),
            land = sum(land),
            isis = sum(isis),
            war = sum(war),
            efficiency = sum(efficiency),
            ecosystem = sum(ecosystem),
            coral = sum(coral),
            disease = sum(disease),
            ocean = sum(ocean),
            tech = sum(tech),
            CONFLICT = sum(CONFLICT),
            clean = sum(clean),
            die = sum(die),
            military = sum(military),
            security = sum(security),
            stock = sum(stock),
            rehabilitation = sum(rehabilitation),
            wind = sum(wind),
            electri = sum(electri))



write.csv(RTsum, 'RetweetSummary.csv', row.names=F)

write.csv(Datesum, 'DateSummary.csv', row.names=F)

dailysum <- keywords %>% group_by(date) %>%
  summarize(ENERGY = sum(ENERGY),
            NATURE = sum(NATURE),
            TOTAL = sum(TOTAL))

write.csv(dailysum, 'timeseries.csv', row.names=F)

link <- read.csv('media.csv', head=F, col.names=c('url', 'count'),
                 stringsAsFactors=F)

url <- 'https://t.co/ugf6dPQ20D'

library(httr)

getnew <- function(url){
  newurl <- 'URL has expired'
  try({newurl <- GET(url)$url}, silent=T)
  return(newurl)
}

f <- NULL
for (i in c(url, 'test', url)){
  f <- c(f, getnew(i))
}
  

getnew(url)

link$newurl <- sapply(X=link$url, FUN=getnew)
                        