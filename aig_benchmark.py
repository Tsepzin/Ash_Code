import pandas as pd
import numpy as np
import odbc
from my_functions import custom_dates as cd

datetime_obj_end = cd.t_1

constr = "DRIVER={SQL Server Native Client 11.0};SERVER=ash-prdkblddbao,4071;DATABASE=AshburtonRisk;Trusted_Connection=yes;"
db = odbc.odbc(constr)

writer = pd.ExcelWriter(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\reports\benchmarks\aig\aig_benchmark.xlsx')

# R208 Return
sql = "SELECT Date, TradeDate, BondCode, AllInPrice, AccruedInterest FROM Investment.vwDailyBondMTMGap WHERE (Date BETWEEN '2020-01-15' AND " + " ' " +  datetime_obj_end + "') AND BondCode = 'R208'"
df = pd.read_sql(sql, db)
df = df.sort_values(['Date'])
df['Coupon'] = np.where((df['AccruedInterest'] < 0) & (df['AccruedInterest'].shift(1) > 0), df['AccruedInterest'].shift(1) - df['AccruedInterest'],0)
df['AllInPriceAdj'] = df['AllInPrice'] + df['Coupon']
df['R208 Return'] = (df['AllInPrice'] + df['Coupon'] - df['AllInPrice'].shift(1)) / df['AllInPrice'].shift(1) *100

# R2023 Return
sql = "SELECT Date, TradeDate, BondCode, AllInPrice, AccruedInterest FROM Investment.vwDailyBondMTMGap WHERE (Date BETWEEN '2020-01-15' AND " + " ' " +  datetime_obj_end + "') AND BondCode = 'R2023'"
df1 = pd.read_sql(sql, db)
df1 = df1.sort_values(['Date'])
df1['Coupon'] = np.where((df1['AccruedInterest'] < 0) & (df1['AccruedInterest'].shift(1) > 0), df1['AccruedInterest'].shift(1) - df1['AccruedInterest'],0)
df1['AllInPriceAdj'] = df1['AllInPrice'] + df1['Coupon']
df1['R2023 Return'] = (df1['AllInPrice'] + df1['Coupon'] - df1['AllInPrice'].shift(1)) / df1['AllInPrice'].shift(1) *100
df1 = df1[['Date','R2023 Return']]

df = df.merge(df1, how='left', on=['Date'])
df = df.dropna()
df['Benchmark Return'] = 0.5 * df['R208 Return'] + 0.5 * df['R2023 Return']
df = df[['Date','TradeDate','R208 Return','R2023 Return','Benchmark Return']]

df.to_excel(writer, 'LDI', index=False)
writer.save()



