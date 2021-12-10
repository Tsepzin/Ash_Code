import pandas as pd
import odbc
import numpy as np
import datetime
import os
from my_functions import custom_dates as cd
from my_functions import option_price
from my_functions import option_delta
from my_functions import implied_vol

# date_str_start = input('Enter start date (Format dd/mm/yyyy):')
# format_str = '%d/%m/%Y' # The format
# datetime_obj_start = str(datetime.datetime.strptime(date_str_start, format_str).date())
date_str_end = input('Enter end date (Format dd/mm/yyyy):')
format_str = '%d/%m/%Y' # The format
datetime_obj_end = str(datetime.datetime.strptime(date_str_end, format_str).date())
# daterange = pd.date_range(str((pd.to_datetime(datetime_obj_start) + pd.DateOffset(days=1)).date()), datetime_obj_end)

# writer = pd.ExcelWriter(r'C:\Users\XTW\Documents\py_testing\ ' + str(PfCode) + '_Attribution Report_' + datetime_obj_start + '_' + datetime_obj_end + '.xlsx')

constr = "DRIVER={SQL Server Native Client 11.0};SERVER=ash-prdkblddbao,4071;DATABASE=AshburtonRisk;Trusted_Connection=yes;"
db = odbc.odbc(constr)

sql = "SELECT ValueDate,InstrumentCode, InstrumentLongName, InstrumentTypeDescription, Delta, FuturesExpiryDate, StrikePrice, ContractType FROM AshburtonRisk.Staging.MaitlandASISAInstruments WHERE ValueDate = " + " ' " + str(datetime_obj_end) + " ' " + " AND InstrumentTypeDescription = 'OPTION : BOND FUTURE'"
df = pd.read_sql(sql, db)
df.drop_duplicates(['InstrumentCode'], inplace=True)
df['RiskFree'] = 0.00

sql = "SELECT ValuationDate, InstrumentCode, BaseEffectiveExposure, HoldingsNominal, MarketPrice FROM Investment.vwMaitlandHoldings WHERE ValuationDate = " + " ' " + str(datetime_obj_end) + " ' " + ""
df1 = pd.read_sql(sql, db)

df = df.merge(df1, on=['InstrumentCode'], how = 'left')
df.drop_duplicates(['InstrumentCode'], inplace=True)

df['UnderlyingPrice'] = df['BaseEffectiveExposure']/(df['HoldingsNominal']*df['Delta']*1000)

df['T'] = (pd.to_datetime(df['FuturesExpiryDate']) - pd.to_datetime(df['ValuationDate'])).dt.days/365

df['ImpliedVolatility'] = df.apply(lambda x: implied_vol.implied_vol(x['UnderlyingPrice'], x['StrikePrice'], x['T'], x['MarketPrice']/1000, x['RiskFree'], x['ContractType']), axis=1)

    
df['DeltaNew'] = df.apply(lambda x: option_delta.option_delta(x['UnderlyingPrice'], x['StrikePrice'], x['T'], x['RiskFree'], x['ImpliedVolatility'], x['ContractType']), axis=1)
    
df['shift_100d'] = df.apply(lambda x: ((option_delta.option_delta(x['UnderlyingPrice']*(1-100/10000), x['StrikePrice'], x['T'], x['RiskFree'], x['ImpliedVolatility'], x['ContractType']) * x['UnderlyingPrice']*(1-100/10000)) / (x['UnderlyingPrice']*x['DeltaNew']) - 1) * x['DeltaNew'], axis=1)
    


df.to_csv(r'C:\Users\XTW\Documents\py_testing\option_bond_future.csv', index=False)
