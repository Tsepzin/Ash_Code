import pandas as pd
import odbc
import numpy as np
import datetime
from my_functions import custom_dates as cd

# date_str_start = input('Enter start date (Format dd/mm/yyyy):')
# format_str = '%d/%m/%Y' # The format
# datetime_obj_start = str(datetime.datetime.strptime(date_str_start, format_str).date())

# date_str_end = input('Enter end date (Format dd/mm/yyyy):')
# format_str = '%d/%m/%Y' # The format
# datetime_obj_end = str(datetime.datetime.strptime(date_str_end, format_str).date())

datetime_obj_start = cd.bd_t_1
datetime_obj_end = cd.t_1

daterange = pd.date_range(datetime_obj_start , datetime_obj_end)

constr = "DRIVER={SQL Server Native Client 11.0};SERVER=ash-prdkblddbao,4071;DATABASE=AshburtonRisk;Trusted_Connection=yes;"
db = odbc.odbc(constr)

for dates in daterange:

	sql = "SELECT BondCode, Date, Maturity, Coupon, BPSpread, MTM, AllInPrice, CleanPrice, AccruedInterest, ReferenceCPI FROM Investment.vwDailyBondMTMGap WHERE Date = " + " ' " + str(dates.date()) + "'" + " AND BondCode IN ('I2038')"
	df = pd.read_sql(sql, db)

	sql = "SELECT BondCode, BPSpread AS Prev_BPSpread, MTM AS Prev_MTM, AllInPrice AS Prev_AllInPrice, AccruedInterest AS Prev_AccruedInterest, ModifiedDuration AS Prev_ModifiedDuration,Convexity AS Prev_Convexity, ReferenceCPI AS Prev_ReferenceCPI FROM Investment.vwDailyBondMTMGap WHERE Date = " + " ' " + str((pd.to_datetime(dates) + pd.DateOffset(days=-1)).date()) + "'" + " AND BondCode IN ('I2038')"
	df_prev = pd.read_sql(sql, db)

	df = df.merge(df_prev, how='left', on=['BondCode'])



	df_w = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\config\AlbiWeights.xlsx', sheet_name='GILBX15 Weight')
	df_w = df_w[df_w['AsDate'] == pd.to_datetime(str((pd.to_datetime(dates) + pd.DateOffset(days=-1)).date()))].T.reset_index()
	df_w = df_w.iloc[1:,]
	df_w.rename(columns={'index': 'BondCode',df_w.columns[1]: 'nominal'}, inplace=True)

	df = df.merge(df_w, how='left', on=['BondCode'])

	df['weight'] = df.nominal * df.Prev_AllInPrice
	df['weight'] = df.weight / df.weight.sum()
	df['coupon_adj'] = np.where((df.AccruedInterest < 0) & (df.Prev_AccruedInterest > 0), df.Prev_AccruedInterest - df.AccruedInterest, 0)
	df['return'] = (df.AllInPrice + df.coupon_adj)/df.Prev_AllInPrice - 1
	df['return_spread'] = 0.0172
	df['return'] = (1+df['return'])*(1+df['return_spread'])**(1/365)-1
	df['total_return'] = (df.weight*df['return']).sum()
	df['cpi_return'] = df.ReferenceCPI / df.Prev_ReferenceCPI - 1

	df['Spread Contribution'] = 0.0
	df['Convexity Contribution'] = df['weight']*0.5*df['Prev_Convexity']*((df['MTM'] - df['Prev_MTM'])/100)**2
	df['Inflation Contribution'] = df.cpi_return*df['weight']
	df['ILBCarry Contribution'] = df['Prev_MTM']*1/365/100
	df['Return Contribution'] = df['return'] * df['weight']
	df['Yield Curve Contribution'] = (1+df['Return Contribution'])/((1+df['Spread Contribution'])*(1+df['Convexity Contribution'])*(1+df['Inflation Contribution'])*(1+df['ILBCarry Contribution'])) - 1
	df['Portfolio Code'] = 'GILBX15'
	df.rename(columns={'BondCode': 'Instrument Code','weight':'Weight','return':'Return'}, inplace=True)
	df = df[['Portfolio Code','Instrument Code','Weight','Return','Spread Contribution','Convexity Contribution','Inflation Contribution','ILBCarry Contribution','Yield Curve Contribution','Return Contribution']]
	df = df.append(df.sum(), ignore_index=True)
	df['Portfolio Code'].iloc[1] = 'Total'
	df['Instrument Code'].iloc[1] = ''
	df.to_csv(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\reports\liability_models\satu\satu_bm_' + str(dates.date()) + '.csv', index=False)
