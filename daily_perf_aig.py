import pandas as pd
import odbc
import numpy as np
import os

constr = "DRIVER={SQL Server Native Client 11.0};SERVER=ash-prdkblddbao,4071;DATABASE=AshburtonRisk;Trusted_Connection=yes;"
db = odbc.odbc(constr)

writer = pd.ExcelWriter(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\input_data\daily_perf_aig.xlsx')

date_str_start = input('Enter start date (Format yyyy-mm-dd):')
date_str_end = input('Enter end date (Format yyyy-mm-dd):')

sql = "SELECT ValuationDate,PortfolioCode,InstrumentCode,HoldingsNominal,AccruedIncome,MarketValue,(MarketValue/HoldingsNominal) AS AllInPrice  FROM Investment.vwMaitlandHoldings WHERE ValuationDate IN ( " + "'" + date_str_start + "'" + "," + "'" + date_str_end + "'" + ") AND PortfolioCode IN ('95949')"
df = pd.read_sql(sql, db)

# Return Calculation
df['R186_Return'] = float((df[(df['ValuationDate'] == date_str_end) & (df['InstrumentCode'] == 'R186')]['AllInPrice'].values / df[(df['ValuationDate'] == date_str_start) & (df['InstrumentCode'] == 'R186')]['AllInPrice'].values - 1)*100)
df['R2023_Return'] = float((df[(df['ValuationDate'] == date_str_end) & (df['InstrumentCode'] == 'R2023')]['AllInPrice'].values / df[(df['ValuationDate'] == date_str_start) & (df['InstrumentCode'] == 'R2023')]['AllInPrice'].values - 1)*100)
df.to_excel(writer, 'bm_perf', index=False)

# Daily Performance
sql = "SELECT * FROM Investment.MaitlandDailyFundPerformance WHERE ValueDate IN (" + "'" + date_str_end + "'" + ") AND PortfolioCode IN ('95949')"
df = pd.read_sql(sql, db)
df = df.iloc[:, 4:]
df.to_excel(writer, '95949_perf', index=False)

sql = "SELECT * FROM Investment.MaitlandDailyFundPerformance WHERE ValueDate IN (" + "'" + date_str_end + "'" + ") AND PortfolioCode IN ('95950')"
df = pd.read_sql(sql, db)
df = df.iloc[:, 4:]
df.to_excel(writer, '95950_perf', index=False)

sql = "SELECT * FROM Investment.MaitlandDailyFundPerformance WHERE ValueDate IN (" + "'" + date_str_end + "'" + ") AND PortfolioCode IN ('95951')"
df = pd.read_sql(sql, db)
df = df.iloc[:, 4:]
df.to_excel(writer, '95951_perf', index=False)

sql = "SELECT * FROM Investment.MaitlandDailyFundPerformance WHERE ValueDate IN (" + "'" + date_str_end + "'" + ") AND PortfolioCode IN ('95952')"
df = pd.read_sql(sql, db)
df = df.iloc[:, 4:]
df.to_excel(writer, '95952_perf', index=False)

writer.save()