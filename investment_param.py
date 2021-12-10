import pandas as pd
import odbc
import numpy as np
import datetime
from my_functions import custom_dates as cd

# date_str_end = input('Enter end date (Format dd/mm/yyyy):')
# format_str = '%d/%m/%Y' # The format
# datetime_obj_end = str(datetime.datetime.strptime(date_str_end, format_str).date())

datetime_obj_end = cd.t_1

funds = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\config\Investement_parameters.xlsx', sheet_name='funds')
funds = funds.fund_code.astype(str)
funds = "','".join(funds)
funds = "'" + funds + "'"

sql = "SELECT * FROM Investment.vwMaitlandHoldings WHERE ValuationDate = " + " '" + str(cd.t_1) + "'" + " AND PortfolioCode IN " + " ( " + (funds) + ")"
# holdings = pd.read_sql(sql, db)
holdings = pd.read_excel(r'Z:\Investment Analytics\Fund Reports\Fund Management FI\Traditional\2019\2019-07\2019-07 Investments Parameters_v2.xlsx', sheet_name='Data')
# holdings['PortfolioCode'] = holdings['PortfolioCode'].astype(int)


# Market Value
df_excl_cln = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\config\Investement_parameters.xlsx', sheet_name='credit_issuer_excl_cln')
df_cln = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\config\Investement_parameters.xlsx', sheet_name='cln')

temp = holdings.merge(df_cln[['InstrumentCode','Sector']], how='left', on=['InstrumentCode'])

temp_excl_cln = temp[temp['Sector'] != 'CLN']
temp_excl_cln.FI_Issuer_Remapped = temp_excl_cln.FI_Issuer_Remapped.str.upper()
temp_excl_cln.FI_GuaranteeType = temp_excl_cln.FI_GuaranteeType.str.upper()
temp_excl_cln = pd.pivot_table(temp_excl_cln, index=['FI_Issuer_Remapped','FI_GuaranteeType'], columns=['PortfolioCode'], values=['MarketValue'], aggfunc=np.sum)
temp_excl_cln.columns = temp_excl_cln.columns.droplevel()
temp_excl_cln = temp_excl_cln.reset_index()
temp_excl_cln = temp_excl_cln.rename(columns={'FI_Issuer_Remapped': 'Underlying','FI_GuaranteeType': 'Guarantee Type'})
df_excl_cln = df_excl_cln.merge(temp_excl_cln, how='left', on=['Underlying','Guarantee Type'])

temp_cln = temp[temp['Sector'] == 'CLN']
temp_cln = pd.pivot_table(temp_cln, index=['InstrumentCode'], columns=['PortfolioCode'], values=['MarketValue'], aggfunc=np.sum)
temp_cln.columns = temp_cln.columns.droplevel()
temp_cln = temp_cln.reset_index()
df_cln = df_cln.merge(temp_cln, how='left', on=['InstrumentCode'])

df = df_excl_cln.append(df_cln, sort=False)
df = df.append(df.sum(numeric_only=True), ignore_index=True)
df['Sector'].iloc[-1] = 'Total'

df.to_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\reports\investment_parameters\investment_parameters_market_value.xlsx', index=False)

# ====================================================================================================================================================================================
# Percentage
df_excl_cln = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\config\Investement_parameters.xlsx', sheet_name='credit_issuer_excl_cln')
df_cln = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\config\Investement_parameters.xlsx', sheet_name='cln')
df_inguza = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\config\Investement_parameters.xlsx', sheet_name='inguza')
df_cln = df_cln.append(df_inguza, sort=False)

temp = holdings.merge(df_cln[['InstrumentCode','Sector']], how='left', on=['InstrumentCode'])

df = pd.DataFrame()  # reset data frames

temp_excl_cln = temp[temp['Sector'] != 'CLN']
temp_excl_cln.FI_Issuer_Remapped = temp_excl_cln.FI_Issuer_Remapped.str.upper()
temp_excl_cln.FI_GuaranteeType = temp_excl_cln.FI_GuaranteeType.str.upper()
temp_excl_cln['MarketValuePercentage'] = temp_excl_cln['MarketValuePercentage'].apply(lambda x: x/100)
temp_excl_cln = pd.pivot_table(temp_excl_cln, index=['FI_Issuer_Remapped','FI_GuaranteeType'], columns=['PortfolioCode'], values=['MarketValuePercentage'], aggfunc=np.sum)
temp_excl_cln.columns = temp_excl_cln.columns.droplevel()
temp_excl_cln = temp_excl_cln.reset_index()
temp_excl_cln = temp_excl_cln.rename(columns={'FI_Issuer_Remapped': 'Underlying','FI_GuaranteeType': 'Guarantee Type'})
df_excl_cln = df_excl_cln.merge(temp_excl_cln, how='left', on=['Underlying','Guarantee Type'])

temp_cln = temp[(temp['Sector'] == 'CLN') | (temp['Sector'] == 'INGUZA')]
temp_cln['MarketValuePercentage'] = temp_cln['MarketValuePercentage'].apply(lambda x: x/100)
temp_cln = pd.pivot_table(temp_cln, index=['InstrumentCode'], columns=['PortfolioCode'], values=['MarketValuePercentage'], aggfunc=np.sum)
temp_cln.columns = temp_cln.columns.droplevel()
temp_cln = temp_cln.reset_index()
df_cln = df_cln.merge(temp_cln, how='left', on=['InstrumentCode'])

df = df_excl_cln.append(df_cln, sort=False)

df_new = pd.DataFrame()
for c in range(11,len(df.columns)):
	x = pd.DataFrame()
	# x = pd.concat([df.iloc[:,:11],df.iloc[:,c:c+1]], sort=False, ignore_index=False)
	x = pd.concat([df.iloc[:,:11],df.iloc[:,c:c+1]], axis=1)
	y = x.columns[len(x.columns)-1]
	x.rename(columns={x.columns[len(x.columns)-1]:'Exposure'}, inplace=True)
	x['PortfolioCode'] = y
	df_new = df_new.append(x)

df_new = pd.pivot_table(df_new, index=['PortfolioCode','Underlying','Guarantee Type'], values=['Single Limit_Adj','Exposure'], aggfunc=[np.mean,np.sum])
df_new.columns = df_new.columns.droplevel(0)
df_new = df_new.reset_index()
df_new = df_new.iloc[:,[0,1,2,3,6]]
df_new = df_new[df_new.iloc[:,3] > df_new.iloc[:,4]]
df_new.to_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\reports\investment_parameters\issuer_limits.xlsx', index=False)

df = df.append(df.sum(numeric_only=True), ignore_index=True)
df['Sector'].iloc[-1] = 'Total'

df.to_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\reports\investment_parameters\investment_parameters_percentage.xlsx', index=False)


