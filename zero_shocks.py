import pandas as pd
import odbc
import numpy as np
import datetime
from my_functions import custom_dates as cd

constr = "DRIVER={SQL Server Native Client 11.0};SERVER=ash-prdkblddbao,4071;DATABASE=AshburtonRisk;Trusted_Connection=yes;"
db = odbc.odbc(constr)

sql = "SELECT InstrumentCode, DataDate, InstrumentShortName, InstrumentLongName, InstrumentTypeDescription, InstrumentCurrency, ValuationMethod, IssueDate, CounterParty, CouponFrequency, InterestRate/100 AS InterestRate, Spread/100 AS Spread, IsDiscountYield, CouponType,FirstCouponDate, PrevCouponDate, NextCouponDate,LastCouponDate, ExDate, MaturityDate, IsResetDates, NextResetDate, ModifiedDuration AS ModifiedDuration_Maitland, DayCountFactor,IssuerCode, IssuerName, DayCountConvention, (InterestRate+Spread) AS Coupon FROM Investment.MaitlandASISAInstruments WHERE DataDate = " + " ' " + cd.t_1 + "'" + ""
df = pd.read_sql(sql, db)

df = df[(df.InstrumentTypeDescription == 'BOND : UNLISTED') | (df.InstrumentTypeDescription == 'CALL MONEY') | (df.InstrumentTypeDescription == 'CASH') | (df.InstrumentTypeDescription.str.upper().str[:4] == 'FUND') | (df.InstrumentTypeDescription == 'UNITS')]
df = df.drop_duplicates('InstrumentCode')

df = df[['InstrumentCode','InstrumentLongName','InstrumentTypeDescription']]

df['shift_100d'] = 0.0
df['shift_75d'] = 0.0
df['shift_50d'] = 0.0
df['shift_25d'] = 0.0
df['shift_25u'] = 0.0
df['shift_50u'] = 0.0
df['shift_75u'] = 0.0
df['shift_100u'] = 0.0

df.to_csv(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\instrument_data\input\zero_shocks.csv',index=False)
