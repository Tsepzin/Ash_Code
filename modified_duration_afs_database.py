import pandas as pd
import odbc
import numpy as np
import datetime
from my_functions import custom_dates as cd

# date_str_start = input('Enter valuation date (Format dd/mm/yyyy):')
# format_str = '%d/%m/%Y' # The format
# datetime_obj_start = str(datetime.datetime.strptime(date_str_start, format_str).date())

datetime_obj_start = cd.bd_t_1

# Config file
funds = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\config\modified_duration.xlsx', sheet_name='funds')
PfCode = []
for i in range(len(funds)):
    PfCode.append(funds.iloc[i,1])

# Albi Weight
albi = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\config\AlbiWeights.xlsx', sheet_name='Weight')
albi = albi[albi['AsDate'] == pd.to_datetime(datetime_obj_start)]
albi = albi.T.reset_index()
albi.drop(index=0, inplace=True)
albi = albi[albi!=0].dropna()
albi.to_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\reports\modified_duration\input\albi_weights_' + datetime_obj_start + '.xlsx', index=False, header=False)
	
constr = "DRIVER={SQL Server Native Client 11.0};SERVER=ash-prdkblddbao,4071;DATABASE=AshburtonRisk;Trusted_Connection=yes;"
db = odbc.odbc(constr)

sql = "SELECT InstrumentCode, ValuationDate, InstrumentTypeDescription, InstrumentLongName, MaturityDate, PrevCouponDate, NextCouponDate, (InterestRate + Spread)/100 AS Coupon, CouponType, IsResetDates, CouponFrequency  FROM Investment.MaitlandASISAInstruments WHERE DataDate = " + " ' " + datetime_obj_start + "'" + " "
df_static = pd.read_sql(sql, db)
df_static.drop_duplicates(subset=['InstrumentCode'], keep='first', inplace=True)
df_static['Redemption'] = 100.0
df_static['CouponFrequency#'] = np.where(df_static['CouponFrequency'] == 'S', 2, np.where(df_static['CouponFrequency'] == 'Q', 4,1))

# Connect to a database
constr = "DRIVER={SQL Server Native Client 11.0};SERVER=ash-rbqadb01,4071;DATABASE=AFSAnalyticsHub;Trusted_Connection=yes;"
db = odbc.odbc(constr)

sql = "SELECT InstrumentCode, ((BaseMarketValue - AssetAccruedIncome)/NULLIF(HoldingNominal, 0)*100) AS CleanPrice, ((BaseMarketValue)/NULLIF(HoldingNominal, 0)*100) AS AllInPrice FROM Maitland.ASH_Holding_2_6_Daily WHERE ValuationDate = " + " ' " + datetime_obj_start + "'" + ""
df_hlds = pd.read_sql(sql, db)
df_hlds.drop_duplicates(subset=['InstrumentCode'], keep='first', inplace=True)
df_static = df_static.merge(df_hlds, how='left', on=['InstrumentCode'])
df_static = df_static.dropna(subset=['CleanPrice'])
df_static = df_static[df_static['CleanPrice'] != 0]

df_static.to_csv(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\reports\modified_duration\input\MD_input_' + datetime_obj_start + '.csv', index = False)

# Holdings
writer = pd.ExcelWriter(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\reports\modified_duration\input\Holdings_' + datetime_obj_start + '.xlsx')

for i in PfCode:
	pieces = []
	# Connect to a database
	constr = "DRIVER={SQL Server Native Client 11.0};SERVER=ash-rbqadb01,4071;DATABASE=AFSAnalyticsHub;Trusted_Connection=yes;"
	db = odbc.odbc(constr)
	sql = "SELECT InstrumentCode, PortfolioIDCode, PortfolioName, ValuationDate, PortfolioBaseCurrency, InstrumentLongName, HoldingNominal,  BaseEffectiveExposure ,(BaseEffectiveExposure/TotalMarketValue) AS Weight1,BaseMarketValue,(BaseMarketValue/TotalMarketValue) AS Weight2, ((BaseMarketValue - AssetAccruedIncome)/NULLIF(HoldingNominal, 0)*100) AS CleanPrice FROM Maitland.ASH_Holding_2_6_Daily WHERE ValuationDate = " + " '" + datetime_obj_start + "'" + " AND PortfolioIDCode = " + "'" + str(i) + "'" +""
	df = pd.read_sql(sql, db)
	df = df.drop_duplicates(['InstrumentCode'])
	constr = "DRIVER={SQL Server Native Client 11.0};SERVER=ash-prdkblddbao,4071;DATABASE=AshburtonRisk;Trusted_Connection=yes;"
	db = odbc.odbc(constr)
	sql = "SELECT InstrumentCode, IsResetDates, InstrumentTypeDescription, MaturityDate, PrevCouponDate, NextCouponDate, (InterestRate/100) AS Coupon, CouponFrequency, CouponType FROM Investment.MaitlandASISAInstruments WHERE DataDate = " + " '" + datetime_obj_start + "'" + " AND PortfolioIDCode = " + "'" + str(i) + "'" +""
	df_type = pd.read_sql(sql, db)
	df_type = df_type.drop_duplicates(['InstrumentCode'])
	df = df.merge(df_type, how='left', on=['InstrumentCode'])
	df.to_excel(writer, str(i), index=False)
writer.save()

# Connect to a database
constr = "DRIVER={SQL Server Native Client 11.0};SERVER=ash-prdkblddbao,4071;DATABASE=AshburtonRisk;Trusted_Connection=yes;"
db = odbc.odbc(constr)

sql = "SELECT BondCode, TradeDate, Maturity, AllInPrice, ModifiedDuration FROM Investment.vwDailyBondMTMGap WHERE TradeDate = " + " ' " + datetime_obj_start + "'" + " "
df_mtm = pd.read_sql(sql, db)
df_mtm = df_mtm[df_mtm.ModifiedDuration != 0]
df_mtm.to_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\reports\modified_duration\input\mtm_' + datetime_obj_start + '.xlsx', index=False)


