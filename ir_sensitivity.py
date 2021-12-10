import pandas as pd
import odbc
import numpy as np
import datetime
from my_functions import custom_dates as cd

PfCode = ['95106','30126','95922','30117','95110','95921','44008','30107','95923','30113','95027','95924','95925','95107','95806','95204','30127','95101','95109']

constr = "DRIVER={SQL Server Native Client 11.0};SERVER=ash-prdkblddbao,4071;DATABASE=AshburtonRisk;Trusted_Connection=yes;"
db = odbc.odbc(constr)

df_input = pd.read_csv(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\instrument_data\input\combine.csv')

for i in PfCode:
	sql = "SELECT InstrumentCode, EffectiveExpoure FROM Investment.vwMaitlandHoldings WHERE ValuationDate = " + " '" + cd.t_1 + "'" + " AND PortfolioCode = " + "'" + i + "'" +""
	df = pd.read_sql(sql, db)
	
	df['weight'] = df.EffectiveExpoure/df.EffectiveExpoure.sum()
	df = df[['InstrumentCode','weight']]
	df = df.merge(df_input, how='left', on=['InstrumentCode'])
	df = df[['InstrumentCode','InstrumentLongName','InstrumentTypeDescription','weight','shift_100d','shift_75d','shift_50d','shift_25d','shift_25u','shift_50u','shift_75u','shift_100u']]
	df.to_csv(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\reports\ir_sensitivity\ir_sensitivity_' + str(i) + '.csv', index=False)