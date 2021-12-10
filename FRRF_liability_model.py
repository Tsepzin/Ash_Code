# Effective date: 01 July 2018
import pandas as pd
import odbc
import numpy as np
import datetime
from pandas.tseries.offsets import MonthEnd
import scipy.interpolate
from scipy.optimize import newton
from QuantLib import *
from dateutil import parser
from my_functions import custom_dates as cd

# silence warnings
import warnings
warnings.filterwarnings('ignore')

def excel_date(date1):
    temp = datetime.datetime(1899, 12, 30)  
    delta = date1 - temp
    return delta.dt.days + delta.dt.seconds / 86400
	
def xnpv(rate, values, dates):
	'''Replicates the XNPV() function'''
	min_date = min(dates)
	return sum([value/(1+rate)**((date-min_date).days/365)
	for value, date
	in zip(values,dates)
	])
	
def xirr(values, dates):
		'''Replicate the XIRR() function'''
		return newton (lambda r: xnpv(r, values, dates),0)	

# Set the curve end-date
curve_end_date_2 = '2142-06-24'


date_str_start = input('Enter start date (Format dd/mm/yyyy):')
format_str = '%d/%m/%Y' # The format
datetime_obj_start = str(datetime.datetime.strptime(date_str_start, format_str).date())

date_str_end = input('Enter end date (Format dd/mm/yyyy):')
format_str = '%d/%m/%Y' # The format
datetime_obj_end = str(datetime.datetime.strptime(date_str_end, format_str).date())

# datetime_obj_start = cd.bd_t_1
# datetime_obj_end = cd.t_1

daterange = pd.date_range(datetime_obj_start, datetime_obj_end)

for dates in daterange:
	datetime_obj = Date.from_date(pd.to_datetime(dates))
	if cd.sa_calendar.isBusinessDay(datetime_obj)== True:
		bd_datetime_obj = datetime_obj
	else:
		bd_datetime_obj = cd.prev_business_day(datetime_obj)
		
	prev_bd_datetime_obj = cd.prev_business_day(datetime_obj)
	
	datetime_obj = "%d-%d-%d" %(datetime_obj.year(),datetime_obj.month(),datetime_obj.dayOfMonth())
	bd_datetime_obj = "%d-%d-%d" %(bd_datetime_obj.year(),bd_datetime_obj.month(),bd_datetime_obj.dayOfMonth())
	prev_bd_datetime_obj = "%d-%d-%d" %(prev_bd_datetime_obj.year(),prev_bd_datetime_obj.month(),prev_bd_datetime_obj.dayOfMonth())

	# Connecting to database
	constr = "DRIVER={SQL Server Native Client 11.0};SERVER=ash-prdkblddbao,4071;DATABASE=AshburtonRisk;Trusted_Connection=yes;"
	db = odbc.odbc(constr)

	# JSEZero Curve
	sql = "SELECT TenorDate, BondCurveYield/100 AS BondCurveYield, RealCurveYield/100 AS RealCurveYield FROM Solutions.JSEZeroCurve WHERE FileDataDate = " + " ' " + bd_datetime_obj+ "'" + ""
	df_jse_zero_curve = pd.read_sql(sql, db)
	df_jse_zero_curve = df_jse_zero_curve.append(df_jse_zero_curve.iloc[0,:],ignore_index=True) # 29/08/2019
	df_jse_zero_curve = df_jse_zero_curve.sort_values(by=['TenorDate'], ascending=True)
	df_jse_zero_curve['TenorDate'].iloc[0] = datetime_obj # 29/08/2019
	df_jse_zero_curve['TenorDate'] = pd.to_datetime(df_jse_zero_curve['TenorDate'])
	curve_end_date_1 = df_jse_zero_curve['TenorDate'].max()
	df_append = df_jse_zero_curve.tail(1)
	date_t = (pd.to_datetime(curve_end_date_2) - pd.to_datetime(curve_end_date_1)).days
	df_append = pd.concat([df_append]*date_t, ignore_index=True)
	df_append['TenorDate'] = pd.date_range(str((pd.to_datetime(curve_end_date_1) + pd.DateOffset(days=1)).date()), curve_end_date_2)
	df_append['TenorDate'] = df_append.TenorDate.dt.date
	df_jse_zero_curve = df_jse_zero_curve.append(df_append, ignore_index=True)
	df_jse_zero_curve['TenorDate'] = pd.to_datetime(df_jse_zero_curve['TenorDate'])
	df_jse_zero_curve['x_axis'] = excel_date(df_jse_zero_curve.TenorDate)
	df_jse_zero_curve['bond_curve_naca'] = np.exp(df_jse_zero_curve.BondCurveYield)-1
	df_jse_zero_curve['real_curve_naca'] = np.exp(df_jse_zero_curve.RealCurveYield)-1
	df_jse_zero_curve['bond_curve_base'] = df_jse_zero_curve['bond_curve_naca']
	df_jse_zero_curve['real_curve_base'] = df_jse_zero_curve['real_curve_naca']
	df_jse_zero_curve['be_base'] = (1+df_jse_zero_curve['bond_curve_base'])/(1+df_jse_zero_curve['real_curve_base'])-1
	# Linking functions
	bond_curve_base_y_interp = scipy.interpolate.interp1d(df_jse_zero_curve.x_axis, df_jse_zero_curve.bond_curve_base, fill_value='extrapolate')
	real_curve_base_y_interp = scipy.interpolate.interp1d(df_jse_zero_curve.x_axis, df_jse_zero_curve.real_curve_base, fill_value='extrapolate')
	be_curve_base_y_interp = scipy.interpolate.interp1d(df_jse_zero_curve.x_axis, df_jse_zero_curve.be_base, fill_value='extrapolate')

	#=====================================================================================================================================================================

	# Parameters
	InvestmentCPISpread_bps = 0
	MedicalCPISpread_bps = 0
	InflationLag_months = 12
	InflationIndexation_months = 4
	cash_flow_lag_months = 4
	actual_fix_date = '2021-01-01'
	last_cf_profile_date = '2021-01-01'


	# CPI Index
	df_cpi_new = df_jse_zero_curve.copy()
	df_cpi_new = df_cpi_new[['TenorDate']]
	df_cpi_new['value_date'] = pd.to_datetime(datetime_obj)
	df_cpi_new['eff_date'] = df_cpi_new.TenorDate - pd.DateOffset(months=InflationIndexation_months)
	slice = df_cpi_new.iloc[0,:]
	df_cpi_new = df_cpi_new[df_cpi_new.TenorDate.dt.day == df_cpi_new.TenorDate.dt.days_in_month]
	df_cpi_new = df_cpi_new.append(slice,ignore_index=True) # 29/08/2019
	df_cpi_new = df_cpi_new.drop_duplicates('TenorDate') # 29/08/2019
	df_cpi_new = df_cpi_new.sort_values(by=['TenorDate'], ascending=True) # 29/08/2019
	df_cpi_new['x_axis'] = excel_date(df_cpi_new.eff_date)
	df_cpi_new['t'] = (df_cpi_new.TenorDate.dt.date - df_cpi_new.value_date.dt.date).dt.days/365
	df_cpi_new['be_base'] = be_curve_base_y_interp(excel_date(df_cpi_new.TenorDate))
	df_cpi_new['cpi_base'] = 100*(1+df_cpi_new['be_base'])**df_cpi_new['t']
	be_base_y_interp = scipy.interpolate.interp1d(df_cpi_new.x_axis, df_cpi_new.be_base, fill_value='extrapolate')
	cpi_base_y_interp = scipy.interpolate.interp1d(df_cpi_new.x_axis, df_cpi_new.cpi_base, fill_value='extrapolate')

	# CPI Table
	df_cpi = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\Input\CPI Intepolated numbers.xlsm', sheet_name = 'CPI Series')
	df_cpi.rename(columns={'CPI Index': 'RefCPI', 'Date': 'actual_cpi_date'}, inplace=True)
	df_cpi['value_date'] = pd.to_datetime(datetime_obj)
	df_cpi['actual_fix_date'] = pd.to_datetime(actual_fix_date)
	df_cpi['ref_fix_date'] = df_cpi.actual_fix_date - pd.DateOffset(months=cash_flow_lag_months)
	# df_cpi['ref_fix_m_end_date'] = df_cpi['ref_fix_date']
	df_cpi['ref_fix_m_end_date'] = df_cpi.actual_fix_date - pd.DateOffset(months=cash_flow_lag_months) + pd.DateOffset(months=1) - pd.DateOffset(1)
	df_cpi['ref_value_date'] = df_cpi.value_date - pd.DateOffset(months=InflationIndexation_months)
	df_cpi['last_cf_profile_date'] = pd.to_datetime(last_cf_profile_date)
	df_cpi['ref_last_cf_profile_date'] = df_cpi.last_cf_profile_date - pd.DateOffset(months=cash_flow_lag_months)
	df_cpi = df_cpi[['actual_cpi_date','actual_fix_date','ref_fix_date','ref_fix_m_end_date','value_date','ref_value_date','ref_last_cf_profile_date','RefCPI']]
	ref_cpi_y_interp = scipy.interpolate.interp1d(excel_date(df_cpi.actual_cpi_date), df_cpi.RefCPI, fill_value='extrapolate')
	df_cpi['fix_cpi'] = ref_cpi_y_interp(excel_date(df_cpi.ref_fix_date))
	df_cpi['fix_m_end_cpi'] = ref_cpi_y_interp(excel_date(df_cpi.ref_fix_m_end_date))
	df_cpi['cpi_base'] = cpi_base_y_interp(excel_date(df_cpi.ref_fix_m_end_date))
	df_cpi['current_cpi'] = ref_cpi_y_interp(excel_date(df_cpi.ref_value_date))
	df_cpi['last_cf_cpi'] = ref_cpi_y_interp(excel_date(df_cpi.ref_last_cf_profile_date))
	df_cpi['accrual_factor'] = df_cpi.fix_cpi / df_cpi.last_cf_cpi
	df_cpi['implied_cpi'] = df_cpi.accrual_factor - 1
	df_cpi['adjusted_accrual_factor'] = df_cpi.implied_cpi + 1
	df_cpi['multiplier'] = 100/df_cpi['current_cpi']
	df_cpi['index_start_value'] = df_cpi['last_cf_cpi']*df_cpi['multiplier']

	
	#=====================================================================================================================================================================

	# Valuation
	df = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\Input\LDICashflows.xlsx')
	df = df[df.PortfolioIDCode == 'FRRF']
	df = df[(df.cash_flow_date > datetime_obj)]
	df['CurrentDate'] = pd.to_datetime(datetime_obj)
	df['diff'] = df['DataDate'] - df['CurrentDate']
	df['diff'] = df['diff'].apply(lambda x: x.days)
	df = df[df['diff'] <= 0]
	df = df[df['diff'] == max(df['diff'])]
	df.drop(['diff','DataDate'], axis=1, inplace=True)
	df = df.sort_values(by=['cash_flow_date'], ascending=True)
	df = df[['cash_flow_date','OriginalRCF']]
	df = df.groupby(['cash_flow_date'], sort=True).sum().reset_index()
	df['CurrentDate'] = datetime_obj
	df.cash_flow_date = pd.to_datetime(df.cash_flow_date)
	df.CurrentDate = pd.to_datetime(df.CurrentDate)
	df['t'] = df.cash_flow_date - df.CurrentDate
	df.t = df.t.dt.days/365
	my_dates = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\config\my_dates_FRRF.xlsx')
	df = df.merge(my_dates, how='left', on=['cash_flow_date'])
	df['index_start_value'] = df_cpi.index_start_value.iloc[-1]
	df ['index_end_value' ] = np.where(df.check == 'fixed',df['index_start_value'],cpi_base_y_interp(excel_date(df.index_end_date))) # 29/08/2019
	# df ['index_end_value' ].iloc[0] = 97.1740758
	# df ['index_end_value' ].iloc[1] = 97.1740758
	# df ['index_end_value' ].iloc[2] = 97.1740758
	# df ['index_end_value' ].iloc[3] = 97.1740758
	df['accrual_factor_base'] = df.index_end_value/df.index_start_value
	df['nominal_cf_base'] = np.where(df.cash_flow_date == df.CurrentDate, 0, df.OriginalRCF*df.accrual_factor_base)
	df['nom_df_base'] = bond_curve_base_y_interp(excel_date(df.cash_flow_date))
	df['real_df_base'] = real_curve_base_y_interp(excel_date(df.cash_flow_date))
	df['npv_base'] = ((1+df.nom_df_base)**(-df.t))*df.nominal_cf_base
	df['real_npv_base'] = ((1+df.real_df_base)**(-df.t))*df.OriginalRCF
	df['total_npv_base'] = df['npv_base'].sum()
	df['total_real_npv_base'] = df['real_npv_base'].sum()
	df['nominal_cf_base_today'] = np.where(df.cash_flow_date == df.CurrentDate,df.OriginalRCF*df.accrual_factor_base*df_cpi['adjusted_accrual_factor'].iloc[0],0)
	df['nominal_cf_base_today'] = df['nominal_cf_base_today'].iloc[0]
	df = df[(df.cash_flow_date > datetime_obj)]

	# Nominal XIRR 
	df_nom_xirr_base= df[['cash_flow_date', 'nominal_cf_base']]
	df_nom_xirr_base= df_nom_xirr_base.append({'cash_flow_date':pd.to_datetime(datetime_obj),'nominal_cf_base':-df['total_npv_base'].iloc[-1]}, ignore_index=True)
	df_nom_xirr_base= df_nom_xirr_base.sort_values(by=['cash_flow_date'], ascending=True)
	xnpv(0.05,df_nom_xirr_base.nominal_cf_base,df_nom_xirr_base.cash_flow_date)
	nom_base = xirr(df_nom_xirr_base.nominal_cf_base,df_nom_xirr_base.cash_flow_date)

	# Real XIRR 
	df_real_xirr_base= df[['cash_flow_date', 'OriginalRCF']]
	df_real_xirr_base= df_real_xirr_base.append({'cash_flow_date':pd.to_datetime(datetime_obj),'OriginalRCF':-df['total_real_npv_base'].iloc[-1]}, ignore_index=True)
	df_real_xirr_base= df_real_xirr_base.sort_values(by=['cash_flow_date'], ascending=True)
	xnpv(0.05,df_real_xirr_base.OriginalRCF,df_real_xirr_base.cash_flow_date)
	real_base = xirr(df_real_xirr_base.OriginalRCF,df_real_xirr_base.cash_flow_date)
	
	df['nominal_xirr'] = nom_base
	df['real_xirr'] = real_base
	df['cpi'] = df_cpi['current_cpi'].iloc[-1]
	df['t*pv'] = df.t * df.npv_base
	df['duration'] = df['t*pv'].sum()/df.total_npv_base

	# Info
	df_info = pd.DataFrame({'InvestmentCPISpread_bps':[InvestmentCPISpread_bps],'MedicalCPISpread_bps':[MedicalCPISpread_bps], 
	'InflationLag_months':[InflationLag_months],'InflationIndexation_months':[InflationIndexation_months],'last_cf_profile_date':[last_cf_profile_date],
	'cpi_last_cf_date': [df_cpi['last_cf_cpi'].iloc[-1]],
	'cpi_value_date':[df_cpi['current_cpi'].iloc[-1]],'accrual_factor':[df_cpi['accrual_factor'].iloc[-1]], 'implied_cpi':[df_cpi['implied_cpi'].iloc[-1]],
	'adjusted_accrual_factor':[df_cpi['adjusted_accrual_factor'].iloc[-1]], 'npv_base':[df['total_npv_base'].iloc[-1]], 'real_npv_base':[df['total_real_npv_base'].iloc[-1]],
	'nominal_yield_base':[nom_base], 'real_yield_base':[real_base],'cash_flow_base_today':[df['nominal_cf_base_today'].iloc[0]]})
	df_info = df_info.T

	# Export file
	writer = pd.ExcelWriter(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\reports\liability_models\FRRF\FRRF_liability_valuation_model_' + datetime_obj + '.xlsx')
	df_info.to_excel(writer, 'Info')
	df.to_excel(writer, 'Valuation', index=False)
	df_jse_zero_curve.to_excel(writer, 'JSE Yield Curves', index=False)
	writer.save()
	
	
	
	#=======================================================================================================================================================================================
	#=======================================================================================================================================================================================
	#=======================================================================================================================================================================================
	
	
	
	# JSEZero Curve
	sql = "SELECT TenorDate, BondCurveYield/100 AS BondCurveYield, RealCurveYield/100 AS RealCurveYield FROM Solutions.JSEZeroCurve WHERE FileDataDate = " + " ' " + prev_bd_datetime_obj+ "'" + ""
	df_jse_zero_curve = pd.read_sql(sql, db)
	df_jse_zero_curve = df_jse_zero_curve.append(df_jse_zero_curve.iloc[0,:],ignore_index=True) # 29/08/2019
	df_jse_zero_curve = df_jse_zero_curve.sort_values(by=['TenorDate'], ascending=True)
	df_jse_zero_curve['TenorDate'].iloc[0] = datetime_obj # 29/08/2019
	df_jse_zero_curve['TenorDate'] = pd.to_datetime(df_jse_zero_curve['TenorDate'])
	curve_end_date_1 = df_jse_zero_curve['TenorDate'].max()
	df_append = df_jse_zero_curve.tail(1)
	date_t = (pd.to_datetime(curve_end_date_2) - pd.to_datetime(curve_end_date_1)).days
	df_append = pd.concat([df_append]*date_t, ignore_index=True)
	df_append['TenorDate'] = pd.date_range(str((pd.to_datetime(curve_end_date_1) + pd.DateOffset(days=1)).date()), curve_end_date_2)
	df_append['TenorDate'] = df_append.TenorDate.dt.date
	df_jse_zero_curve = df_jse_zero_curve.append(df_append, ignore_index=True)
	df_jse_zero_curve['TenorDate'] = pd.to_datetime(df_jse_zero_curve['TenorDate'])
	df_jse_zero_curve['x_axis'] = excel_date(df_jse_zero_curve.TenorDate)
	df_jse_zero_curve['bond_curve_naca'] = np.exp(df_jse_zero_curve.BondCurveYield)-1
	df_jse_zero_curve['real_curve_naca'] = np.exp(df_jse_zero_curve.RealCurveYield)-1
	df_jse_zero_curve['bond_curve_base'] = df_jse_zero_curve['bond_curve_naca']
	df_jse_zero_curve['real_curve_base'] = df_jse_zero_curve['real_curve_naca']
	df_jse_zero_curve['be_base'] = (1+df_jse_zero_curve['bond_curve_base'])/(1+df_jse_zero_curve['real_curve_base'])-1
	# Linking functions
	bond_curve_base_y_interp = scipy.interpolate.interp1d(df_jse_zero_curve.x_axis, df_jse_zero_curve.bond_curve_base, fill_value='extrapolate')
	real_curve_base_y_interp = scipy.interpolate.interp1d(df_jse_zero_curve.x_axis, df_jse_zero_curve.real_curve_base, fill_value='extrapolate')
	be_curve_base_y_interp = scipy.interpolate.interp1d(df_jse_zero_curve.x_axis, df_jse_zero_curve.be_base, fill_value='extrapolate')

	#=====================================================================================================================================================================

	# Parameters
	InvestmentCPISpread_bps = 0
	MedicalCPISpread_bps = 0
	InflationLag_months = 12
	InflationIndexation_months = 4
	cash_flow_lag_months = 4
	actual_fix_date = '2021-01-01'
	last_cf_profile_date = '2021-01-01'


	# CPI Index
	df_cpi_new = df_jse_zero_curve.copy()
	df_cpi_new = df_cpi_new[['TenorDate']]
	df_cpi_new['value_date'] = pd.to_datetime(datetime_obj)
	df_cpi_new['eff_date'] = df_cpi_new.TenorDate - pd.DateOffset(months=InflationIndexation_months)
	slice = df_cpi_new.iloc[0,:]
	df_cpi_new = df_cpi_new[df_cpi_new.TenorDate.dt.day == df_cpi_new.TenorDate.dt.days_in_month]
	df_cpi_new = df_cpi_new.append(slice,ignore_index=True) # 29/08/2019
	df_cpi_new = df_cpi_new.drop_duplicates('TenorDate') # 29/08/2019
	df_cpi_new = df_cpi_new.sort_values(by=['TenorDate'], ascending=True) # 29/08/2019
	df_cpi_new['x_axis'] = excel_date(df_cpi_new.eff_date)
	df_cpi_new['t'] = (df_cpi_new.TenorDate.dt.date - df_cpi_new.value_date.dt.date).dt.days/365
	df_cpi_new['be_base'] = be_curve_base_y_interp(excel_date(df_cpi_new.TenorDate))
	df_cpi_new['cpi_base'] = 100*(1+df_cpi_new['be_base'])**df_cpi_new['t']
	be_base_y_interp = scipy.interpolate.interp1d(df_cpi_new.x_axis, df_cpi_new.be_base, fill_value='extrapolate')
	cpi_base_y_interp = scipy.interpolate.interp1d(df_cpi_new.x_axis, df_cpi_new.cpi_base, fill_value='extrapolate')

	# CPI Table
	df_cpi = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\Input\CPI Intepolated numbers.xlsm', sheet_name = 'CPI Series')
	df_cpi.rename(columns={'CPI Index': 'RefCPI', 'Date': 'actual_cpi_date'}, inplace=True)
	df_cpi['value_date'] = pd.to_datetime(datetime_obj)
	df_cpi['actual_fix_date'] = pd.to_datetime(actual_fix_date)
	df_cpi['ref_fix_date'] = df_cpi.actual_fix_date - pd.DateOffset(months=cash_flow_lag_months)
	# df_cpi['ref_fix_m_end_date'] = df_cpi['ref_fix_date']
	df_cpi['ref_fix_m_end_date'] = df_cpi.actual_fix_date - pd.DateOffset(months=cash_flow_lag_months) + pd.DateOffset(months=1) - pd.DateOffset(1)
	df_cpi['ref_value_date'] = df_cpi.value_date - pd.DateOffset(months=InflationIndexation_months)
	df_cpi['last_cf_profile_date'] = pd.to_datetime(last_cf_profile_date)
	df_cpi['ref_last_cf_profile_date'] = df_cpi.last_cf_profile_date - pd.DateOffset(months=cash_flow_lag_months)
	df_cpi = df_cpi[['actual_cpi_date','actual_fix_date','ref_fix_date','ref_fix_m_end_date','value_date','ref_value_date','ref_last_cf_profile_date','RefCPI']]
	ref_cpi_y_interp = scipy.interpolate.interp1d(excel_date(df_cpi.actual_cpi_date), df_cpi.RefCPI, fill_value='extrapolate')
	df_cpi['fix_cpi'] = ref_cpi_y_interp(excel_date(df_cpi.ref_fix_date))
	df_cpi['fix_m_end_cpi'] = ref_cpi_y_interp(excel_date(df_cpi.ref_fix_m_end_date))
	df_cpi['cpi_base'] = cpi_base_y_interp(excel_date(df_cpi.ref_fix_m_end_date))
	df_cpi['current_cpi'] = ref_cpi_y_interp(excel_date(df_cpi.ref_value_date))
	df_cpi['last_cf_cpi'] = ref_cpi_y_interp(excel_date(df_cpi.ref_last_cf_profile_date))
	df_cpi['accrual_factor'] = df_cpi.fix_cpi / df_cpi.last_cf_cpi
	df_cpi['implied_cpi'] = df_cpi.accrual_factor - 1
	df_cpi['adjusted_accrual_factor'] = df_cpi.implied_cpi + 1
	df_cpi['multiplier'] = 100/df_cpi['current_cpi']
	df_cpi['index_start_value'] = df_cpi['last_cf_cpi']*df_cpi['multiplier']

	
	#=====================================================================================================================================================================

	# Valuation
	df = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\Input\LDICashflows.xlsx')
	df = df[df.PortfolioIDCode == 'FRRF']
	df = df[(df.cash_flow_date > datetime_obj)]
	df['CurrentDate'] = pd.to_datetime(datetime_obj)
	df['diff'] = df['DataDate'] - df['CurrentDate']
	df['diff'] = df['diff'].apply(lambda x: x.days)
	df = df[df['diff'] <= 0]
	df = df[df['diff'] == max(df['diff'])]
	df.drop(['diff','DataDate'], axis=1, inplace=True)
	df = df.sort_values(by=['cash_flow_date'], ascending=True)
	df = df[['cash_flow_date','OriginalRCF']]
	df = df.groupby(['cash_flow_date'], sort=True).sum().reset_index()
	df['CurrentDate'] = datetime_obj
	df.cash_flow_date = pd.to_datetime(df.cash_flow_date)
	df.CurrentDate = pd.to_datetime(df.CurrentDate)
	df['t'] = df.cash_flow_date - df.CurrentDate
	df.t = df.t.dt.days/365
	my_dates = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\config\my_dates_FRRF.xlsx')
	df = df.merge(my_dates, how='left', on=['cash_flow_date'])
	df['index_start_value'] = df_cpi.index_start_value.iloc[-1]
	df ['index_end_value' ] = np.where(df.check == 'fixed',df['index_start_value'],cpi_base_y_interp(excel_date(df.index_end_date))) # 29/08/2019
	# df ['index_end_value' ].iloc[0] = 97.1740758
	# df ['index_end_value' ].iloc[1] = 97.1740758
	# df ['index_end_value' ].iloc[2] = 97.1740758
	# df ['index_end_value' ].iloc[3] = 97.1740758
	df['accrual_factor_base'] = df.index_end_value/df.index_start_value
	df['nominal_cf_base'] = np.where(df.cash_flow_date == df.CurrentDate, 0, df.OriginalRCF*df.accrual_factor_base)
	df['nom_df_base'] = bond_curve_base_y_interp(excel_date(df.cash_flow_date))
	df['real_df_base'] = real_curve_base_y_interp(excel_date(df.cash_flow_date))
	df['npv_base'] = ((1+df.nom_df_base)**(-df.t))*df.nominal_cf_base
	df['real_npv_base'] = ((1+df.real_df_base)**(-df.t))*df.OriginalRCF
	df['total_npv_base'] = df['npv_base'].sum()
	df['total_real_npv_base'] = df['real_npv_base'].sum()
	df['nominal_cf_base_today'] = np.where(df.cash_flow_date == df.CurrentDate,df.OriginalRCF*df.accrual_factor_base*df_cpi['adjusted_accrual_factor'].iloc[0],0)
	df['nominal_cf_base_today'] = df['nominal_cf_base_today'].iloc[0]
	df = df[(df.cash_flow_date > datetime_obj)]

	# Nominal XIRR 
	df_nom_xirr_base= df[['cash_flow_date', 'nominal_cf_base']]
	df_nom_xirr_base= df_nom_xirr_base.append({'cash_flow_date':pd.to_datetime(datetime_obj),'nominal_cf_base':-df['total_npv_base'].iloc[-1]}, ignore_index=True)
	df_nom_xirr_base= df_nom_xirr_base.sort_values(by=['cash_flow_date'], ascending=True)
	xnpv(0.05,df_nom_xirr_base.nominal_cf_base,df_nom_xirr_base.cash_flow_date)
	nom_base = xirr(df_nom_xirr_base.nominal_cf_base,df_nom_xirr_base.cash_flow_date)

	# Real XIRR 
	df_real_xirr_base= df[['cash_flow_date', 'OriginalRCF']]
	df_real_xirr_base= df_real_xirr_base.append({'cash_flow_date':pd.to_datetime(datetime_obj),'OriginalRCF':-df['total_real_npv_base'].iloc[-1]}, ignore_index=True)
	df_real_xirr_base= df_real_xirr_base.sort_values(by=['cash_flow_date'], ascending=True)
	xnpv(0.05,df_real_xirr_base.OriginalRCF,df_real_xirr_base.cash_flow_date)
	real_base = xirr(df_real_xirr_base.OriginalRCF,df_real_xirr_base.cash_flow_date)
	
	df['nominal_xirr'] = nom_base
	df['real_xirr'] = real_base
	df['cpi'] = df_cpi['current_cpi'].iloc[-1]
	df['t*pv'] = df.t * df.npv_base
	df['duration'] = df['t*pv'].sum()/df.total_npv_base

	# Info
	df_info = pd.DataFrame({'InvestmentCPISpread_bps':[InvestmentCPISpread_bps],'MedicalCPISpread_bps':[MedicalCPISpread_bps], 
	'InflationLag_months':[InflationLag_months],'InflationIndexation_months':[InflationIndexation_months],'last_cf_profile_date':[last_cf_profile_date],
	'cpi_last_cf_date': [df_cpi['last_cf_cpi'].iloc[-1]],
	'cpi_value_date':[df_cpi['current_cpi'].iloc[-1]],'accrual_factor':[df_cpi['accrual_factor'].iloc[-1]], 'implied_cpi':[df_cpi['implied_cpi'].iloc[-1]],
	'adjusted_accrual_factor':[df_cpi['adjusted_accrual_factor'].iloc[-1]], 'npv_base':[df['total_npv_base'].iloc[-1]], 'real_npv_base':[df['total_real_npv_base'].iloc[-1]],
	'nominal_yield_base':[nom_base], 'real_yield_base':[real_base],'cash_flow_base_today':[df['nominal_cf_base_today'].iloc[0]]})
	df_info = df_info.T

	# Export file
	writer = pd.ExcelWriter(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\reports\liability_models\FRRF\FRRF_liability_valuation_model_' + datetime_obj + '_prev.xlsx')
	df_info.to_excel(writer, 'Info')
	df.to_excel(writer, 'Valuation', index=False)
	df_jse_zero_curve.to_excel(writer, 'JSE Yield Curves', index=False)
	writer.save()