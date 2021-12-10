import pandas as pd
import odbc
import numpy as np
import datetime
from my_functions import custom_dates as cd
from my_functions import frn_model
import QuantLib as ql

pd.set_option('mode.chained_assignment', None)

funds = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\config\ir_sensitivity.xlsx', sheet_name='funds')
funds = funds.fund_code.astype(str)
funds = "','".join(funds)
funds = "'" + funds + "'"

constr = "DRIVER={SQL Server Native Client 11.0};SERVER=ash-prdkblddbao,4071;DATABASE=AshburtonRisk;Trusted_Connection=yes;"
db = odbc.odbc(constr)

sql = "SELECT InstrumentCode, DataDate, InstrumentShortName, InstrumentLongName, InstrumentTypeDescription, InstrumentCurrency, ValuationMethod, IssueDate, CounterParty, CouponFrequency, InterestRate/100 AS InterestRate, Spread/100 AS Spread, IsDiscountYield, CouponType,FirstCouponDate, PrevCouponDate, NextCouponDate,LastCouponDate, ExDate, MaturityDate, IsResetDates, NextResetDate, ModifiedDuration AS ModifiedDuration_Maitland, DayCountFactor,IssuerCode, IssuerName, DayCountConvention, (InterestRate+Spread) AS Coupon FROM Investment.MaitlandASISAInstruments WHERE DataDate = " + " ' " + cd.t_1 + "'" + " AND PortfolioIDCode IN " + " ( " + (funds) + ")"
df = pd.read_sql(sql, db)

df = df[(df.InstrumentTypeDescription == 'BOND : FOREIGN BOND') & (df.CouponType == 'VLIN')]
df = df.drop_duplicates('InstrumentCode')
df['FaceValue'] = 100.0
df.MaturityDate = pd.to_datetime(df.MaturityDate, format='%Y/%m/%d').dt.strftime("%Y-%m-%d")
df['MaturityDateObj']= df.apply(lambda row :ql.DateParser.parseISO(pd.to_datetime(row['MaturityDate']).strftime('%Y-%m-%d')),axis=1)
df['CouponFrequency#'] = np.where(df.CouponFrequency == 'Q',4, np.where(df.CouponFrequency == 'S',2,np.where(df.CouponFrequency == 'M',12,1)))

sql = "SELECT BondCode, BPSpread/10000 AS BPSpread FROM Investment.vwDailyBondMTMGap WHERE Date = " + " ' " + cd.bd_t_1 + "'" + ""
df_besa = pd.read_sql(sql, db)
df_besa.rename(columns={'BondCode':'InstrumentCode'}, inplace=True)
df = df.merge(df_besa, how='left', on=['InstrumentCode'])
df['BPSpread'] = df['Spread']

# Remove matured instruments
df = df[(df.MaturityDateObj - ql.Date.from_date(pd.to_datetime(cd.bd_t1))) > 1]
df = df.reset_index()

# update bp spreads
df_bp_spread = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\mapping_table\mapping_table.xlsx', sheet_name='foreign_bond_vlin')
df = df.merge(df_bp_spread, how='left', on=['InstrumentCode'])
df['BPSpread'] = np.where(df['BPSpread_y'].isnull(),df['BPSpread_x'],df['BPSpread_y'])
df = df.drop(['BPSpread_x', 'BPSpread_y'], axis=1)

#Pricing
pieces = []
for row in range(len(df)):
	print('foreign_bond_vlin', df.iloc[row,df.columns.get_loc('InstrumentCode')], 'price')
	df_new = frn_model.frn_model(ql.Date.from_date(pd.to_datetime(cd.bd_t1)),df.iloc[row,df.columns.get_loc('MaturityDateObj')],df.iloc[row,df.columns.get_loc('InterestRate')],df.iloc[row,df.columns.get_loc('Spread')],df.iloc[row,df.columns.get_loc('BPSpread')],df.iloc[row,df.columns.get_loc('CouponFrequency#')])
	pieces.append(df_new)
df_new = pd.concat(pieces, ignore_index=True)
df['accrued_interest'] = df_new['accrued_interest']
df['clean_price'] = df_new['clean_price']
df['all_in_price'] = df_new['all_in_price']
df['modified_duration'] = df_new['modified_duration']
df['shift_100d'] = df_new['all_in_price_100d']/df_new['all_in_price']-1
df['shift_75d'] = df_new['all_in_price_75d']/df_new['all_in_price']-1
df['shift_50d'] = df_new['all_in_price_50d']/df_new['all_in_price']-1
df['shift_25d'] = df_new['all_in_price_25d']/df_new['all_in_price']-1
df['shift_25u'] = df_new['all_in_price_25u']/df_new['all_in_price']-1
df['shift_50u'] = df_new['all_in_price_50u']/df_new['all_in_price']-1
df['shift_75u'] = df_new['all_in_price_75u']/df_new['all_in_price']-1
df['shift_100u'] = df_new['all_in_price_100u']/df_new['all_in_price']-1

df = df.drop('index', axis=1)
df.to_csv(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\instrument_data\input\foreign_bond_vlin.csv',index=False)
