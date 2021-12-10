import pandas as pd
import odbc
import numpy as np
import datetime
import os
from pandas.tseries.offsets import MonthEnd
from pandas.tseries.offsets import YearEnd
from my_functions import custom_dates as cd

constr = "DRIVER={SQL Server Native Client 11.0};SERVER=ash-prdkblddbao,4071;DATABASE=AshburtonRisk;Trusted_Connection=yes;"
db = odbc.odbc(constr)

datetime_obj_end = cd.bd_t_1

PfCode = ['30107','30113','30117','44008','95101','95104','95106','95107','95109','95110','95902','95815','95921','95923','95935','95955','97239','97240']

data = pd.DataFrame()

for x in PfCode:

    sql = "SELECT * FROM Investment.MaitlandDailyFundPerformance WHERE (ValueDate BETWEEN '2017-12-31' AND " + " ' " + str(datetime_obj_end) + " ' " + ") AND PortfolioCode = " + "'" + x + "'" +""
    df = pd.read_sql(sql, db)
    df.sort_values(by=['ValueDate'], ascending=True, inplace=True)
    df.set_index(['ValueDate'], inplace=True)

    df['CumGrossReturn'] = (df['PercentageChangeGross']/100 + 1).cumprod()
    df['Day'] = float(df.loc[df.index == df.index.max()]['CumGrossReturn'].values / df.loc[df.index == df.index.max() + pd.DateOffset(-1)]['CumGrossReturn'].values -1) if df.loc[df.index == df.index.max() + pd.DateOffset(-1)]['CumGrossReturn'].values.size > 0 else 'NA'
    df['MTD'] = float(df.loc[df.index == df.index.max()]['CumGrossReturn'].values / df.loc[df.index == df.index.max() + MonthEnd(-1)]['CumGrossReturn'].values -1) if df.loc[df.index == df.index.max() + MonthEnd(-1)]['CumGrossReturn'].values.size > 0 else 'NA'
    df['YTD'] = float(df.loc[df.index == df.index.max()]['CumGrossReturn'].values / df.loc[df.index == df.index.max() + YearEnd(-1)]['CumGrossReturn'].values -1) if df.loc[df.index == df.index.max() + YearEnd(-1)]['CumGrossReturn'].values.size > 0 else 'NA'
    df['Rolling 31 Days'] = float(df.loc[df.index == df.index.max()]['CumGrossReturn'].values / df.loc[df.index == df.index.max() + pd.DateOffset(-31)]['CumGrossReturn'].values -1) if df.loc[df.index == df.index.max() + pd.DateOffset(-31)]['CumGrossReturn'].values.size > 0 else 'NA'
    df['Rolling 91 Days'] = float(df.loc[df.index == df.index.max()]['CumGrossReturn'].values / df.loc[df.index == df.index.max() + pd.DateOffset(-91)]['CumGrossReturn'].values -1) if df.loc[df.index == df.index.max() + pd.DateOffset(-91)]['CumGrossReturn'].values.size > 0 else 'NA'
    df['Rolling 365 Days'] = float(df.loc[df.index == df.index.max()]['CumGrossReturn'].values / df.loc[df.index == df.index.max() + pd.DateOffset(-365)]['CumGrossReturn'].values -1) if df.loc[df.index == df.index.max() + pd.DateOffset(-365)]['CumGrossReturn'].values.size > 0 else 'NA'
    df['Rolling 3 Years'] = float(df.loc[df.index == df.index.max()]['CumGrossReturn'].values / df.loc[df.index == df.index.max() + pd.DateOffset(years=-3)]['CumGrossReturn'].values)**(1/3) -1 if df.loc[df.index == df.index.max() + pd.DateOffset(years=-3)]['CumGrossReturn'].values.size > 0 else 'NA'
    df = df.loc[df.index == df.index.max()]
    data = data.append(df)

data.to_excel(r'C:\Users\XTW\Documents\py_testing\fi_daily_performance_input.xlsx')