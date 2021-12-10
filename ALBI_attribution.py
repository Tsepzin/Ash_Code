import pandas as pd
import odbc
import numpy as np
import datetime
import os
from my_functions import custom_dates as cd


date_str_start = input('Enter start date (Format dd/mm/yyyy):')
format_str = '%d/%m/%Y' # The format
datetime_obj_start = str(datetime.datetime.strptime(date_str_start, format_str).date())
date_str_end = input('Enter end date (Format dd/mm/yyyy):')
format_str = '%d/%m/%Y' # The format
datetime_obj_end = str(datetime.datetime.strptime(date_str_end, format_str).date())
daterange = pd.date_range(str((pd.to_datetime(datetime_obj_start) + pd.DateOffset(days=1)).date()), datetime_obj_end)

writer = pd.ExcelWriter(r'C:\Users\XTW\Documents\py_testing\ALBI Attribution Report_' + datetime_obj_start + '_' + datetime_obj_end + '.xlsx')

constr = "DRIVER={SQL Server Native Client 11.0};SERVER=ash-prdkblddbao,4071;DATABASE=AshburtonRisk;Trusted_Connection=yes;"
db = odbc.odbc(constr)

df = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\config\AlbiWeights.xlsx', sheet_name='Weight')

df = df.melt(id_vars='AsDate', var_name='InstrumentCode', value_name='HoldingsNominal')

df = df[df['HoldingsNominal'].notnull()]
df = df[df['HoldingsNominal'] != 0]

df = df[(df['AsDate'] >= pd.to_datetime(datetime_obj_start)) & (df['AsDate'] <= pd.to_datetime(datetime_obj_end))]
df.rename(columns={'AsDate': 'ValuationDate'}, inplace=True)

# JSE Prices
sql = "SELECT Date, BondCode, AllInPrice, CleanPrice, AccruedInterest, BPSpread, MTM, ModifiedDuration, Convexity FROM Investment.vwDailyBondMTMGap WHERE (Date BETWEEN " + " ' " + str(datetime_obj_start) + " ' " + " AND " + " ' " + str(datetime_obj_end) + " ' " + ")"
jse = pd.read_sql(sql, db)
jse.rename(columns={'Date': 'ValuationDate', 'BondCode': 'InstrumentCode'}, inplace=True)

df = df.merge(jse, how='left', on=['InstrumentCode','ValuationDate'])

df['MarketValue'] = df['HoldingsNominal']*df['AllInPrice']

# TotalMarketValue and Weight
df1 = df.groupby('ValuationDate', as_index=False)['MarketValue'].sum()
df1.rename(columns={'MarketValue': 'TotalMarketValue'}, inplace=True)
df = df.merge(df1, how='left', on=['ValuationDate'])
df['Weight'] = df['MarketValue'] / df['TotalMarketValue']

# Previous day's values
df_prev = df[['ValuationDate','InstrumentCode','Weight','AllInPrice','AccruedInterest','BPSpread', 'MTM','ModifiedDuration','Convexity']]
df_prev['ValuationDate'] = df_prev['ValuationDate'] + pd.DateOffset(days=1)
df_prev.rename(columns={'Weight': 'prev_Weight','AllInPrice':'prev_AllInPrice','AccruedInterest':'prev_AccruedInterest','BPSpread':'prev_BPSpread','MTM':'prev_MTM','ModifiedDuration':'prev_ModifiedDuration','Convexity':'prev_Convexity'}, inplace=True)
df = df.merge(df_prev, how='left', on=['InstrumentCode','ValuationDate'])

# Drop the first day
df = df[df['ValuationDate'] != pd.to_datetime(datetime_obj_start)]

# Create PortfolioCode and InstrumentTypeDescription
df['PortfolioCode'] = 'ALBI'
df['InstrumentTypeDescription'] = 'BOND : FIXED RATE BOND'

# Returns
df['Return'] = np.where((df['AccruedInterest'] < 0) & (df['prev_AccruedInterest'] > 0),(df['AllInPrice'] + df['prev_AccruedInterest'] - df['AccruedInterest']) / df['prev_AllInPrice'] - 1 , df['AllInPrice'] / df['prev_AllInPrice'] - 1)
df['Nominal Carry Return'] = df['prev_MTM']/365/100
df['Real Carry Return'] = 0.0
df['Repo Return'] = 0.0
df['Inflation Return'] = 0.0
df['Spread Return'] = np.where((df['BPSpread'].isnull()) | (df['prev_BPSpread'].isnull()),0,-df['prev_ModifiedDuration']*(df['BPSpread'] - df['prev_BPSpread'])/10000)
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