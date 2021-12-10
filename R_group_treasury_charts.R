# install.packages('readxl')
# install.packages('ggplot2')
# install.packages('dplyr')

library('readxl')
library('ggplot2')
library('dplyr')

funds  = c('FNB FLI LT Cap','FNB FLI Working','FNB IBNR IPF','FNB IBNR RPF','FNB Life','Friscol','Momentum Ability','RMBSi')

for (i in funds) {
	setwd(paste('//rmb-vpr-file02/Ashburton/Support Services/Risk Management/Investment Analytics/Python/take_on/reports/compliance/holdings', i, sep='/'))
	holdings = read_excel('holdings.xlsx')
	colnames(holdings) = make.names(colnames(holdings))

	# # Bi-Variate Analysis
	# qplot(National.Rating,fill=Industry,data=holdings, geom= "bar",
		  # main = "Industry Distribution per National Rating",
		  # xlab = "National Rating",
		  # ylab = "Industry")
		  
	# qplot(Global.Rating,fill=Industry,data=holdings, geom= "bar",
		  # main = "Industry Distribution per Global Rating",
		  # xlab = "Global Rating",
		  # ylab = "Industry")


	# # Univariate Analysis
	# par(mfrow=c(1,2))	  
	# # Modified Duration
	# hist(holdings$Mod.Dur,col='blue',main='Histogram of Modified Duration',xlab='Modified Duration')

	# # Time to Maturity (Days)
	# hist(holdings$'Time.to.Maturity..days.'/365,col='blue',main='Histogram of Time to Maturity',xlab='Time to Maturity')

	# National Rating
	national_rating = holdings %>% group_by(National.Rating) %>% summarise(Weight = sum(X.Market.Value,na.rm=TRUE))
	ggplot(national_rating, aes(x = National.Rating, y = Weight, fill=National.Rating)) + geom_bar(stat = "identity")
	ggsave('National Rating.jpeg', width = 9, height = 6)

	# National Rating vs Industry
	national_rating_vs_industry = holdings %>% group_by(National.Rating,Industry) %>% summarise(Weight = sum(X.Market.Value,na.rm=TRUE))
	ggplot(national_rating_vs_industry, aes(x = National.Rating, y = Weight, fill=Industry)) + geom_bar(stat = "identity")
	ggsave('National Rating vs Industry.jpeg', width = 9, height = 6)

	# National Rating vs Guarantee
	national_rating_vs_guarantee = holdings %>% group_by(National.Rating,Guarantee) %>% summarise(Weight = sum(X.Market.Value,na.rm=TRUE))
	ggplot(national_rating_vs_guarantee, aes(x = National.Rating, y = Weight, fill=Guarantee)) + geom_bar(stat = "identity")
	ggsave('National Rating vs Guarantee.jpeg', width = 9, height = 6)

	# National Rating vs Collateralization
	national_rating_vs_collateral = holdings %>% group_by(National.Rating,Collateralization) %>% summarise(Weight = sum(X.Market.Value,na.rm=TRUE))
	ggplot(national_rating_vs_collateral, aes(x = National.Rating, y = Weight, fill=Collateralization)) + geom_bar(stat = "identity")
	ggsave('National Rating vs Collateral.jpeg', width = 9, height = 6)

	# Global Rating
	global_rating = holdings %>% group_by(Global.Rating) %>% summarise(Weight = sum(X.Market.Value,na.rm=TRUE))
	ggplot(global_rating, aes(x = Global.Rating, y = Weight, fill=Global.Rating)) + geom_bar(stat = "identity")
	ggsave('Global Rating.jpeg', width = 9, height = 6)

	# Global Rating vs Industry
	global_rating_vs_industry = holdings %>% group_by(Global.Rating,Industry) %>% summarise(Weight = sum(X.Market.Value,na.rm=TRUE))
	ggplot(global_rating_vs_industry, aes(x = Global.Rating, y = Weight, fill=Industry)) + geom_bar(stat = "identity")
	ggsave('Global Rating vs Industry.jpeg', width = 9, height = 6)

	# Global Rating vs Guarantee
	global_rating_vs_guarantee = holdings %>% group_by(Global.Rating,Guarantee) %>% summarise(Weight = sum(X.Market.Value,na.rm=TRUE))
	ggplot(global_rating_vs_guarantee, aes(x = Global.Rating, y = Weight, fill=Guarantee)) + geom_bar(stat = "identity")
	ggsave('Global Rating vs Guarantee.jpeg', width = 9, height = 6)

	# Global Rating vs Collateralization
	global_rating_vs_collateral = holdings %>% group_by(Global.Rating,Collateralization) %>% summarise(Weight = sum(X.Market.Value,na.rm=TRUE))
	ggplot(global_rating_vs_collateral, aes(x = Global.Rating, y = Weight, fill=Collateralization)) + geom_bar(stat = "identity")
	ggsave('Global Rating vs Collateral.jpeg', width = 9, height = 6)

	# Single Issuer Exposure
	ggplot(holdings, aes(x = Issuer, y = Single.Issuer.Exposure, fill=Issuer)) + geom_bar(stat = "identity") + theme(axis.text.x=element_blank())
	ggsave('Single Issuer Exposure.jpeg', width = 15, height = 6)


	# Single Industry Exposure
	ggplot(holdings, aes(x = Industry, y = Single.Industry.Exposure, fill=Industry)) + geom_bar(stat = "identity") + theme(axis.text.x=element_blank())
	ggsave('Single Industry Exposure.jpeg', width = 9, height = 6)
}