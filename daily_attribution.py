import pandas as pd
import odbc
import numpy as np
import datetime
import os
from my_functions import custom_dates as cd


PfCode = input('Enter PortfolioCode: ')
date_str_start = input('Enter start date (Format dd/mm/yyyy):')
format_str = '%d/%m/%Y' # The format
datetime_obj_start = str(datetime.datetime.strptime(date_str_start, format_str).date())
date_str_end = input('Enter end date (Format dd/mm/yyyy):')
format_str = '%d/%m/%Y' # The format
datetime_obj_end = str(datetime.datetime.strptime(date_str_end, format_str).date())
daterange = pd.date_range(str((pd.to_datetime(datetime_obj_start) + pd.DateOffset(days=1)).date()), datetime_obj_end)

writer = pd.ExcelWriter(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\reports\attribution\out\ ' + str(PfCode) + '_Attribution Report_' + datetime_obj_start + '_' + datetime_obj_end + '.xlsx')
# writer = pd.ExcelWriter(r'Y:\Risk Management\Investment Analytics\Python\take_on\reports\attribution\out\ ' + str(PfCode) + '_Attribution Report_' + datetime_obj_start + '_' + datetime_obj_end + '.xlsx')

constr = "DRIVER={SQL Server Native Client 11.0};SERVER=ash-prdkblddbao,4071;DATABASE=AshburtonRisk;Trusted_Connection=yes;"
db = odbc.odbc(constr)

map_table = pd.read_csv(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\config\spread_duration\map_table.csv')

sql = "SELECT ValuationDate,PortfolioCode, InstrumentCode, (BaseEffectiveExposure/TotalMarketValue) AS Weight, (BaseEffectiveExposure/NULLIF(HoldingsNominal,0)) AS AllInPrice, MarketPrice, AccruedIncome, HoldingsNominal, BaseEffectiveExposure FROM Investment.vwMaitlandHoldings WHERE (ValuationDate BETWEEN " + " ' " + str(datetime_obj_start) + " ' " + " AND " + " ' " + str(datetime_obj_end) + " ' " + ") AND PortfolioCode = " + "'" + PfCode + "'" +""
df = pd.read_sql(sql, db)
#df = df.merge(map_table, how='left', on=['InstrumentCode'])
#df['InstrumentCode'] = np.where(df['InstrumentCode2'].str[:3] == 'ZAM',df['InstrumentCode2'], df['InstrumentCode'])
#df = df.drop([df['InstrumentCode2'], axis=1)    

# Previous day's values
df_prev = df[['ValuationDate','InstrumentCode','Weight','AllInPrice','MarketPrice','AccruedIncome','BaseEffectiveExposure','HoldingsNominal']]
df_prev['ValuationDate'] = df_prev['ValuationDate'] + pd.DateOffset(days=1)
df_prev.rename(columns={'Weight': 'prev_Weight','AllInPrice':'prev_AllInPrice','MarketPrice':'prev_MarketPrice','AccruedIncome':'prev_AccruedIncome', 'BaseEffectiveExposure':'prev_BaseEffectiveExposure','HoldingsNominal':'prev_HoldingsNominal'}, inplace=True)

df = df.merge(df_prev, how='left', on=['InstrumentCode','ValuationDate'])

sql = "SELECT ValueDate,InstrumentCode, InstrumentLongName, InstrumentTypeDescription, Delta, (InterestRate/100) AS CouponRate, ModifiedDuration FROM AshburtonRisk.Staging.MaitlandASISAInstruments WHERE (ValueDate BETWEEN " + " ' " + str(datetime_obj_start) + " ' " + " AND " + " ' " + str(datetime_obj_end) + " ' " + ") AND PortfolioID = " + "'" + PfCode + "'" +""
df1 = pd.read_sql(sql, db)
#df1 = df1.merge(map_table, how='left', on=['InstrumentCode'])
#df1['InstrumentCode'] = np.where(df1['InstrumentCode2'].str[:3] == 'ZAM',df1['InstrumentCode2'], df1['InstrumentCode'])
#df1 = df1.drop([df1['InstrumentCode2'], axis=1)  
df1.rename(columns={'ValueDate': 'ValuationDate'}, inplace=True)
df1 = df1.drop_duplicates(['InstrumentCode','ValuationDate'])

df = df.merge(df1, how='left', on=['InstrumentCode','ValuationDate'])

df1 = df1.drop_duplicates(['InstrumentCode','ValuationDate'])

df1['ValuationDate'] = df1['ValuationDate'] + pd.DateOffset(days=1)
df1 = df1.drop(['InstrumentTypeDescription','InstrumentLongName'], axis=1)
df1.rename(columns={'Delta': 'prev_Delta', 'CouponRate': 'prev_CouponRate', 'ModifiedDuration': 'prev_ModifiedDuration'}, inplace=True)
df = df.merge(df1, how='left', on=['InstrumentCode','ValuationDate'])

sql = "SELECT ValueDate,InstrumentCode, NextCouponDate FROM AshburtonRisk.Staging.MaitlandASISAInstruments WHERE (ValueDate BETWEEN " + " ' " + str(pd.to_datetime(datetime_obj_start) + pd.DateOffset(days=-5)) + " ' " + " AND " + " ' " + str(pd.to_datetime(datetime_obj_end) + pd.DateOffset(days=-5)) + " ' " + ") AND PortfolioID = " + "'" + PfCode + "'" +""
df2 = pd.read_sql(sql, db)
#df2 = df2.merge(map_table, how='left', on=['InstrumentCode'])
#df2['InstrumentCode'] = np.where(df2['InstrumentCode2'].str[:3] == 'ZAM',df2['InstrumentCode2'], df2['InstrumentCode'])
#df2 = df2.drop([df2['InstrumentCode2'], axis=1)  
df2['ValueDate'] = df2['ValueDate'] + pd.DateOffset(days=5)
df2.rename(columns={'ValueDate': 'ValuationDate'}, inplace=True)
df2 = df2.drop_duplicates(['InstrumentCode','ValuationDate'])
df2['NextCouponDate'] = pd.to_datetime(df2['NextCouponDate'], format='%Y/%m/%d').dt.strftime("%Y-%m-%d")

df = df.merge(df2, how='left', on=['InstrumentCode','ValuationDate'])

# CPI
cpi_returns = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\Input\CPI Intepolated numbers.xlsm', sheet_name = 'Intepolated_Numbers', usecols = [0,6])
cpi_returns.rename(columns={'Date': 'ValuationDate'}, inplace=True)
df = df.merge(cpi_returns, how='left', on=['ValuationDate'])

# JSE
sql = "SELECT Date, BondCode, BPSpread, Convexity, MTM FROM Investment.vwDailyBondMTMGap WHERE (Date BETWEEN " + " ' " + str(datetime_obj_start) + " ' " + " AND " + " ' " + str(datetime_obj_end) + " ' " + ")"
jse = pd.read_sql(sql, db)
jse.rename(columns={'Date': 'ValuationDate', 'BondCode': 'InstrumentCode'}, inplace=True)
prev_jse = jse.copy()
prev_jse['ValuationDate'] = prev_jse['ValuationDate'] + pd.DateOffset(days=1)
prev_jse.rename(columns={'BPSpread': 'prev_BPSpread','Convexity': 'prev_Convexity', 'MTM': 'prev_MTM'}, inplace=True)
jse = jse.merge(prev_jse, how='left', on=['InstrumentCode','ValuationDate'])

df = df.merge(jse, how='left', on=['InstrumentCode','ValuationDate'])

# # Spread Duration
# # spread_dur = pd.read_csv(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\spread_duration\spread_duration.csv')
# df5 = pd.DataFrame()
# for filename in os.listdir(r'C:\Users\XTW\Documents\py_testing\spread_duration\data'):
    # df6 = pd.read_csv(os.path.join(r'C:\Users\XTW\Documents\py_testing\spread_duration\data',filename))
    # df5 = df5.append(df6)
    # df5.to_csv(r'C:\Users\XTW\Documents\py_testing\spread_duration\spread_duration.csv', index=False)
spread_dur = pd.read_csv(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\config\spread_duration\spread_duration.csv')
spread_dur.rename(columns={'ValueDate': 'ValuationDate','modified_duration': 'SpreadDuration'}, inplace=True)
spread_dur = spread_dur.drop_duplicates(['InstrumentCode','ValuationDate'])
spread_dur = spread_dur[['InstrumentCode','ValuationDate','SpreadDuration']]
spread_dur['ValuationDate'] = pd.to_datetime(spread_dur['ValuationDate'])
df = df.merge(spread_dur, how='left', on=['InstrumentCode','ValuationDate'])
df['prev_ModifiedDuration'] = np.where(df['InstrumentTypeDescription'] == 'BOND : FLOATING RATE NOTE',df['SpreadDuration'],df['prev_ModifiedDuration'])

# Coupon
df['Coupon'] = np.where(pd.to_datetime(df['ValuationDate'], format='%Y/%m/%d').dt.strftime("%Y-%m-%d") == df['NextCouponDate'], (df['AccruedIncome'] + df['prev_AccruedIncome'])/df['HoldingsNominal'],0)

# Fixing the price
df['AllInPrice'] = np.where(df['InstrumentTypeDescription'].str.contains('OPTION'),np.where(df['Delta']==0,0,df['BaseEffectiveExposure']/(df['HoldingsNominal']*df['Delta']*100000)), df['AllInPrice'])
df['AllInPrice'] = np.where((df['InstrumentTypeDescription'] == 'CASH') | (df['InstrumentTypeDescription'] == 'CALL MONEY'),1, df['AllInPrice'])
df['prev_AllInPrice'] = np.where(df['InstrumentTypeDescription'].str.contains('OPTION') ,np.where(df['prev_Delta']==0,0,df['prev_BaseEffectiveExposure']/(df['prev_HoldingsNominal']*df['prev_Delta']*100000)), df['prev_AllInPrice'])
df['prev_AllInPrice'] = np.where((df['InstrumentTypeDescription'] == 'CASH') | (df['InstrumentTypeDescription'] == 'CALL MONEY'),1, df['prev_AllInPrice'])

df['prev_YTM'] = np.where((df['prev_MTM'] == 0) | (df['prev_MTM'].isnull()), df['prev_CouponRate'],df['prev_MTM']/100)

# Adjustments
adj = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\config\Adj.xlsx')
adj['PortfolioCode'] = adj['PortfolioCode'].astype('str')
df = df.merge(adj, how='left', on=['InstrumentCode','ValuationDate','PortfolioCode'])

# Returns
df['Return'] = np.where((df['AllInPrice'] == 0) | (df['prev_AllInPrice'] == 0), 0, (df['AllInPrice'] + df['Coupon']) / df['prev_AllInPrice'] - 1)
df['Return'] = np.where(df['InstrumentTypeDescription'].str.contains('OPTION') & (df['Return'] >0.5), 0, df['Return'])
df['Return'] = np.where(df['InstrumentTypeDescription'].str.contains('FUND') & (df['Return'] < 0), 0.0002, df['Return'])
df['Return'] = np.where(df['InstrumentTypeDescription'].str.contains('FUND') & (df['Return'] > 0.002), 0.0002, df['Return'])
df['Return'] = np.where((df['InstrumentTypeDescription'] == 'BOND : UNLISTED') & (df['Return'] < 0), 0.0002, df['Return'])
df['Return'] = np.where(df['AdjReturn'].notnull() , df['AdjReturn'], df['Return'])
# df['Return'] = np.where((df['InstrumentTypeDescription'] == 'BOND : UNLISTED') & (df['Return'] > 0.002), 0.0002, df['Return'])
df['Nominal Carry Return'] = np.where(df['InstrumentTypeDescription'] != 'BOND : CPI LINKED',df['prev_YTM']/365,0)
df['Nominal Carry Return'] = np.where(df['InstrumentTypeDescription'].str.contains('FUND') | (df['InstrumentTypeDescription'] == 'BOND : UNLISTED'), df['Return'], df['Nominal Carry Return'])
df['Nominal Carry Return'] = np.where(df.InstrumentLongName.str.upper().str[:4] == 'REPO', 0, df['Nominal Carry Return'])
df['Real Carry Return'] = np.where(df['InstrumentTypeDescription'] == 'BOND : CPI LINKED',df['prev_YTM']/365,0)
df['Repo Return'] = np.where(df.InstrumentLongName.str.upper().str[:4] == 'REPO', df['Return'], 0)
df['Inflation Return'] = np.where(df['InstrumentTypeDescription'] == 'BOND : CPI LINKED',df['CPI_Return'],0)
df['Spread Return'] = np.where((df['BPSpread'] == 0) | (df['prev_BPSpread'] == 0),0,-df['prev_ModifiedDuration']*(df['BPSpread'] - df['prev_BPSpread'])/10000)
df['Convexity Return'] = np.where((df['Convexity'] == 0) | (df['prev_Convexity'] == 0),0,0.5*df['prev_Convexity']*((df['MTM'] - df['prev_MTM'])/100)**2)

# Contribution
df['Contribution'] = df['prev_Weight']*df['Return']
df['Nominal Carry Contribution'] = df['prev_Weight']*df['Nominal Carry Return']
df['Real Carry Contribution'] = df['prev_Weight']*df['Real Carry Return']
df['Repo Contribution'] = df['prev_Weight']*df['Repo Return']
df['Inflation Contribution'] = df['prev_Weight']*df['Inflation Return']
df['Spread Contribution'] = df['prev_Weight']*df['Spread Return']
df['Convexity Contribution'] = df['prev_Weight']*df['Convexity Return']

# Chain-linking
df['Return'] = np.log(1 + df['Return'])
df['Contribution'] = np.log(1 + df['Contribution'])
df['Nominal Carry Return'] = np.log(1 + df['Nominal Carry Return'])
df['Nominal Carry Contribution'] = np.log(1 + df['Nominal Carry Contribution'])
df['Real Carry Return'] = np.log(1 + df['Real Carry Return'])
df['Real Carry Contribution'] = np.log(1 + df['Real Carry Contribution'])
df['Repo Return'] = np.log(1 + df['Repo Return'])
df['Repo Contribution'] = np.log(1 + df['Repo Contribution'])
df['Inflation Return'] = np.log(1 + df['Inflation Return'])
df['Inflation Contribution'] = np.log(1 + df['Inflation Contribution'])
df['Spread Return'] = np.log(1 + df['Spread Return'])
df['Spread Contribution'] = np.log(1 + df['Spread Contribution'])
df['Convexity Return'] = np.log(1 + df['Convexity Return'])
df['Convexity Contribution'] = np.log(1 + df['Convexity Contribution'])


df = df[df['ValuationDate'] != datetime_obj_start]

# Daily Performance
sql = "SELECT ValueDate, (PercentageChangeGross/100) AS GrossReturn FROM Investment.MaitlandDailyFundPerformance WHERE (ValueDate BETWEEN " + " ' " + str(pd.to_datetime(datetime_obj_start) + pd.DateOffset(days=1)) + " ' " + " AND " + " ' " + str(pd.to_datetime(datetime_obj_end) + pd.DateOffset(days=0)) + " ' " + ") AND PortfolioCode = " + "'" + PfCode + "'" +""
df_perf = pd.read_sql(sql, db)
df_perf.rename(columns={'ValueDate': 'ValuationDate'}, inplace=True)

contr = pd.pivot_table(df,index=['ValuationDate'], values = ['Contribution'], aggfunc=np.sum).reset_index()

df_perf = df_perf.merge(contr, how='left', on=['ValuationDate'])
df_perf['Diff'] = df_perf['GrossReturn'] - df_perf['Contribution']
df_perf['ValuationDate'] = df_perf['ValuationDate'].apply(lambda x: pd.to_datetime(x).date())

df_perf.to_excel(writer, 'Daily Returns', index=False)
df.to_excel(writer, 'Raw Data', index=False)

# Report
ret = pd.pivot_table(df,index=['PortfolioCode','InstrumentCode','InstrumentTypeDescription'], values = ['Return'], aggfunc=np.sum).reset_index()
contr = pd.pivot_table(df,index=['PortfolioCode','InstrumentCode','InstrumentTypeDescription'], values = ['Contribution'], aggfunc=np.sum ).reset_index()
nominal_c = pd.pivot_table(df,index=['PortfolioCode','InstrumentCode','InstrumentTypeDescription'], values = ['Nominal Carry Contribution'], aggfunc=np.sum ).reset_index()
real_c = pd.pivot_table(df,index=['PortfolioCode','InstrumentCode','InstrumentTypeDescription'], values = ['Real Carry Contribution'], aggfunc=np.sum ).reset_index()
repo_c = pd.pivot_table(df,index=['PortfolioCode','InstrumentCode','InstrumentTypeDescription'], values = ['Repo Contribution'], aggfunc=np.sum ).reset_index()
inflation_c = pd.pivot_table(df,index=['PortfolioCode','InstrumentCode','InstrumentTypeDescription'], values = ['Inflation Contribution'], aggfunc=np.sum ).reset_index()
spread_c = pd.pivot_table(df,index=['PortfolioCode','InstrumentCode','InstrumentTypeDescription'], values = ['Spread Contribution'], aggfunc=np.sum ).reset_index()
convexity_c = pd.pivot_table(df,index=['PortfolioCode','InstrumentCode','InstrumentTypeDescription'], values = ['Convexity Contribution'], aggfunc=np.sum ).reset_index()
df = pd.pivot_table(df,index=['PortfolioCode','InstrumentCode','InstrumentTypeDescription'], values = ['Weight'], aggfunc=np.sum).reset_index()
length = (pd.to_datetime(datetime_obj_end).date()-pd.to_datetime(datetime_obj_start).date()).days
df['Weight'] = df['Weight']/length
df = df.merge(ret, how='left', on=['PortfolioCode','InstrumentCode','InstrumentTypeDescription'])
df = df.merge(spread_c, how='left', on=['PortfolioCode','InstrumentCode','InstrumentTypeDescription'])
df = df.merge(convexity_c, how='left', on=['PortfolioCode','InstrumentCode','InstrumentTypeDescription'])
df = df.merge(inflation_c, how='left', on=['PortfolioCode','InstrumentCode','InstrumentTypeDescription'])
df = df.merge(nominal_c, how='left', on=['PortfolioCode','InstrumentCode','InstrumentTypeDescription'])
df = df.merge(real_c, how='left', on=['PortfolioCode','InstrumentCode','InstrumentTypeDescription'])
df = df.merge(repo_c, how='left', on=['PortfolioCode','InstrumentCode','InstrumentTypeDescription'])
df = df.merge(contr, how='left', on=['PortfolioCode','InstrumentCode','InstrumentTypeDescription'])
df['Yield Curve Contribution'] = df['Contribution'] - df['Spread Contribution'] - df['Convexity Contribution'] - df['Inflation Contribution'] - df['Nominal Carry Contribution'] - df['Real Carry Contribution'] - df['Repo Contribution']

# Sorting columns
df.rename(columns={'PortfolioCode': 'Portfolio Code','InstrumentCode': 'Instrument Code', 'InstrumentTypeDescription': 'Instrument Type'}, inplace=True)
df = df[['Portfolio Code','Instrument Code','Instrument Type','Weight','Return','Spread Contribution', 'Convexity Contribution', 'Inflation Contribution', 'Nominal Carry Contribution', 'Real Carry Contribution', 'Repo Contribution', 'Yield Curve Contribution', 'Contribution']]

df[['Return','Spread Contribution','Convexity Contribution','Inflation Contribution','Nominal Carry Contribution','Real Carry Contribution','Repo Contribution','Yield Curve Contribution','Contribution']] = np.where(len(daterange) > 365,(1+df[['Return','Spread Contribution','Convexity Contribution','Inflation Contribution','Nominal Carry Contribution','Real Carry Contribution','Repo Contribution','Yield Curve Contribution','Contribution']])**(365/len(daterange))-1,df[['Return','Spread Contribution','Convexity Contribution','Inflation Contribution','Nominal Carry Contribution','Real Carry Contribution','Repo Contribution','Yield Curve Contribution','Contribution']])

df.to_excel(writer, 'Attribution', index=False)
workbook  = writer.book
worksheet = writer.sheets['Attribution']
percentage_center = workbook.add_format({'num_format': '0.000%', 'align': 'center', 'valign': 'vcenter'})
left = workbook.add_format({'align': 'left', 'valign': 'vleft'})
worksheet.set_column('D:M', 12, percentage_center)
worksheet.set_column('B:B', 16, left)
worksheet.set_column('C:C', 27, left)
writer.save()
