library('xts')
library('PerformanceAnalytics')
library('readxl')

setwd('//rmb-vpr-file02/Ashburton/Support Services/Risk Management/Investment Analytics/Python/take_on/config')

absolute = read_excel('//rmb-vpr-file02/Ashburton/Support Services/Risk Management/Investment Analytics/Python/take_on/config/returns_pivot_table.xlsx', sheet='absolute')
absolute_xts <- xts(x=absolute,order.by=as.Date(absolute$date))
#absolute_xts <- xts(x=absolute[,5:18],order.by=as.Date(absolute$date))
#absolute_xts = absolute_xts[,-c(3,4,7)]

alpha = read_excel('//rmb-vpr-file02/Ashburton/Support Services/Risk Management/Investment Analytics/Python/take_on/config/returns_pivot_table.xlsx', sheet='alpha')
alpha_xts <- xts(x=alpha,order.by=as.Date(alpha$date))
# alpha_xts <- xts(x=alpha[,5:18],order.by=as.Date(alpha$date))
# alpha_xts = alpha_xts[,-c(3,4,7)]


color = c('pink','#FF0099','#CCFF00','#FF9900','blue4','#00FF4D','red4','olivedrab',
          'cyan2','mediumslateblue','bisque','lightgoldenrod')

# Cumulative Alpha Plot:
chart.RollingPerformance(R=alpha_xts, width=12,
                         legend.loc="bottomleft", main='Rolling 12-Month Alpha - 31 Dec 2019', colorset=color)

# Rolling tracking error
chart.RollingPerformance(R=alpha_xts,FUN="sd",width=12, legend.loc="topleft", main='Rolling 12-Month Tracking Error - 31 Dec 2019', colorset=color)

# Information ratio plot:
chart.RiskReturnScatter(R=tail(alpha_xts,12), xlab = 'Tracking Error', ylab = 'Alpha', main='1 Year Information Ratio - 31 Dec 2019')

# Drawdown Chart
chart.Drawdown(R=absolute_xts,geometric=T, main="Absolute Drawdown - 31 Dec 2019",
               legend.loc="bottomleft", colorset=color)

# Box plot:
chart.Boxplot(R=tail(absolute_xts,12), sort.by=c("mean"), main="1 Year Return Distribution - 31 Dec 2019")

# Risk-return scatter plot:
chart.RiskReturnScatter(R=tail(absolute_xts,12), xlab = 'Volatility', ylab = 'Return', main="1 Year Volatility vs Return - 31 Dec 2019")

# Modified Value at Risk
VaR(R=tail(absolute_xts,12),p=0.95,method="modified")

# Rolling volatility
chart.RollingPerformance(R=absolute_xts,FUN="sd",width=12, legend.loc="topleft", main='Rolling 12-Month Volatility - 31 Dec 2019', colorset=color)
