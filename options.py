import pandas as pd
import odbc
import numpy as np
import datetime
from my_functions import custom_dates as cd
from my_functions import ytm_model
from my_functions import price_model
import QuantLib as ql


pd.set_option('mode.chained_assignment', None)

funds = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\config\ir_sensitivity.xlsx', sheet_name='funds')
funds = funds.fund_code.astype(str)
funds = "','".join(funds)
funds = "'" + funds + "'"

constr = "DRIVER={SQL Server Native Client 11.0};SERVER=ash-prdkblddbao,4071;DATABASE=AshburtonRisk;Trusted_Connection=yes;"
db = odbc.odbc(constr)

sql = "SELECT InstrumentCode, DataDate, InstrumentShortName, InstrumentLongName, InstrumentTypeDescription, InstrumentCurrency, ValuationMethod, IssueDate, CounterParty, CouponFrequency, InterestRate/100 AS Coupon, IsDiscountYield, CouponType,FirstCouponDate, PrevCouponDate, NextCouponDate,LastCouponDate, ExDate, MaturityDate, IsResetDates, NextResetDate, ModifiedDuration AS ModifiedDuration_Maitland, DayCountFactor,IssuerCode, IssuerName, DayCountConvention FROM Investment.MaitlandASISAInstruments WHERE DataDate = " + " ' " + cd.t_1 + "'" + " AND PortfolioIDCode IN " + " ( " + (funds) + ")"
df = pd.read_sql(sql, db)

df = df[df.InstrumentTypeDescription == 'BOND : CPI LINKED']
df = df.drop_duplicates('InstrumentCode')
df['FaceValue'] = 100.0
df.MaturityDate = pd.to_datetime(df.MaturityDate, format='%Y/%m/%d').dt.strftime("%Y-%m-%d")
df['MaturityDateObj']= df.apply(lambda row :ql.DateParser.parseISO(pd.to_datetime(row['MaturityDate']).strftime('%Y-%m-%d')),axis=1)
df.IssueDate = pd.to_datetime(df.IssueDate, format='%Y/%m/%d').dt.strftime("%Y-%m-%d")
df['IssueDateObj']= df.apply(lambda row :ql.DateParser.parseISO(pd.to_datetime(row['IssueDate']).strftime('%Y-%m-%d')),axis=1)
df['DataDateObj']= df.apply(lambda row :ql.DateParser.parseISO(pd.to_datetime(row['DataDate']).strftime('%Y-%m-%d')),axis=1)
df['CompoundingFrequency'] = np.where(df.CouponFrequency == 'Q',ql.Quarterly, np.where(df.CouponFrequency == 'S',ql.Semiannual,np.where(df.CouponFrequency == 'M',ql.Monthly,ql.Annual)))
df['BusinessConvention'] = ql.Following
df['DateGeneration'] = ql.DateGeneration.Backward
df['SettlementDays'] = 1

sql = "SELECT InstrumentCode, IIF(HoldingsNominal = 0, 0, (MarketValue - AccruedIncome)/HoldingsNominal*100) AS market_price, IIF(HoldingsNominal = 0, 0, AccruedIncome/HoldingsNominal*100) AS accrued_interest FROM Investment.vwMaitlandHoldings WHERE ValuationDate = " + " ' " + cd.bd_t_1 + "'" + ""
df_ytm = pd.read_sql(sql, db)
df_ytm = df_ytm.drop_duplicates('InstrumentCode')
df = df.merge(df_ytm, how='left', on=['InstrumentCode'])

# Remove matured instruments
df = df[((df.MaturityDateObj - df.DataDateObj) > 1) & df.market_price.notnull()]
df = df.reset_index()

#ytm
pieces = []
for row in range(len(df)):
	print('cpi', df.iloc[row,df.columns.get_loc('InstrumentCode')], 'ytm')
	df_new = ytm_model.ytm_model(df.iloc[row,df.columns.get_loc('DataDateObj')],int(df.iloc[row,df.columns.get_loc('SettlementDays')]), df.iloc[row,df.columns.get_loc('IssueDateObj')] ,df.iloc[row,df.columns.get_loc('MaturityDateObj')],df.iloc[row,df.columns.get_loc('Coupon')],int(df.iloc[row,df.columns.get_loc('CompoundingFrequency')]), int(df.iloc[row,df.columns.get_loc('BusinessConvention')]), int(df.iloc[row,df.columns.get_loc('DateGeneration')]), df.iloc[row,df.columns.get_loc('market_price')], df.iloc[row,df.columns.get_loc('FaceValue')])
	pieces.append(df_new)
df_new = pd.concat(pieces, ignore_index=True)
df['ytm'] = df_new['ytm']

#all_in_price
df['all_in_price'] = df.market_price

#clean_price
pieces = []
for row in range(len(df)):
	print('cpi', df.iloc[row,df.columns.get_loc('InstrumentCode')], 'price')
	df_new = price_model.price_model(df.iloc[row,df.columns.get_loc('DataDateObj')],int(df.iloc[row,df.columns.get_loc('SettlementDays')]), df.iloc[row,df.columns.get_loc('IssueDateObj')] ,df.iloc[row,df.columns.get_loc('MaturityDateObj')],df.iloc[row,df.columns.get_loc('Coupon')],int(df.iloc[row,df.columns.get_loc('CompoundingFrequency')]), int(df.iloc[row,df.columns.get_loc('BusinessConvention')]), int(df.iloc[row,df.columns.get_loc('DateGeneration')]), df.iloc[row,df.columns.get_loc('ytm')], df.iloc[row,df.columns.get_loc('FaceValue')])
	pieces.append(df_new)
df_new = pd.concat(pieces, ignore_index=True)
df['clean_price'] = df_new['clean_price']
df['clean_price_100d'] = df_new['clean_price_100d']
df['clean_price_75d'] = df_new['clean_price_75d']
df['clean_price_50d'] = df_new['clean_price_50d']
df['clean_price_25d'] = df_new['clean_price_25d']
df['clean_price_25u'] = df_new['clean_price_25u']
df['clean_price_50u'] = df_new['clean_price_50u']
df['clean_price_75u'] = df_new['clean_price_75u']
df['clean_price_100u'] = df_new['clean_price_100u']

#all_in_price 
df['all_in_price'] = df.accrued_interest + df.clean_price

#Shifts
df['shift_100d'] = (df.clean_price_100d + df.accrued_interest) / df.all_in_price - 1
df['shift_75d'] = (df.clean_price_75d + df.accrued_interest) / df.all_in_price - 1
df['shift_50d'] = (df.clean_price_50d + df.accrued_interest) / df.all_in_price - 1
df['shift_25d'] = (df.clean_price_25d + df.accrued_interest) / df.all_in_price - 1
df['shift_25u'] = (df.clean_price_25u + df.accrued_interest) / df.all_in_price - 1
df['shift_50u'] = (df.clean_price_50u + df.accrued_interest) / df.all_in_price - 1
df['shift_75u'] = (df.clean_price_75u + df.accrued_interest) / df.all_in_price - 1
df['shift_100u'] = (df.clean_price_100u + df.accrued_interest) / df.all_in_price - 1

df = df.drop('index', axis=1)
df.to_csv(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\instrument_data\input\cpi_bonds.csv',index=False)