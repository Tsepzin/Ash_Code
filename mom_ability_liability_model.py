# Effective date: 01 July 2018
import pandas as pd
import odbc
import numpy as np
import datetime
# from pandas.tseries.offsets import MonthEnd
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
curve_end_date_2 = '2142-06-30'


date_str_start = input('Enter start date (Format dd/mm/yyyy):')
format_str = '%d/%m/%Y' # The format
datetime_obj_start = str(datetime.datetime.strptime(date_str_start, format_str).date())

date_str_end = input('Enter end date (Format dd/mm/yyyy):')
format_str = '%d/%m/%Y' # The format
datetime_obj_end = str(datetime.datetime.strptime(date_str_end, format_str).date())

# datetime_obj_start = cd.bd_t_1
# datetime_obj_end = cd.t_1

daterange = pd.date_range(datetime_obj_start, datetime_obj_end)

# Connecting to database
constr = "DRIVER={SQL Server Native Client 11.0};SERVER=ash-prdkblddbao,4071;DATABASE=AshburtonRisk;Trusted_Connection=yes;"
db = odbc.odbc(constr)

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
    # constr = "DRIVER={SQL Server Native Client 11.0};SERVER=ash-prdkblddbao,4071;DATABASE=AshburtonRisk;Trusted_Connection=yes;"
    # db = odbc.odbc(constr)
    # JSEZero Curve
    # sql = "SELECT TenorDate, BondCurveYield/100 AS BondCurveYield, RealCurveYield/100 AS RealCurveYield FROM Solutions.JSEZeroCurve WHERE FileDataDate = " + " ' " + bd_datetime_obj+ "'" + ""
    # df_jse_zero_curve = pd.read_sql(sql, db)
    
    # Parameters
    InvestmentCPISpread_bps = 10
    MedicalCPISpread_bps = 250
    InflationIndexation_months = 4
    last_cf_date = '2020-12-31'
    
    df_cpi = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\Input\CPI Intepolated numbers.xlsm', sheet_name = 'CPI Series')
    cpi_y_interp = scipy.interpolate.interp1d(excel_date(df_cpi['Date']), df_cpi['CPI Index'], fill_value='extrapolate')
    df_cpi = pd.DataFrame(pd.date_range(df_cpi['Date'].min(), df_cpi['Date'].max()), columns=['Date'])
    df_cpi['CPI'] = cpi_y_interp(excel_date(df_cpi['Date']))
    current_cpi = (df_cpi[df_cpi['Date'] == pd.to_datetime(datetime_obj) - pd.DateOffset(months = InflationIndexation_months)])['CPI'].values
    print('current_cpi: ', current_cpi)
    last_cf_cpi = (df_cpi[df_cpi['Date'] == pd.to_datetime(last_cf_date) - pd.DateOffset(months = InflationIndexation_months)])['CPI'].values
    print('last_cf_cpi: ', last_cf_cpi)
    accrual_factor = current_cpi / last_cf_cpi
    print('accrual_factor: ', accrual_factor)
    implied_cpi = accrual_factor ** (365/(pd.to_datetime(datetime_obj) - pd.to_datetime(last_cf_date)).days) -1
    print('implied_cpi: ', implied_cpi) 
    adjusted_accrual_factor = (1 + implied_cpi + MedicalCPISpread_bps/10000)**((pd.to_datetime(datetime_obj) - pd.to_datetime(last_cf_date)).days/365)
    print('adjusted_accrual_factor: ', adjusted_accrual_factor) 
    
    curve = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\curves\rmb_curves_ldi\rmb_curves_ldi_' + str(pd.to_datetime(bd_datetime_obj).date()) + '.xlsx')
    bond_curve = curve[curve['Name'] == 'RMBZERO']
    bond_curve.rename(columns={'Date': 'TenorDate', 'Rate': 'BondCurveYield'}, inplace=True)
    bond_curve = bond_curve[['TenorDate','BondCurveYield']]
    bond_curve['BondCurveYield'] = (1 + bond_curve['BondCurveYield']/2)**2 - 1   # converting comp freq from NACS to NACA
    bond_curve = bond_curve.sort_values(['TenorDate'])
    curve_end_date_1 = bond_curve['TenorDate'].max()
    df_append = bond_curve.tail(1)
    date_t = (pd.to_datetime(curve_end_date_2) - pd.to_datetime(curve_end_date_1)).days
    df_append = pd.concat([df_append]*date_t, ignore_index=True)
    df_append['TenorDate'] = pd.date_range(str((pd.to_datetime(curve_end_date_1) + pd.DateOffset(days=1)).date()), curve_end_date_2)
    df_append['TenorDate'] = df_append.TenorDate.dt.date
    bond_curve = bond_curve.append(df_append, ignore_index=True)
    bond_curve = bond_curve.sort_values(['TenorDate'])
    bond_curve['TenorDate'] = pd.to_datetime(bond_curve['TenorDate'])
    real_curve = curve[curve['Name'] == 'RMBRealBond']
    real_curve.rename(columns={'Date': 'TenorDate', 'Rate': 'RealCurveYield'}, inplace=True)
    real_curve = real_curve[['TenorDate','RealCurveYield']]
    real_curve['RealCurveYield'] = (1 + real_curve['RealCurveYield']/2)**2 - 1   # converting comp freq from NACS to NACA
    real_curve = real_curve.sort_values(['TenorDate'])
    curve_end_date_1 = real_curve['TenorDate'].max()
    df_append = real_curve.tail(1)
    date_t = (pd.to_datetime(curve_end_date_2) - pd.to_datetime(curve_end_date_1)).days
    df_append = pd.concat([df_append]*date_t, ignore_index=True)
    df_append['TenorDate'] = pd.date_range(str((pd.to_datetime(curve_end_date_1) + pd.DateOffset(days=1)).date()), curve_end_date_2)
    df_append['TenorDate'] = df_append.TenorDate.dt.date
    real_curve = real_curve.append(df_append, ignore_index=True)
    real_curve = real_curve.sort_values(['TenorDate'])
    real_curve['TenorDate'] = pd.to_datetime(real_curve['TenorDate'])
    
    # Interpolation
    bond_curve_base_y_interp = scipy.interpolate.interp1d(excel_date(bond_curve['TenorDate']), bond_curve['BondCurveYield'], fill_value='extrapolate')
    real_curve_base_y_interp = scipy.interpolate.interp1d(excel_date(real_curve['TenorDate']), real_curve['RealCurveYield'], fill_value='extrapolate')
    
    curve = pd.DataFrame(pd.date_range(datetime_obj, curve_end_date_2, freq='M'), columns=['TenorDate'])
    curve['bond_base'] = bond_curve_base_y_interp(excel_date(curve['TenorDate']))
    curve['real_base'] = real_curve_base_y_interp(excel_date(curve['TenorDate']))
    curve['be_base'] = (1 + curve['bond_base']) / (1 + curve['real_base']) - 1
    be_curve_base_y_interp = scipy.interpolate.interp1d(excel_date(curve['TenorDate']), curve['be_base'], fill_value='extrapolate')
    
    # Valuation
    df = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\Input\LDICashflows.xlsx')
    df = df[df.PortfolioIDCode == 95930]
    df['cf_filter'] = (df['DataDate'] - pd.to_datetime(datetime_obj)).dt.days
    df = df[df['cf_filter'] <= 0]
    df = df[df['cf_filter'] == df['cf_filter'].max()]
    df = df[(df.cash_flow_date > datetime_obj)]
    df['CurrentDate'] = pd.to_datetime(datetime_obj)
    df['t'] = (df['cash_flow_date'] - df['CurrentDate']).dt.days/365
    df['AdjustedRCF'] = df['OriginalRCF'] * adjusted_accrual_factor
    df['nom_df_base'] = bond_curve_base_y_interp(excel_date(df.cash_flow_date)) + InvestmentCPISpread_bps/10000
    df['real_df_base'] = real_curve_base_y_interp(excel_date(df.cash_flow_date)) + InvestmentCPISpread_bps/10000
    df['be_rate_base'] = be_curve_base_y_interp(excel_date(df.cash_flow_date)) + MedicalCPISpread_bps/10000
    df['nominal_cf_base'] = (1 + df['be_rate_base'])**df['t']*df['AdjustedRCF']
    df['npv_base'] = ((1+df['nom_df_base'])**(-df['t']))*df['nominal_cf_base']
    df['real_npv_base'] = ((1+df.real_df_base)**(-df.t))*df.OriginalRCF
    df['total_npv_base'] = df['npv_base'].sum()
    df['total_real_npv_base'] = df['real_npv_base'].sum()
    
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
    df['cpi'] = float(current_cpi)
    df['t*pv'] = df.t * df.npv_base
    df['duration'] = df['t*pv'].sum()/df.total_npv_base
    
    # Export file
    writer = pd.ExcelWriter(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\reports\liability_models\mom_ability\mom_ability_liability_valuation_model_' + datetime_obj + '.xlsx')
    df.to_excel(writer, 'Valuation', index=False)
    curve.to_excel(writer, 'Curves', index=False)
    writer.save()
