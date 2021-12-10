import pandas as pd
import odbc
import numpy as np
import datetime
from my_functions import custom_dates as cd
from my_functions import frn_model
import QuantLib as ql

pd.set_option('mode.chained_assignment', None)

date_str_start = input('Enter start date (Format dd/mm/yyyy):')
format_str = '%d/%m/%Y' # The format
datetime_obj_start = str(datetime.datetime.strptime(date_str_start, format_str).date())
date_str_end = input('Enter end date (Format dd/mm/yyyy):')
format_str = '%d/%m/%Y' # The format
datetime_obj_end = str(datetime.datetime.strptime(date_str_end, format_str).date())
daterange = pd.date_range(datetime_obj_start, datetime_obj_end)

constr = "DRIVER={SQL Server Native Client 11.0};SERVER=ash-prdkblddbao,4071;DATABASE=AshburtonRisk;Trusted_Connection=yes;"
db = odbc.odbc(constr)

df1 = pd.read_csv(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\config\spread_duration\spread_duration.csv')

sql = "SELECT InstrumentCode, ValueDate, InstrumentShortName, InstrumentLongName, InstrumentTypeDescription, InstrumentCurrency, ValuationMethod, IssueDate, CounterParty, CouponFrequency, InterestRate/100 AS InterestRate, Spread/100 AS Spread, IsDiscountYield, CouponType,FirstCouponDate, PrevCouponDate, NextCouponDate,LastCouponDate, ExDate, MaturityDate, IsResetDates, NextResetDate, ModifiedDuration AS ModifiedDuration_Maitland, DayCountFactor,IssuerCode, IssuerName, DayCountConvention, (InterestRate+Spread) AS Coupon FROM AshburtonRisk.Staging.MaitlandASISAInstruments WHERE (ValueDate BETWEEN " + " ' " + str(datetime_obj_start) + " ' " + " AND " + " ' " + str(datetime_obj_end) + " ' " + ") AND InstrumentTypeDescription IN ('BOND : FLOATING RATE NOTE','MMI : FLOATING RATE NOTE') AND PortfolioID IN ('30107','30113','30117','44008','95101','95104','95105','95106','95107','95108','95109','95110','95160','95815','95921','95923','95935','95946','97239','97240','95955','95031','95027','95924','95925','95929','95930','95931','95932','95933','95936','95949','95950','95951','95952','95967','95968','95902')"
df = pd.read_sql(sql, db)

df = df.drop_duplicates(['InstrumentCode','ValueDate'])
df['FaceValue'] = 100.0
df.MaturityDate = pd.to_datetime(df.MaturityDate, format='%Y/%m/%d').dt.strftime("%Y-%m-%d")
df['MaturityDateObj']= df.apply(lambda row :ql.DateParser.parseISO(pd.to_datetime(row['MaturityDate']).strftime('%Y-%m-%d')),axis=1)
df['CouponFrequency#'] = np.where(df.CouponFrequency == 'Q',4, np.where(df.CouponFrequency == 'S',2,np.where(df.CouponFrequency == 'M',12,1)))

sql = "SELECT BondCode, Date, BPSpread/10000 AS BPSpread FROM Investment.vwDailyBondMTMGap WHERE (Date BETWEEN " + " ' " + str(datetime_obj_start) + " ' " + " AND " + " ' " + str(datetime_obj_end) + " ' " + ")"
df_besa = pd.read_sql(sql, db)
df_besa.rename(columns={'BondCode':'InstrumentCode','Date':'ValueDate'}, inplace=True)
df_besa_prev = df_besa.copy()
df_besa_prev['ValueDate'] = df_besa_prev['ValueDate'] + pd.DateOffset(days=1)
df_besa_prev.rename(columns={'BPSpread':'prev_BPSpread'}, inplace=True)

df_besa = df_besa.merge(df_besa_prev, how='left', on=['InstrumentCode','ValueDate'])
df = df.merge(df_besa, how='left', on=['InstrumentCode','ValueDate'])

# Remove matured instruments
# df = df[(df.MaturityDateObj - ql.Date.from_date(pd.to_datetime(df['ValueDate']))) > 1]

df['Diff'] = df['BPSpread'] - df['prev_BPSpread']
df = df[df['Diff'] != 0]
df = df[df['Diff'].notnull()]


df['ValueDateObj']= df.apply(lambda row :ql.DateParser.parseISO(pd.to_datetime(row['ValueDate']).strftime('%Y-%m-%d')),axis=1)
df = df.reset_index()

#Pricing
pieces = []
for row in range(len(df)):
    #df_new = frn_model.frn_model(ql.Date.from_date(pd.to_datetime(dates)),df.iloc[row,df.columns.get_loc('MaturityDateObj')],df.iloc[row,df.columns.get_loc('InterestRate')],df.iloc[row,df.columns.get_loc('Spread')],df.iloc[row,df.columns.get_loc('BPSpread')],df.iloc[row,df.columns.get_loc('CouponFrequency#')])
    df_new = frn_model.frn_model(df.iloc[row,df.columns.get_loc('ValueDateObj')],df.iloc[row,df.columns.get_loc('MaturityDateObj')],df.iloc[row,df.columns.get_loc('InterestRate')],df.iloc[row,df.columns.get_loc('Spread')],df.iloc[row,df.columns.get_loc('BPSpread')],df.iloc[row,df.columns.get_loc('CouponFrequency#')])
    pieces.append(df_new)
df_new = pd.concat(pieces, ignore_index=True)
df['accrued_interest'] = df_new['accrued_interest']
df['clean_price'] = df_new['clean_price']
df['all_in_price'] = df_new['all_in_price']
df['modified_duration'] = df_new['modified_duration']

df1 = df1.append(df, ignore_index=True)
df1['ValueDate'] = pd.to_datetime(df1['ValueDate'])
df1.drop_duplicates(subset=['InstrumentCode','ValueDate'], inplace = True)
  
#df.to_csv(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\instrument_data\input\listed_frn.csv',index=False)
df1.to_csv(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\config\spread_duration\spread_duration.csv',index=False)