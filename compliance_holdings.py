import pandas as pd
import odbc
import numpy as np
import datetime
from my_functions import custom_dates as cd

# date_str_end = input('Enter end date (Format dd/mm/yyyy):')
# format_str = '%d/%m/%Y' # The format
# datetime_obj_end = str(datetime.datetime.strptime(date_str_end, format_str).date())

datetime_obj_end = cd.bd_t_1
# datetime_obj_end = cd.t_1

constr = "DRIVER={SQL Server Native Client 11.0};SERVER=rmb-ppr-msql05,1433;DATABASE=Cubit;Trusted_Connection=yes;"
db = odbc.odbc(constr)

writer = pd.ExcelWriter(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\reports\compliance\holdings\combined\holdings_' + datetime_obj_end + '.xlsx')

unclasified_df = pd.DataFrame()

#************************************************************************************************************************************************************************************
# 'FNB Life Shareholder'

# Config file
listed = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\config\compliance.xlsx', sheet_name='listed')
unlisted = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\config\compliance.xlsx', sheet_name='unlisted')
unlisted['Underlying Debt Transaction'] = unlisted['Underlying Debt Transaction'].str.upper().str.strip()
unlisted['Tranche'] = unlisted['Tranche'].str.upper().str.strip()

sql = "SELECT ValueDate, InstrumentCode, InstrumentCode AS 'Instrument Name', InstrumentType, IssuerName, MtmValuation AS 'All-in Market Value-Val', InstrumentMaturityDate AS 'Inst Maty Dt', TradedRate, MtmRate, PV01 FROM dbo.ValuationExtended WHERE ValueDate = " + " ' " + datetime_obj_end + "'" + " AND PortfolioCode IN ('17065','17067')"
df = pd.read_sql(sql, db)
df['IssuerName'] = df['IssuerName'].str.upper()
df['InstrumentCode'] = df['InstrumentCode'].str.upper()
df['Yield'] = np.where(df['TradedRate']==0,df['MtmRate'],df['TradedRate'])
df['Mod Dur'] = df['PV01']*-10000/df['All-in Market Value-Val']
df = df[df['InstrumentCode'].str.contains('LC17G|DC16E|IN304U1907|IN304U|LL19L04004')==False]
df = df[df['InstrumentType']!='Deposit']
df['%Market Value'] = df['All-in Market Value-Val']/df['All-in Market Value-Val'].sum()
df['Time to Maturity (days)'] = (pd.to_datetime(df['Inst Maty Dt']) - pd.to_datetime(df['ValueDate'])).dt.days
df['Time to Maturity (days)'] = df['Time to Maturity (days)'].fillna(0)
df['Weighted Duration'] = df['%Market Value']* df['Mod Dur']
df = df.merge(listed, how='left', on=['InstrumentCode'])
# single_issuer_exposure
single_issuer_exposure = df.groupby(['Issuer']).sum()['%Market Value'].reset_index()
single_issuer_exposure.rename(columns={'%Market Value':'Single Issuer Exposure'}, inplace=True)
df = df.merge(single_issuer_exposure, how='left', on=['Issuer'])
df['duplicated_issuer'] = df['Single Issuer Exposure'].duplicated()
df['Single Issuer Exposure'] = np.where(df['duplicated_issuer']==True,0,df['Single Issuer Exposure'])
# single_issuer_exposure
single_industry_exposure = df.groupby(['Industry']).sum()['%Market Value'].reset_index()
single_industry_exposure.rename(columns={'%Market Value':'Single Industry Exposure'}, inplace=True)
df = df.merge(single_industry_exposure, how='left', on=['Industry'])
df['duplicated_industry'] = df['Single Industry Exposure'].duplicated()
df['Single Industry Exposure'] = np.where(df['duplicated_industry']==True,0,df['Single Industry Exposure'])

df.drop(['MtmRate','TradedRate','PV01','duplicated_issuer','duplicated_industry'], axis=1, inplace=True)
df = df[['ValueDate','InstrumentCode','Instrument Name','InstrumentType','%Market Value','All-in Market Value-Val','Issuer','Yield','Inst Maty Dt','Mod Dur','Time to Maturity (days)','Single Issuer Exposure','Industry','Single Industry Exposure','Weighted Duration','Issuer Type','Guarantee','National Rating','Global Rating','Source','PD','LGD','Collateralization','Classification','IssuerName','Status']]
df = df.sort_values(by=['Issuer','InstrumentType'], ascending=False)

df.to_excel(writer,'FNB Life', index=False)

unclasified = df[df['National Rating'].isnull()]
unclasified = unclasified[['ValueDate','InstrumentCode','InstrumentType','Inst Maty Dt','IssuerName']]
unclasified_df = unclasified_df.append(unclasified)

#************************************************************************************************************************************************************************************
# # FNB Life Credit
# # AIG
# aig_nav = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\reports\compliance\credit_funds\nav_report.xlsx', sheet_name='aig_nav')
# aig_nav.rename(columns={'Maturity date':'Maturity Date'}, inplace=True)
# aig_nav['Underlying Debt Transaction'] = aig_nav['Underlying Debt Transaction'].str.upper().str.strip()
# aig_nav['Tranche'] = aig_nav['Tranche'].str.upper().str.strip()
# aig_nav = aig_nav[['Underlying Debt Transaction','Tranche','Secured','FNB Life','Industry','Spread','Type','Maturity Date','Total Yield']]
# aig_nav['Fund'] = 'Note - AIG2U'
# aig_nav['Grade'] = 'Investment Grade'
# aig_nav['Deal type'] = 'Loan'
# aig_nav.rename(columns={'FNB Life': 'Value'}, inplace=True)
# aig_nav['Exposure'] = aig_nav['Value']/aig_nav['Value'].sum()
# aig_nav = aig_nav[aig_nav['Value'] != 0]
# aig_nav['Time to Maturity (days)'] = (pd.to_datetime(aig_nav['Maturity Date']) - pd.to_datetime(datetime_obj_end)).dt.days
# aig_nav['Time to Maturity (days)'] = aig_nav['Time to Maturity (days)'].fillna(0)
# aig_nav = aig_nav.merge(unlisted, how='left', on=['Underlying Debt Transaction','Tranche'])
# # single_issuer_exposure
# single_issuer_exposure = aig_nav.groupby(['Underlying Debt Transaction']).sum()['Exposure'].reset_index()
# single_issuer_exposure.rename(columns={'Exposure':'Single Issuer Exposure'}, inplace=True)
# aig_nav = aig_nav.merge(single_issuer_exposure, how='left', on=['Underlying Debt Transaction'])
# aig_nav['duplicated_issuer'] = aig_nav['Single Issuer Exposure'].duplicated()
# aig_nav['Single Issuer Exposure'] = np.where(aig_nav['duplicated_issuer']==True,0,aig_nav['Single Issuer Exposure'])
# aig_nav['ValueDate']= pd.to_datetime(datetime_obj_end)
# aig_nav['InstrumentType']= 'UNLISTED LOAN'
# aig_nav['Mod Dur']= 0.25
# aig_nav['Issuer']= ''
# aig_nav['Single Industry Exposure']= ''
# aig_nav['Weighted Duration']= ''
# aig_nav['Classification']= ''
# aig_nav.rename(columns={'Underlying Debt Transaction': 'InstrumentCode', 'Tranche':'Instrument Name','Exposure':'%Market Value','Value':'All-in Market Value-Val','Maturity Date':'Inst Maty Dt','Total Yield':'Yield'}, inplace=True)
# aig_nav = aig_nav[['ValueDate','InstrumentCode','Instrument Name','InstrumentType','%Market Value','Issuer','All-in Market Value-Val','Inst Maty Dt','Yield','Mod Dur','Time to Maturity (days)','Single Issuer Exposure','Industry','Single Industry Exposure','Weighted Duration','Issuer Type','Guarantee','Collateralization','National Rating','Global Rating','Source','PD','LGD','Classification']]
# aig_nav = aig_nav.fillna('')

# aig_nav.to_excel(writer,'FNB Life Credit', index=False)

#************************************************************************************************************************************************************************************
# 'FNB IBNR RPF'

# Config file
listed = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\config\compliance.xlsx', sheet_name='listed')
unlisted = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\config\compliance.xlsx', sheet_name='unlisted')

sql = "SELECT ValueDate, InstrumentCode, InstrumentCode AS 'Instrument Name', InstrumentType, IssuerName, MtmValuation AS 'All-in Market Value-Val', InstrumentMaturityDate AS 'Inst Maty Dt', TradedRate, MtmRate, PV01 FROM dbo.ValuationExtended WHERE ValueDate = " + " ' " + datetime_obj_end + "'" + " AND PortfolioCode IN ('17782','17688')"
df = pd.read_sql(sql, db)
df['IssuerName'] = df['IssuerName'].str.upper()
df['InstrumentCode'] = df['InstrumentCode'].str.upper()
df['Yield'] = np.where(df['TradedRate']==0,df['MtmRate'],df['TradedRate'])
df['Mod Dur'] = df['PV01']*-10000/df['All-in Market Value-Val']
df = df[df['InstrumentCode'].str.contains('LC17G|DC16E|IN304U1907|IN304U|LL19L04004')==False]
df = df[df['InstrumentType']!='Deposit']
df['%Market Value'] = df['All-in Market Value-Val']/df['All-in Market Value-Val'].sum()
df['Time to Maturity (days)'] = (pd.to_datetime(df['Inst Maty Dt']) - pd.to_datetime(df['ValueDate'])).dt.days
df['Time to Maturity (days)'] = df['Time to Maturity (days)'].fillna(0)
df['Weighted Duration'] = df['%Market Value']* df['Mod Dur']
df = df.merge(listed, how='left', on=['InstrumentCode'])
# single_issuer_exposure
single_issuer_exposure = df.groupby(['Issuer']).sum()['%Market Value'].reset_index()
single_issuer_exposure.rename(columns={'%Market Value':'Single Issuer Exposure'}, inplace=True)
df = df.merge(single_issuer_exposure, how='left', on=['Issuer'])
df['duplicated_issuer'] = df['Single Issuer Exposure'].duplicated()
df['Single Issuer Exposure'] = np.where(df['duplicated_issuer']==True,0,df['Single Issuer Exposure'])
# single_issuer_exposure
single_industry_exposure = df.groupby(['Industry']).sum()['%Market Value'].reset_index()
single_industry_exposure.rename(columns={'%Market Value':'Single Industry Exposure'}, inplace=True)
df = df.merge(single_industry_exposure, how='left', on=['Industry'])
df['duplicated_industry'] = df['Single Industry Exposure'].duplicated()
df['Single Industry Exposure'] = np.where(df['duplicated_industry']==True,0,df['Single Industry Exposure'])

df.drop(['MtmRate','TradedRate','PV01','duplicated_issuer','duplicated_industry'], axis=1, inplace=True)
df = df[['ValueDate','InstrumentCode','Instrument Name','InstrumentType','%Market Value','All-in Market Value-Val','Issuer','Yield','Inst Maty Dt','Mod Dur','Time to Maturity (days)','Single Issuer Exposure','Industry','Single Industry Exposure','Weighted Duration','Issuer Type','Guarantee','National Rating','Global Rating','Source','PD','LGD','Collateralization','Classification','IssuerName','Status']]
df = df.sort_values(by=['Issuer','InstrumentType'], ascending=False)

unclasified = df[df['National Rating'].isnull()]
unclasified = unclasified[['ValueDate','InstrumentCode','InstrumentType','Inst Maty Dt','IssuerName']]
unclasified_df = unclasified_df.append(unclasified)

df.to_excel(writer,'FNB IBNR RPF', index=False)


#************************************************************************************************************************************************************************************
# 'FNB IBNR IPF'

# Config file
listed = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\config\compliance.xlsx', sheet_name='listed')
unlisted = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\config\compliance.xlsx', sheet_name='unlisted')

sql = "SELECT ValueDate, InstrumentCode, InstrumentCode AS 'Instrument Name', InstrumentType, IssuerName, MtmValuation AS 'All-in Market Value-Val', InstrumentMaturityDate AS 'Inst Maty Dt', TradedRate, MtmRate, PV01 FROM dbo.ValuationExtended WHERE ValueDate = " + " ' " + datetime_obj_end + "'" + " AND PortfolioCode IN ('17689','16997')"
df = pd.read_sql(sql, db)
df['IssuerName'] = df['IssuerName'].str.upper()
df['InstrumentCode'] = df['InstrumentCode'].str.upper()
df['Yield'] = np.where(df['TradedRate']==0,df['MtmRate'],df['TradedRate'])
df['Mod Dur'] = df['PV01']*-10000/df['All-in Market Value-Val']
df = df[df['InstrumentCode'].str.contains('LC17G|DC16E|IN304U1907|IN304U|LL19L04004')==False]
df = df[df['InstrumentType']!='Deposit']
df['%Market Value'] = df['All-in Market Value-Val']/df['All-in Market Value-Val'].sum()
df['Time to Maturity (days)'] = (pd.to_datetime(df['Inst Maty Dt']) - pd.to_datetime(df['ValueDate'])).dt.days
df['Time to Maturity (days)'] = df['Time to Maturity (days)'].fillna(0)
df['Weighted Duration'] = df['%Market Value']* df['Mod Dur']
df = df.merge(listed, how='left', on=['InstrumentCode'])
# single_issuer_exposure
single_issuer_exposure = df.groupby(['Issuer']).sum()['%Market Value'].reset_index()
single_issuer_exposure.rename(columns={'%Market Value':'Single Issuer Exposure'}, inplace=True)
df = df.merge(single_issuer_exposure, how='left', on=['Issuer'])
df['duplicated_issuer'] = df['Single Issuer Exposure'].duplicated()
df['Single Issuer Exposure'] = np.where(df['duplicated_issuer']==True,0,df['Single Issuer Exposure'])
# single_issuer_exposure
single_industry_exposure = df.groupby(['Industry']).sum()['%Market Value'].reset_index()
single_industry_exposure.rename(columns={'%Market Value':'Single Industry Exposure'}, inplace=True)
df = df.merge(single_industry_exposure, how='left', on=['Industry'])
df['duplicated_industry'] = df['Single Industry Exposure'].duplicated()
df['Single Industry Exposure'] = np.where(df['duplicated_industry']==True,0,df['Single Industry Exposure'])

df.drop(['MtmRate','TradedRate','PV01','duplicated_issuer','duplicated_industry'], axis=1, inplace=True)
df = df[['ValueDate','InstrumentCode','Instrument Name','InstrumentType','%Market Value','All-in Market Value-Val','Issuer','Yield','Inst Maty Dt','Mod Dur','Time to Maturity (days)','Single Issuer Exposure','Industry','Single Industry Exposure','Weighted Duration','Issuer Type','Guarantee','National Rating','Global Rating','Source','PD','LGD','Collateralization','Classification','IssuerName','Status']]
df = df.sort_values(by=['Issuer','InstrumentType'], ascending=False)

unclasified = df[df['National Rating'].isnull()]
unclasified = unclasified[['ValueDate','InstrumentCode','InstrumentType','Inst Maty Dt','IssuerName']]
unclasified_df = unclasified_df.append(unclasified)

df.to_excel(writer,'FNB IBNR IPF', index=False)


#************************************************************************************************************************************************************************************
# 'FNB FLI LT Cap'

# Config file
listed = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\config\compliance.xlsx', sheet_name='listed')
unlisted = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\config\compliance.xlsx', sheet_name='unlisted')

sql = "SELECT ValueDate, InstrumentCode, InstrumentCode AS 'Instrument Name', InstrumentType, IssuerName, MtmValuation AS 'All-in Market Value-Val', InstrumentMaturityDate AS 'Inst Maty Dt', TradedRate, MtmRate, PV01 FROM dbo.ValuationExtended WHERE ValueDate = " + " ' " + datetime_obj_end + "'" + " AND PortfolioCode IN ('19783')"
df = pd.read_sql(sql, db)
df['IssuerName'] = df['IssuerName'].str.upper()
df['InstrumentCode'] = df['InstrumentCode'].str.upper()
df['Yield'] = np.where(df['TradedRate']==0,df['MtmRate'],df['TradedRate'])
df['Mod Dur'] = df['PV01']*-10000/df['All-in Market Value-Val']
df = df[df['InstrumentCode'].str.contains('LC17G|DC16E|IN304U1907|IN304U|LL19L04004')==False]
df = df[df['InstrumentType']!='Deposit']
df['%Market Value'] = df['All-in Market Value-Val']/df['All-in Market Value-Val'].sum()
df['Time to Maturity (days)'] = (pd.to_datetime(df['Inst Maty Dt']) - pd.to_datetime(df['ValueDate'])).dt.days
df['Time to Maturity (days)'] = df['Time to Maturity (days)'].fillna(0)
df['Weighted Duration'] = df['%Market Value']* df['Mod Dur']
df = df.merge(listed, how='left', on=['InstrumentCode'])
# single_issuer_exposure
single_issuer_exposure = df.groupby(['Issuer']).sum()['%Market Value'].reset_index()
single_issuer_exposure.rename(columns={'%Market Value':'Single Issuer Exposure'}, inplace=True)
df = df.merge(single_issuer_exposure, how='left', on=['Issuer'])
df['duplicated_issuer'] = df['Single Issuer Exposure'].duplicated()
df['Single Issuer Exposure'] = np.where(df['duplicated_issuer']==True,0,df['Single Issuer Exposure'])
# single_issuer_exposure
single_industry_exposure = df.groupby(['Industry']).sum()['%Market Value'].reset_index()
single_industry_exposure.rename(columns={'%Market Value':'Single Industry Exposure'}, inplace=True)
df = df.merge(single_industry_exposure, how='left', on=['Industry'])
df['duplicated_industry'] = df['Single Industry Exposure'].duplicated()
df['Single Industry Exposure'] = np.where(df['duplicated_industry']==True,0,df['Single Industry Exposure'])

df.drop(['MtmRate','TradedRate','PV01','duplicated_issuer','duplicated_industry'], axis=1, inplace=True)
df = df[['ValueDate','InstrumentCode','Instrument Name','InstrumentType','%Market Value','All-in Market Value-Val','Issuer','Yield','Inst Maty Dt','Mod Dur','Time to Maturity (days)','Single Issuer Exposure','Industry','Single Industry Exposure','Weighted Duration','Issuer Type','Guarantee','National Rating','Global Rating','Source','PD','LGD','Collateralization','Classification','IssuerName','Status']]
df = df.sort_values(by=['Issuer','InstrumentType'], ascending=False)

unclasified = df[df['National Rating'].isnull()]
unclasified = unclasified[['ValueDate','InstrumentCode','InstrumentType','Inst Maty Dt','IssuerName']]
unclasified_df = unclasified_df.append(unclasified)

df.to_excel(writer,'FNB FLI LT Cap', index=False)


#************************************************************************************************************************************************************************************
# 'FNB FLI Working'

# Config file
listed = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\config\compliance.xlsx', sheet_name='listed')
unlisted = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\config\compliance.xlsx', sheet_name='unlisted')

sql = "SELECT ValueDate, InstrumentCode, InstrumentCode AS 'Instrument Name', InstrumentType, IssuerName, MtmValuation AS 'All-in Market Value-Val', InstrumentMaturityDate AS 'Inst Maty Dt', TradedRate, MtmRate, PV01 FROM dbo.ValuationExtended WHERE ValueDate = " + " ' " + datetime_obj_end + "'" + " AND PortfolioCode IN ('19735')"
df = pd.read_sql(sql, db)
df['IssuerName'] = df['IssuerName'].str.upper()
df['InstrumentCode'] = df['InstrumentCode'].str.upper()
df['Yield'] = np.where(df['TradedRate']==0,df['MtmRate'],df['TradedRate'])
df['Mod Dur'] = df['PV01']*-10000/df['All-in Market Value-Val']
df = df[df['InstrumentCode'].str.contains('LC17G|DC16E|IN304U1907|IN304U|LL19L04004')==False]
df = df[df['InstrumentType']!='Deposit']
df['%Market Value'] = df['All-in Market Value-Val']/df['All-in Market Value-Val'].sum()
df['Time to Maturity (days)'] = (pd.to_datetime(df['Inst Maty Dt']) - pd.to_datetime(df['ValueDate'])).dt.days
df['Time to Maturity (days)'] = df['Time to Maturity (days)'].fillna(0)
df['Weighted Duration'] = df['%Market Value']* df['Mod Dur']
df = df.merge(listed, how='left', on=['InstrumentCode'])
# single_issuer_exposure
single_issuer_exposure = df.groupby(['Issuer']).sum()['%Market Value'].reset_index()
single_issuer_exposure.rename(columns={'%Market Value':'Single Issuer Exposure'}, inplace=True)
df = df.merge(single_issuer_exposure, how='left', on=['Issuer'])
df['duplicated_issuer'] = df['Single Issuer Exposure'].duplicated()
df['Single Issuer Exposure'] = np.where(df['duplicated_issuer']==True,0,df['Single Issuer Exposure'])
# single_issuer_exposure
single_industry_exposure = df.groupby(['Industry']).sum()['%Market Value'].reset_index()
single_industry_exposure.rename(columns={'%Market Value':'Single Industry Exposure'}, inplace=True)
df = df.merge(single_industry_exposure, how='left', on=['Industry'])
df['duplicated_industry'] = df['Single Industry Exposure'].duplicated()
df['Single Industry Exposure'] = np.where(df['duplicated_industry']==True,0,df['Single Industry Exposure'])

df.drop(['MtmRate','TradedRate','PV01','duplicated_issuer','duplicated_industry'], axis=1, inplace=True)
df = df[['ValueDate','InstrumentCode','Instrument Name','InstrumentType','%Market Value','All-in Market Value-Val','Issuer','Yield','Inst Maty Dt','Mod Dur','Time to Maturity (days)','Single Issuer Exposure','Industry','Single Industry Exposure','Weighted Duration','Issuer Type','Guarantee','National Rating','Global Rating','Source','PD','LGD','Collateralization','Classification','IssuerName','Status']]
df = df.sort_values(by=['Issuer','InstrumentType'], ascending=False)

unclasified = df[df['National Rating'].isnull()]
unclasified = unclasified[['ValueDate','InstrumentCode','InstrumentType','Inst Maty Dt','IssuerName']]
unclasified_df = unclasified_df.append(unclasified)

df.to_excel(writer,'FNB FLI Working', index=False)


#************************************************************************************************************************************************************************************
# # 'FNB SF Liquidity'

# # Config file
# listed = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\config\compliance.xlsx', sheet_name='listed')
# unlisted = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\config\compliance.xlsx', sheet_name='unlisted')

# sql = "SELECT ValueDate, InstrumentCode, InstrumentCode AS 'Instrument Name', InstrumentType, IssuerName, MtmValuation AS 'All-in Market Value-Val', InstrumentMaturityDate AS 'Inst Maty Dt', TradedRate, MtmRate, PV01 FROM dbo.ValuationExtended WHERE ValueDate = " + " ' " + datetime_obj_end + "'" + " AND PortfolioCode IN ('21958')"
# df = pd.read_sql(sql, db)
# df['IssuerName'] = df['IssuerName'].str.upper()
# df['InstrumentCode'] = df['InstrumentCode'].str.upper()
# df['Yield'] = np.where(df['TradedRate']==0,df['MtmRate'],df['TradedRate'])
# df['Mod Dur'] = df['PV01']*-10000/df['All-in Market Value-Val']
# df = df[df['InstrumentCode'].str.contains('LC17G|DC16E|IN304U1907|IN304U|LL19L04004')==False]
# df = df[df['InstrumentType']!='Deposit']
# df['%Market Value'] = df['All-in Market Value-Val']/df['All-in Market Value-Val'].sum()
# df['Time to Maturity (days)'] = (pd.to_datetime(df['Inst Maty Dt']) - pd.to_datetime(df['ValueDate'])).dt.days
# df['Time to Maturity (days)'] = df['Time to Maturity (days)'].fillna(0)
# df['Weighted Duration'] = df['%Market Value']* df['Mod Dur']
# df = df.merge(listed, how='left', on=['InstrumentCode'])
# # single_issuer_exposure
# single_issuer_exposure = df.groupby(['Issuer']).sum()['%Market Value'].reset_index()
# single_issuer_exposure.rename(columns={'%Market Value':'Single Issuer Exposure'}, inplace=True)
# df = df.merge(single_issuer_exposure, how='left', on=['Issuer'])
# df['duplicated_issuer'] = df['Single Issuer Exposure'].duplicated()
# df['Single Issuer Exposure'] = np.where(df['duplicated_issuer']==True,0,df['Single Issuer Exposure'])
# # single_issuer_exposure
# single_industry_exposure = df.groupby(['Industry']).sum()['%Market Value'].reset_index()
# single_industry_exposure.rename(columns={'%Market Value':'Single Industry Exposure'}, inplace=True)
# df = df.merge(single_industry_exposure, how='left', on=['Industry'])
# df['duplicated_industry'] = df['Single Industry Exposure'].duplicated()
# df['Single Industry Exposure'] = np.where(df['duplicated_industry']==True,0,df['Single Industry Exposure'])

# df.drop(['MtmRate','TradedRate','PV01','duplicated_issuer','duplicated_industry'], axis=1, inplace=True)
# df = df[['ValueDate','InstrumentCode','Instrument Name','InstrumentType','%Market Value','All-in Market Value-Val','Issuer','Yield','Inst Maty Dt','Mod Dur','Time to Maturity (days)','Single Issuer Exposure','Industry','Single Industry Exposure','Weighted Duration','Issuer Type','Guarantee','National Rating','Global Rating','Source','PD','LGD','Collateralization','Classification','IssuerName','Status']]
# df = df.sort_values(by=['Issuer','InstrumentType'], ascending=False)

# unclasified = df[df['National Rating'].isnull()]
# unclasified = unclasified[['ValueDate','InstrumentCode','InstrumentType','Inst Maty Dt','IssuerName']]
# unclasified_df = unclasified_df.append(unclasified)

# df.to_excel(writer,'FNB SF Liquidity', index=False)


#************************************************************************************************************************************************************************************
# 'Friscol'

constr = "DRIVER={SQL Server Native Client 11.0};SERVER=ash-prdkblddbao,4071;DATABASE=AshburtonRisk;Trusted_Connection=yes;"
db = odbc.odbc(constr)

# Config file
listed = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\config\compliance.xlsx', sheet_name='listed')
unlisted = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\config\compliance.xlsx', sheet_name='unlisted')

sql = "SELECT ValuationDate AS ValueDate, InstrumentCode, InstrumentLongName AS 'Instrument Name', BaseEffectiveExposure AS 'All-in Market Value-Val' FROM Investment.vwMaitlandHoldings WHERE ValuationDate = " + " ' " + datetime_obj_end + "'" + " AND PortfolioCode IN ('95921')"
df = pd.read_sql(sql, db)
df = df[(df['Instrument Name']!='MANAGEMENT FEES ZAR') & (df['Instrument Name']!='VAT ON MANAGEMENT FEES ZAR')]

sql = "SELECT InstrumentCode, IssuerName, InstrumentTypeDescription AS InstrumentType, InterestRate AS Yield, MaturityDate AS 'Inst Maty Dt', ModifiedDuration AS 'Mod Dur', ISIN FROM Investment.MaitlandASISAInstruments WHERE DataDate = " + " ' " + datetime_obj_end + "'" + " AND PortfolioIDCode IN ('95921')"
df_static = pd.read_sql(sql, db)
#df_static['InstrumentCode'] = np.where(df_static['ISIN'].str[:3] == 'ZAM',df_static['ISIN'], df_static['InstrumentCode'])
#df_static = df_static.drop(['ISIN'], axis=1)
df_static = df_static.drop_duplicates()

df = df.merge(df_static, how='left', on=['InstrumentCode'])
df['InstrumentCode'] = df['InstrumentCode'].apply(lambda x: x.replace('CASH','SOUTH AFRICAN RAND I'))

df['IssuerName'] = df['IssuerName'].str.upper()
df['InstrumentCode'] = df['InstrumentCode'].str.upper()
df = df[df.InstrumentCode.str.contains('EXPENSE') == False]
df['%Market Value'] = df['All-in Market Value-Val']/df['All-in Market Value-Val'].sum()
df['Time to Maturity (days)'] = (pd.to_datetime(df['Inst Maty Dt']) - pd.to_datetime(df['ValueDate'])).dt.days
df['Time to Maturity (days)'] = df['Time to Maturity (days)'].fillna(0)
df['Weighted Duration'] = df['%Market Value']* df['Mod Dur']
df = df.merge(listed, how='left', on=['InstrumentCode'])
# single_issuer_exposure
single_issuer_exposure = df.groupby(['Issuer']).sum()['%Market Value'].reset_index()
single_issuer_exposure.rename(columns={'%Market Value':'Single Issuer Exposure'}, inplace=True)
df = df.merge(single_issuer_exposure, how='left', on=['Issuer'])
df['duplicated_issuer'] = df['Single Issuer Exposure'].duplicated()
df['Single Issuer Exposure'] = np.where(df['duplicated_issuer']==True,0,df['Single Issuer Exposure'])
# single_issuer_exposure
single_industry_exposure = df.groupby(['Industry']).sum()['%Market Value'].reset_index()
single_industry_exposure.rename(columns={'%Market Value':'Single Industry Exposure'}, inplace=True)
df = df.merge(single_industry_exposure, how='left', on=['Industry'])
df['duplicated_industry'] = df['Single Industry Exposure'].duplicated()
df['Single Industry Exposure'] = np.where(df['duplicated_industry']==True,0,df['Single Industry Exposure'])

df.drop(['duplicated_issuer','duplicated_industry'], axis=1, inplace=True)
df = df[['ValueDate','InstrumentCode','Instrument Name','InstrumentType','%Market Value','All-in Market Value-Val','Issuer','Yield','Inst Maty Dt','Mod Dur','Time to Maturity (days)','Single Issuer Exposure','Industry','Single Industry Exposure','Weighted Duration','Issuer Type','Guarantee','National Rating','Global Rating','Source','PD','LGD','Collateralization','Classification','IssuerName','Status']]
df = df.sort_values(by=['Issuer','InstrumentType'], ascending=False)

unclasified = df[df['National Rating'].isnull()]
unclasified = unclasified[['ValueDate','InstrumentCode','InstrumentType','Inst Maty Dt','IssuerName']]
unclasified_df = unclasified_df.append(unclasified)

df.to_excel(writer,'Friscol', index=False)


#************************************************************************************************************************************************************************************


# 'Friscol2'

constr = "DRIVER={SQL Server Native Client 11.0};SERVER=ash-prdkblddbao,4071;DATABASE=AshburtonRisk;Trusted_Connection=yes;"
db = odbc.odbc(constr)

# Config file
listed = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\config\compliance.xlsx', sheet_name='listed')
unlisted = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\config\compliance.xlsx', sheet_name='unlisted')

sql = "SELECT ValuationDate AS ValueDate, InstrumentCode, InstrumentLongName AS 'Instrument Name', BaseEffectiveExposure AS 'All-in Market Value-Val' FROM Investment.vwMaitlandHoldings WHERE ValuationDate = " + " ' " + datetime_obj_end + "'" + " AND PortfolioCode IN ('95955')"
df = pd.read_sql(sql, db)
df = df[(df['Instrument Name']!='MANAGEMENT FEES ZAR') & (df['Instrument Name']!='VAT ON MANAGEMENT FEES ZAR')]

sql = "SELECT InstrumentCode, IssuerName, InstrumentTypeDescription AS InstrumentType, InterestRate AS Yield, MaturityDate AS 'Inst Maty Dt', ModifiedDuration AS 'Mod Dur', ISIN FROM Investment.MaitlandASISAInstruments WHERE DataDate = " + " ' " + datetime_obj_end + "'" + " AND PortfolioIDCode IN ('95955')"
df_static = pd.read_sql(sql, db)
#df_static['InstrumentCode'] = np.where(df_static['ISIN'].str[:3] == 'ZAM',df_static['ISIN'], df_static['InstrumentCode'])
#df_static = df_static.drop(['ISIN'], axis=1)
df_static = df_static.drop_duplicates()
df = df.merge(df_static, how='left', on=['InstrumentCode'])
df['InstrumentCode'] = df['InstrumentCode'].apply(lambda x: x.replace('CASH','SOUTH AFRICAN RAND I'))

df['IssuerName'] = df['IssuerName'].str.upper()
df['InstrumentCode'] = df['InstrumentCode'].str.upper()
df = df[df.InstrumentCode.str.contains('EXPENSE') == False]
df['%Market Value'] = df['All-in Market Value-Val']/df['All-in Market Value-Val'].sum()
df['Time to Maturity (days)'] = (pd.to_datetime(df['Inst Maty Dt']) - pd.to_datetime(df['ValueDate'])).dt.days
df['Time to Maturity (days)'] = df['Time to Maturity (days)'].fillna(0)
df['Weighted Duration'] = df['%Market Value']* df['Mod Dur']
df = df.merge(listed, how='left', on=['InstrumentCode'])
# single_issuer_exposure
single_issuer_exposure = df.groupby(['Issuer']).sum()['%Market Value'].reset_index()
single_issuer_exposure.rename(columns={'%Market Value':'Single Issuer Exposure'}, inplace=True)
df = df.merge(single_issuer_exposure, how='left', on=['Issuer'])
df['duplicated_issuer'] = df['Single Issuer Exposure'].duplicated()
df['Single Issuer Exposure'] = np.where(df['duplicated_issuer']==True,0,df['Single Issuer Exposure'])
# single_issuer_exposure
single_industry_exposure = df.groupby(['Industry']).sum()['%Market Value'].reset_index()
single_industry_exposure.rename(columns={'%Market Value':'Single Industry Exposure'}, inplace=True)
df = df.merge(single_industry_exposure, how='left', on=['Industry'])
df['duplicated_industry'] = df['Single Industry Exposure'].duplicated()
df['Single Industry Exposure'] = np.where(df['duplicated_industry']==True,0,df['Single Industry Exposure'])

df.drop(['duplicated_issuer','duplicated_industry'], axis=1, inplace=True)
df = df[['ValueDate','InstrumentCode','Instrument Name','InstrumentType','%Market Value','All-in Market Value-Val','Issuer','Yield','Inst Maty Dt','Mod Dur','Time to Maturity (days)','Single Issuer Exposure','Industry','Single Industry Exposure','Weighted Duration','Issuer Type','Guarantee','National Rating','Global Rating','Source','PD','LGD','Collateralization','Classification','IssuerName','Status']]
df = df.sort_values(by=['Issuer','InstrumentType'], ascending=False)

unclasified = df[df['National Rating'].isnull()]
unclasified = unclasified[['ValueDate','InstrumentCode','InstrumentType','Inst Maty Dt','IssuerName']]
unclasified_df = unclasified_df.append(unclasified)

df.to_excel(writer,'Friscol2', index=False)


#************************************************************************************************************************************************************************************


# 'Assupol'

constr = "DRIVER={SQL Server Native Client 11.0};SERVER=ash-prdkblddbao,4071;DATABASE=AshburtonRisk;Trusted_Connection=yes;"
db = odbc.odbc(constr)

# Config file
listed = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\config\compliance.xlsx', sheet_name='listed')
unlisted = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\config\compliance.xlsx', sheet_name='unlisted')

sql = "SELECT ValuationDate AS ValueDate, InstrumentCode, InstrumentLongName AS 'Instrument Name', BaseEffectiveExposure AS 'All-in Market Value-Val' FROM Investment.vwMaitlandHoldings WHERE ValuationDate = " + " ' " + datetime_obj_end + "'" + " AND PortfolioCode IN ('95031')"
df = pd.read_sql(sql, db)
df = df[(df['Instrument Name']!='MANAGEMENT FEES ZAR') & (df['Instrument Name']!='VAT ON MANAGEMENT FEES ZAR')]

sql = "SELECT InstrumentCode, IssuerName, InstrumentTypeDescription AS InstrumentType, InterestRate AS Yield, MaturityDate AS 'Inst Maty Dt', ModifiedDuration AS 'Mod Dur', ISIN FROM Investment.MaitlandASISAInstruments WHERE DataDate = " + " ' " + datetime_obj_end + "'" + " AND PortfolioIDCode IN ('95031')"
df_static = pd.read_sql(sql, db)
#df_static['InstrumentCode'] = np.where(df_static['ISIN'].str[:3] == 'ZAM',df_static['ISIN'], df_static['InstrumentCode'])
#df_static = df_static.drop(['ISIN'], axis=1)
df_static = df_static.drop_duplicates()
df = df.merge(df_static, how='left', on=['InstrumentCode'])
df['InstrumentCode'] = df['InstrumentCode'].apply(lambda x: x.replace('CASH','SOUTH AFRICAN RAND I'))

df['IssuerName'] = df['IssuerName'].str.upper()
df['InstrumentCode'] = df['InstrumentCode'].str.upper()
df = df[df.InstrumentCode.str.contains('EXPENSE') == False]
df['%Market Value'] = df['All-in Market Value-Val']/df['All-in Market Value-Val'].sum()
df['Time to Maturity (days)'] = (pd.to_datetime(df['Inst Maty Dt']) - pd.to_datetime(df['ValueDate'])).dt.days
df['Time to Maturity (days)'] = df['Time to Maturity (days)'].fillna(0)
df['Weighted Duration'] = df['%Market Value']* df['Mod Dur']
df = df.merge(listed, how='left', on=['InstrumentCode'])
# single_issuer_exposure
single_issuer_exposure = df.groupby(['Issuer']).sum()['%Market Value'].reset_index()
single_issuer_exposure.rename(columns={'%Market Value':'Single Issuer Exposure'}, inplace=True)
df = df.merge(single_issuer_exposure, how='left', on=['Issuer'])
df['duplicated_issuer'] = df['Single Issuer Exposure'].duplicated()
df['Single Issuer Exposure'] = np.where(df['duplicated_issuer']==True,0,df['Single Issuer Exposure'])
# single_issuer_exposure
single_industry_exposure = df.groupby(['Industry']).sum()['%Market Value'].reset_index()
single_industry_exposure.rename(columns={'%Market Value':'Single Industry Exposure'}, inplace=True)
df = df.merge(single_industry_exposure, how='left', on=['Industry'])
df['duplicated_industry'] = df['Single Industry Exposure'].duplicated()
df['Single Industry Exposure'] = np.where(df['duplicated_industry']==True,0,df['Single Industry Exposure'])

df.drop(['duplicated_issuer','duplicated_industry'], axis=1, inplace=True)
df = df[['ValueDate','InstrumentCode','Instrument Name','InstrumentType','%Market Value','All-in Market Value-Val','Issuer','Yield','Inst Maty Dt','Mod Dur','Time to Maturity (days)','Single Issuer Exposure','Industry','Single Industry Exposure','Weighted Duration','Issuer Type','Guarantee','National Rating','Global Rating','Source','PD','LGD','Collateralization','Classification','IssuerName','Status']]
df = df.sort_values(by=['Issuer','InstrumentType'], ascending=False)

unclasified = df[df['National Rating'].isnull()]
unclasified = unclasified[['ValueDate','InstrumentCode','InstrumentType','Inst Maty Dt','IssuerName']]
unclasified_df = unclasified_df.append(unclasified)

df.to_excel(writer,'Assupol', index=False)


#************************************************************************************************************************************************************************************



# 'Outsurance'

constr = "DRIVER={SQL Server Native Client 11.0};SERVER=ash-prdkblddbao,4071;DATABASE=AshburtonRisk;Trusted_Connection=yes;"
db = odbc.odbc(constr)

# Config file
listed = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\config\compliance.xlsx', sheet_name='listed')
unlisted = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\config\compliance.xlsx', sheet_name='unlisted')

sql = "SELECT ValuationDate AS ValueDate, InstrumentCode, InstrumentLongName AS 'Instrument Name', BaseEffectiveExposure AS 'All-in Market Value-Val' FROM Investment.vwMaitlandHoldings WHERE ValuationDate = " + " ' " + datetime_obj_end + "'" + " AND PortfolioCode IN ('95923')"
df = pd.read_sql(sql, db)
df = df[(df['Instrument Name']!='MANAGEMENT FEES ZAR') & (df['Instrument Name']!='VAT ON MANAGEMENT FEES ZAR')]

sql = "SELECT InstrumentCode, IssuerName, InstrumentTypeDescription AS InstrumentType, InterestRate AS Yield, MaturityDate AS 'Inst Maty Dt', ModifiedDuration AS 'Mod Dur', ISIN FROM Investment.MaitlandASISAInstruments WHERE DataDate = " + " ' " + datetime_obj_end + "'" + " AND PortfolioIDCode IN ('95923')"
df_static = pd.read_sql(sql, db)
#df_static['InstrumentCode'] = np.where(df_static['ISIN'].str[:3] == 'ZAM',df_static['ISIN'], df_static['InstrumentCode'])
#df_static = df_static.drop(['ISIN'], axis=1)
df_static = df_static.drop_duplicates()

df = df.merge(df_static, how='left', on=['InstrumentCode'])
df['InstrumentCode'] = df['InstrumentCode'].apply(lambda x: x.replace('CASH','SOUTH AFRICAN RAND I'))

df['IssuerName'] = df['IssuerName'].str.upper()
df['InstrumentCode'] = df['InstrumentCode'].str.upper()
df = df[df.InstrumentCode.str.contains('EXPENSE') == False]
df['%Market Value'] = df['All-in Market Value-Val']/df['All-in Market Value-Val'].sum()
df['Time to Maturity (days)'] = (pd.to_datetime(df['Inst Maty Dt']) - pd.to_datetime(df['ValueDate'])).dt.days
df['Time to Maturity (days)'] = df['Time to Maturity (days)'].fillna(0)
df['Weighted Duration'] = df['%Market Value']* df['Mod Dur']
df = df.merge(listed, how='left', on=['InstrumentCode'])
# single_issuer_exposure
single_issuer_exposure = df.groupby(['Issuer']).sum()['%Market Value'].reset_index()
single_issuer_exposure.rename(columns={'%Market Value':'Single Issuer Exposure'}, inplace=True)
df = df.merge(single_issuer_exposure, how='left', on=['Issuer'])
df['duplicated_issuer'] = df['Single Issuer Exposure'].duplicated()
df['Single Issuer Exposure'] = np.where(df['duplicated_issuer']==True,0,df['Single Issuer Exposure'])
# single_issuer_exposure
single_industry_exposure = df.groupby(['Industry']).sum()['%Market Value'].reset_index()
single_industry_exposure.rename(columns={'%Market Value':'Single Industry Exposure'}, inplace=True)
df = df.merge(single_industry_exposure, how='left', on=['Industry'])
df['duplicated_industry'] = df['Single Industry Exposure'].duplicated()
df['Single Industry Exposure'] = np.where(df['duplicated_industry']==True,0,df['Single Industry Exposure'])

df.drop(['duplicated_issuer','duplicated_industry'], axis=1, inplace=True)
df = df[['ValueDate','InstrumentCode','Instrument Name','InstrumentType','%Market Value','All-in Market Value-Val','Issuer','Yield','Inst Maty Dt','Mod Dur','Time to Maturity (days)','Single Issuer Exposure','Industry','Single Industry Exposure','Weighted Duration','Issuer Type','Guarantee','National Rating','Global Rating','Source','PD','LGD','Collateralization','Classification','IssuerName','Status']]
df = df.sort_values(by=['Issuer','InstrumentType'], ascending=False)

unclasified = df[df['National Rating'].isnull()]
unclasified = unclasified[['ValueDate','InstrumentCode','InstrumentType','Inst Maty Dt','IssuerName']]
unclasified_df = unclasified_df.append(unclasified)

df.to_excel(writer,'Outsurance', index=False)

#************************************************************************************************************************************************************************************

# 'AIG SA LDI BOND'

constr = "DRIVER={SQL Server Native Client 11.0};SERVER=ash-prdkblddbao,4071;DATABASE=AshburtonRisk;Trusted_Connection=yes;"
db = odbc.odbc(constr)

# Config file
listed = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\config\compliance.xlsx', sheet_name='listed')
unlisted = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\config\compliance.xlsx', sheet_name='unlisted')

sql = "SELECT ValuationDate AS ValueDate, InstrumentCode, InstrumentLongName AS 'Instrument Name', BaseEffectiveExposure AS 'All-in Market Value-Val' FROM Investment.vwMaitlandHoldings WHERE ValuationDate = " + " ' " + datetime_obj_end + "'" + " AND PortfolioCode IN ('95949')"
df = pd.read_sql(sql, db)
df = df[(df['Instrument Name']!='MANAGEMENT FEES ZAR') & (df['Instrument Name']!='VAT ON MANAGEMENT FEES ZAR')]

sql = "SELECT InstrumentCode, IssuerName, InstrumentTypeDescription AS InstrumentType, InterestRate AS Yield, MaturityDate AS 'Inst Maty Dt', ModifiedDuration AS 'Mod Dur', ISIN FROM Investment.MaitlandASISAInstruments WHERE DataDate = " + " ' " + datetime_obj_end + "'" + " AND PortfolioIDCode IN ('95949')"
df_static = pd.read_sql(sql, db)
#df_static['InstrumentCode'] = np.where(df_static['ISIN'].str[:3] == 'ZAM',df_static['ISIN'], df_static['InstrumentCode'])
#df_static = df_static.drop(['ISIN'], axis=1)
df_static = df_static.drop_duplicates()

df = df.merge(df_static, how='left', on=['InstrumentCode'])
df['InstrumentCode'] = df['InstrumentCode'].apply(lambda x: x.replace('CASH','SOUTH AFRICAN RAND I'))

df['IssuerName'] = df['IssuerName'].str.upper()
df['InstrumentCode'] = df['InstrumentCode'].str.upper()
df = df[df.InstrumentCode.str.contains('EXPENSE') == False]
df['%Market Value'] = df['All-in Market Value-Val']/df['All-in Market Value-Val'].sum()
df['Time to Maturity (days)'] = (pd.to_datetime(df['Inst Maty Dt']) - pd.to_datetime(df['ValueDate'])).dt.days
df['Time to Maturity (days)'] = df['Time to Maturity (days)'].fillna(0)
df['Weighted Duration'] = df['%Market Value']* df['Mod Dur']
df = df.merge(listed, how='left', on=['InstrumentCode'])
# single_issuer_exposure
single_issuer_exposure = df.groupby(['Issuer']).sum()['%Market Value'].reset_index()
single_issuer_exposure.rename(columns={'%Market Value':'Single Issuer Exposure'}, inplace=True)
df = df.merge(single_issuer_exposure, how='left', on=['Issuer'])
df['duplicated_issuer'] = df['Single Issuer Exposure'].duplicated()
df['Single Issuer Exposure'] = np.where(df['duplicated_issuer']==True,0,df['Single Issuer Exposure'])
# single_issuer_exposure
single_industry_exposure = df.groupby(['Industry']).sum()['%Market Value'].reset_index()
single_industry_exposure.rename(columns={'%Market Value':'Single Industry Exposure'}, inplace=True)
df = df.merge(single_industry_exposure, how='left', on=['Industry'])
df['duplicated_industry'] = df['Single Industry Exposure'].duplicated()
df['Single Industry Exposure'] = np.where(df['duplicated_industry']==True,0,df['Single Industry Exposure'])

df.drop(['duplicated_issuer','duplicated_industry'], axis=1, inplace=True)
df = df[['ValueDate','InstrumentCode','Instrument Name','InstrumentType','%Market Value','All-in Market Value-Val','Issuer','Yield','Inst Maty Dt','Mod Dur','Time to Maturity (days)','Single Issuer Exposure','Industry','Single Industry Exposure','Weighted Duration','Issuer Type','Guarantee','National Rating','Global Rating','Source','PD','LGD','Collateralization','Classification','IssuerName','Status']]
df = df.sort_values(by=['Issuer','InstrumentType'], ascending=False)

unclasified = df[df['National Rating'].isnull()]
unclasified = unclasified[['ValueDate','InstrumentCode','InstrumentType','Inst Maty Dt','IssuerName']]
unclasified_df = unclasified_df.append(unclasified)

df.to_excel(writer,'AIG SA LDI BONDS', index=False)

#*********************************************************************************************************************************************************


# 'AIG LIFE LDI BOND'

constr = "DRIVER={SQL Server Native Client 11.0};SERVER=ash-prdkblddbao,4071;DATABASE=AshburtonRisk;Trusted_Connection=yes;"
db = odbc.odbc(constr)

# Config file
listed = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\config\compliance.xlsx', sheet_name='listed')
unlisted = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\config\compliance.xlsx', sheet_name='unlisted')

sql = "SELECT ValuationDate AS ValueDate, InstrumentCode, InstrumentLongName AS 'Instrument Name', BaseEffectiveExposure AS 'All-in Market Value-Val' FROM Investment.vwMaitlandHoldings WHERE ValuationDate = " + " ' " + datetime_obj_end + "'" + " AND PortfolioCode IN ('95950')"
df = pd.read_sql(sql, db)
df = df[(df['Instrument Name']!='MANAGEMENT FEES ZAR') & (df['Instrument Name']!='VAT ON MANAGEMENT FEES ZAR')]

sql = "SELECT InstrumentCode, IssuerName, InstrumentTypeDescription AS InstrumentType, InterestRate AS Yield, MaturityDate AS 'Inst Maty Dt', ModifiedDuration AS 'Mod Dur', ISIN FROM Investment.MaitlandASISAInstruments WHERE DataDate = " + " ' " + datetime_obj_end + "'" + " AND PortfolioIDCode IN ('95950')"
#df_static = pd.read_sql(sql, db)
#df_static['InstrumentCode'] = np.where(df_static['ISIN'].str[:3] == 'ZAM',df_static['ISIN'], df_static['InstrumentCode'])
df_static = df_static.drop(['ISIN'], axis=1)
df_static = df_static.drop_duplicates()

df = df.merge(df_static, how='left', on=['InstrumentCode'])
df['InstrumentCode'] = df['InstrumentCode'].apply(lambda x: x.replace('CASH','SOUTH AFRICAN RAND I'))

df['IssuerName'] = df['IssuerName'].str.upper()
df['InstrumentCode'] = df['InstrumentCode'].str.upper()
df = df[df.InstrumentCode.str.contains('EXPENSE') == False]
df['%Market Value'] = df['All-in Market Value-Val']/df['All-in Market Value-Val'].sum()
df['Time to Maturity (days)'] = (pd.to_datetime(df['Inst Maty Dt']) - pd.to_datetime(df['ValueDate'])).dt.days
df['Time to Maturity (days)'] = df['Time to Maturity (days)'].fillna(0)
df['Weighted Duration'] = df['%Market Value']* df['Mod Dur']
df = df.merge(listed, how='left', on=['InstrumentCode'])
# single_issuer_exposure
single_issuer_exposure = df.groupby(['Issuer']).sum()['%Market Value'].reset_index()
single_issuer_exposure.rename(columns={'%Market Value':'Single Issuer Exposure'}, inplace=True)
df = df.merge(single_issuer_exposure, how='left', on=['Issuer'])
df['duplicated_issuer'] = df['Single Issuer Exposure'].duplicated()
df['Single Issuer Exposure'] = np.where(df['duplicated_issuer']==True,0,df['Single Issuer Exposure'])
# single_issuer_exposure
single_industry_exposure = df.groupby(['Industry']).sum()['%Market Value'].reset_index()
single_industry_exposure.rename(columns={'%Market Value':'Single Industry Exposure'}, inplace=True)
df = df.merge(single_industry_exposure, how='left', on=['Industry'])
df['duplicated_industry'] = df['Single Industry Exposure'].duplicated()
df['Single Industry Exposure'] = np.where(df['duplicated_industry']==True,0,df['Single Industry Exposure'])

df.drop(['duplicated_issuer','duplicated_industry'], axis=1, inplace=True)
df = df[['ValueDate','InstrumentCode','Instrument Name','InstrumentType','%Market Value','All-in Market Value-Val','Issuer','Yield','Inst Maty Dt','Mod Dur','Time to Maturity (days)','Single Issuer Exposure','Industry','Single Industry Exposure','Weighted Duration','Issuer Type','Guarantee','National Rating','Global Rating','Source','PD','LGD','Collateralization','Classification','IssuerName','Status']]
df = df.sort_values(by=['Issuer','InstrumentType'], ascending=False)

unclasified = df[df['National Rating'].isnull()]
unclasified = unclasified[['ValueDate','InstrumentCode','InstrumentType','Inst Maty Dt','IssuerName']]
unclasified_df = unclasified_df.append(unclasified)

df.to_excel(writer,'AIG LIFE LDI BONDS', index=False)

#*********************************************************************************************************************************************************


# 'AIG SA CREDIT'

constr = "DRIVER={SQL Server Native Client 11.0};SERVER=ash-prdkblddbao,4071;DATABASE=AshburtonRisk;Trusted_Connection=yes;"
db = odbc.odbc(constr)

# Config file
listed = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\config\compliance.xlsx', sheet_name='listed')
unlisted = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\config\compliance.xlsx', sheet_name='unlisted')

sql = "SELECT ValuationDate AS ValueDate, InstrumentCode, InstrumentLongName AS 'Instrument Name', BaseEffectiveExposure AS 'All-in Market Value-Val' FROM Investment.vwMaitlandHoldings WHERE ValuationDate = " + " ' " + datetime_obj_end + "'" + " AND PortfolioCode IN ('95951')"
df = pd.read_sql(sql, db)
df = df[(df['Instrument Name']!='MANAGEMENT FEES ZAR') & (df['Instrument Name']!='VAT ON MANAGEMENT FEES ZAR')]

sql = "SELECT InstrumentCode, IssuerName, InstrumentTypeDescription AS InstrumentType, InterestRate AS Yield, MaturityDate AS 'Inst Maty Dt', ModifiedDuration AS 'Mod Dur', ISIN FROM Investment.MaitlandASISAInstruments WHERE DataDate = " + " ' " + datetime_obj_end + "'" + " AND PortfolioIDCode IN ('95951')"
df_static = pd.read_sql(sql, db)
#df_static['InstrumentCode'] = np.where(df_static['ISIN'].str[:3] == 'ZAM',df_static['ISIN'], df_static['InstrumentCode'])
#df_static = df_static.drop(['ISIN'], axis=1)
df_static = df_static.drop_duplicates()

df = df.merge(df_static, how='left', on=['InstrumentCode'])
df['InstrumentCode'] = df['InstrumentCode'].apply(lambda x: x.replace('CASH','SOUTH AFRICAN RAND I'))

df['IssuerName'] = df['IssuerName'].str.upper()
df['InstrumentCode'] = df['InstrumentCode'].str.upper()
df = df[df.InstrumentCode.str.contains('EXPENSE') == False]
df['%Market Value'] = df['All-in Market Value-Val']/df['All-in Market Value-Val'].sum()
df['Time to Maturity (days)'] = (pd.to_datetime(df['Inst Maty Dt']) - pd.to_datetime(df['ValueDate'])).dt.days
df['Time to Maturity (days)'] = df['Time to Maturity (days)'].fillna(0)
df['Weighted Duration'] = df['%Market Value']* df['Mod Dur']
df = df.merge(listed, how='left', on=['InstrumentCode'])
# single_issuer_exposure
single_issuer_exposure = df.groupby(['Issuer']).sum()['%Market Value'].reset_index()
single_issuer_exposure.rename(columns={'%Market Value':'Single Issuer Exposure'}, inplace=True)
df = df.merge(single_issuer_exposure, how='left', on=['Issuer'])
df['duplicated_issuer'] = df['Single Issuer Exposure'].duplicated()
df['Single Issuer Exposure'] = np.where(df['duplicated_issuer']==True,0,df['Single Issuer Exposure'])
# single_issuer_exposure
single_industry_exposure = df.groupby(['Industry']).sum()['%Market Value'].reset_index()
single_industry_exposure.rename(columns={'%Market Value':'Single Industry Exposure'}, inplace=True)
df = df.merge(single_industry_exposure, how='left', on=['Industry'])
df['duplicated_industry'] = df['Single Industry Exposure'].duplicated()
df['Single Industry Exposure'] = np.where(df['duplicated_industry']==True,0,df['Single Industry Exposure'])

df.drop(['duplicated_issuer','duplicated_industry'], axis=1, inplace=True)
df = df[['ValueDate','InstrumentCode','Instrument Name','InstrumentType','%Market Value','All-in Market Value-Val','Issuer','Yield','Inst Maty Dt','Mod Dur','Time to Maturity (days)','Single Issuer Exposure','Industry','Single Industry Exposure','Weighted Duration','Issuer Type','Guarantee','National Rating','Global Rating','Source','PD','LGD','Collateralization','Classification','IssuerName','Status']]
df = df.sort_values(by=['Issuer','InstrumentType'], ascending=False)

unclasified = df[df['National Rating'].isnull()]
unclasified = unclasified[['ValueDate','InstrumentCode','InstrumentType','Inst Maty Dt','IssuerName']]
unclasified_df = unclasified_df.append(unclasified)

df.to_excel(writer,'AIG SA CREDIT', index=False)

#*********************************************************************************************************************************************************


# 'AIG LIFE CREDIT'

constr = "DRIVER={SQL Server Native Client 11.0};SERVER=ash-prdkblddbao,4071;DATABASE=AshburtonRisk;Trusted_Connection=yes;"
db = odbc.odbc(constr)

# Config file
listed = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\config\compliance.xlsx', sheet_name='listed')
unlisted = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\config\compliance.xlsx', sheet_name='unlisted')

sql = "SELECT ValuationDate AS ValueDate, InstrumentCode, InstrumentLongName AS 'Instrument Name', BaseEffectiveExposure AS 'All-in Market Value-Val' FROM Investment.vwMaitlandHoldings WHERE ValuationDate = " + " ' " + datetime_obj_end + "'" + " AND PortfolioCode IN ('95952')"
df = pd.read_sql(sql, db)
df = df[(df['Instrument Name']!='MANAGEMENT FEES ZAR') & (df['Instrument Name']!='VAT ON MANAGEMENT FEES ZAR')]

sql = "SELECT InstrumentCode, IssuerName, InstrumentTypeDescription AS InstrumentType, InterestRate AS Yield, MaturityDate AS 'Inst Maty Dt', ModifiedDuration AS 'Mod Dur', ISIN FROM Investment.MaitlandASISAInstruments WHERE DataDate = " + " ' " + datetime_obj_end + "'" + " AND PortfolioIDCode IN ('95952')"
df_static = pd.read_sql(sql, db)
#df_static['InstrumentCode'] = np.where(df_static['ISIN'].str[:3] == 'ZAM',df_static['ISIN'], df_static['InstrumentCode'])
#df_static = df_static.drop(['ISIN'], axis=1)
df_static = df_static.drop_duplicates()

df = df.merge(df_static, how='left', on=['InstrumentCode'])
df['InstrumentCode'] = df['InstrumentCode'].apply(lambda x: x.replace('CASH','SOUTH AFRICAN RAND I'))

df['IssuerName'] = df['IssuerName'].str.upper()
df['InstrumentCode'] = df['InstrumentCode'].str.upper()
df = df[df.InstrumentCode.str.contains('EXPENSE') == False]
df['%Market Value'] = df['All-in Market Value-Val']/df['All-in Market Value-Val'].sum()
df['Time to Maturity (days)'] = (pd.to_datetime(df['Inst Maty Dt']) - pd.to_datetime(df['ValueDate'])).dt.days
df['Time to Maturity (days)'] = df['Time to Maturity (days)'].fillna(0)
df['Weighted Duration'] = df['%Market Value']* df['Mod Dur']
df = df.merge(listed, how='left', on=['InstrumentCode'])
# single_issuer_exposure
single_issuer_exposure = df.groupby(['Issuer']).sum()['%Market Value'].reset_index()
single_issuer_exposure.rename(columns={'%Market Value':'Single Issuer Exposure'}, inplace=True)
df = df.merge(single_issuer_exposure, how='left', on=['Issuer'])
df['duplicated_issuer'] = df['Single Issuer Exposure'].duplicated()
df['Single Issuer Exposure'] = np.where(df['duplicated_issuer']==True,0,df['Single Issuer Exposure'])
# single_issuer_exposure
single_industry_exposure = df.groupby(['Industry']).sum()['%Market Value'].reset_index()
single_industry_exposure.rename(columns={'%Market Value':'Single Industry Exposure'}, inplace=True)
df = df.merge(single_industry_exposure, how='left', on=['Industry'])
df['duplicated_industry'] = df['Single Industry Exposure'].duplicated()
df['Single Industry Exposure'] = np.where(df['duplicated_industry']==True,0,df['Single Industry Exposure'])

df.drop(['duplicated_issuer','duplicated_industry'], axis=1, inplace=True)
df = df[['ValueDate','InstrumentCode','Instrument Name','InstrumentType','%Market Value','All-in Market Value-Val','Issuer','Yield','Inst Maty Dt','Mod Dur','Time to Maturity (days)','Single Issuer Exposure','Industry','Single Industry Exposure','Weighted Duration','Issuer Type','Guarantee','National Rating','Global Rating','Source','PD','LGD','Collateralization','Classification','IssuerName','Status']]
df = df.sort_values(by=['Issuer','InstrumentType'], ascending=False)

unclasified = df[df['National Rating'].isnull()]
unclasified = unclasified[['ValueDate','InstrumentCode','InstrumentType','Inst Maty Dt','IssuerName']]
unclasified_df = unclasified_df.append(unclasified)

df.to_excel(writer,'AIG LIFE CREDIT', index=False)

#*********************************************************************************************************************************************************


# 'Momentum Ability'

constr = "DRIVER={SQL Server Native Client 11.0};SERVER=ash-prdkblddbao,4071;DATABASE=AshburtonRisk;Trusted_Connection=yes;"
db = odbc.odbc(constr)

# Config file
listed = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\config\compliance.xlsx', sheet_name='listed')
unlisted = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\config\compliance.xlsx', sheet_name='unlisted')

sql = "SELECT ValuationDate AS ValueDate, InstrumentCode, InstrumentLongName AS 'Instrument Name', BaseEffectiveExposure AS 'All-in Market Value-Val' FROM Investment.vwMaitlandHoldings WHERE ValuationDate = " + " ' " + datetime_obj_end + "'" + " AND PortfolioCode IN ('95930')"
df = pd.read_sql(sql, db)
df = df[(df['Instrument Name']!='MANAGEMENT FEES ZAR') & (df['Instrument Name']!='VAT ON MANAGEMENT FEES ZAR')]

sql = "SELECT InstrumentCode, IssuerName, InstrumentTypeDescription AS InstrumentType, InterestRate AS Yield, MaturityDate AS 'Inst Maty Dt', ModifiedDuration AS 'Mod Dur' FROM Investment.MaitlandASISAInstruments WHERE DataDate = " + " ' " + datetime_obj_end + "'" + " AND PortfolioIDCode IN ('95930')"
df_static = pd.read_sql(sql, db)
df_static = df_static.drop_duplicates()

df = df.merge(df_static, how='left', on=['InstrumentCode'])
df['InstrumentCode'] = df['InstrumentCode'].apply(lambda x: x.replace('CASH','SOUTH AFRICAN RAND I'))

df['IssuerName'] = df['IssuerName'].str.upper()
df['InstrumentCode'] = df['InstrumentCode'].str.upper()
df = df[df.InstrumentCode.str.contains('EXPENSE') == False]
df['%Market Value'] = df['All-in Market Value-Val']/df['All-in Market Value-Val'].sum()
df['Time to Maturity (days)'] = (pd.to_datetime(df['Inst Maty Dt']) - pd.to_datetime(df['ValueDate'])).dt.days
df['Time to Maturity (days)'] = df['Time to Maturity (days)'].fillna(0)
df['Weighted Duration'] = df['%Market Value']* df['Mod Dur']
df = df.merge(listed, how='left', on=['InstrumentCode'])
# single_issuer_exposure
single_issuer_exposure = df.groupby(['Issuer']).sum()['%Market Value'].reset_index()
single_issuer_exposure.rename(columns={'%Market Value':'Single Issuer Exposure'}, inplace=True)
df = df.merge(single_issuer_exposure, how='left', on=['Issuer'])
df['duplicated_issuer'] = df['Single Issuer Exposure'].duplicated()
df['Single Issuer Exposure'] = np.where(df['duplicated_issuer']==True,0,df['Single Issuer Exposure'])
# single_issuer_exposure
single_industry_exposure = df.groupby(['Industry']).sum()['%Market Value'].reset_index()
single_industry_exposure.rename(columns={'%Market Value':'Single Industry Exposure'}, inplace=True)
df = df.merge(single_industry_exposure, how='left', on=['Industry'])
df['duplicated_industry'] = df['Single Industry Exposure'].duplicated()
df['Single Industry Exposure'] = np.where(df['duplicated_industry']==True,0,df['Single Industry Exposure'])

df.drop(['duplicated_issuer','duplicated_industry'], axis=1, inplace=True)
df = df[['ValueDate','InstrumentCode','Instrument Name','InstrumentType','%Market Value','All-in Market Value-Val','Issuer','Yield','Inst Maty Dt','Mod Dur','Time to Maturity (days)','Single Issuer Exposure','Industry','Single Industry Exposure','Weighted Duration','Issuer Type','Guarantee','National Rating','Global Rating','Source','PD','LGD','Classification','IssuerName','Status']]
df.rename(columns={'Global Rating2':'Global Rating'}, inplace=True)
df = df.sort_values(by=['Issuer','InstrumentType'], ascending=False)

unclasified = df[df['National Rating'].isnull()]
unclasified = unclasified[['ValueDate','InstrumentCode','InstrumentType','Inst Maty Dt','IssuerName']]
unclasified_df = unclasified_df.append(unclasified)

sql = "SELECT ValuationDate AS ValuationDate, PortfolioName, InstrumentCode, InstrumentLongName, HoldingsNominal AS HoldingNominal, BaseEffectiveExposure AS AssetMarketValue FROM Investment.vwMaitlandHoldings WHERE ValuationDate = " + " ' " + datetime_obj_end + "'" + " AND PortfolioCode IN ('95930')"
mom_a_2 = pd.read_sql(sql, db)
mom_a_2 = mom_a_2[mom_a_2.InstrumentCode.str.contains('EXPENSE') == False]

df.to_excel(writer,'Momentum Ability', index=False)
mom_a_2.to_excel(writer,'Momentum Ability_2', index=False)


#************************************************************************************************************************************************************************************

# 'RMBSi'

constr = "DRIVER={SQL Server Native Client 11.0};SERVER=ash-prdkblddbao,4071;DATABASE=AshburtonRisk;Trusted_Connection=yes;"
db = odbc.odbc(constr)

# Config file
listed = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\config\compliance.xlsx', sheet_name='listed')
unlisted = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\config\compliance.xlsx', sheet_name='unlisted')

sql = "SELECT ValuationDate AS ValueDate, InstrumentCode, InstrumentLongName AS 'Instrument Name', BaseEffectiveExposure AS 'All-in Market Value-Val' FROM Investment.vwMaitlandHoldings WHERE ValuationDate = " + " ' " + datetime_obj_end + "'" + " AND PortfolioCode IN ('95936')"
df = pd.read_sql(sql, db)
df = df[(df['Instrument Name']!='MANAGEMENT FEES ZAR') & (df['Instrument Name']!='VAT ON MANAGEMENT FEES ZAR')]

sql = "SELECT InstrumentCode, IssuerName, InstrumentTypeDescription AS InstrumentType, InterestRate AS Yield, MaturityDate AS 'Inst Maty Dt', ModifiedDuration AS 'Mod Dur' FROM Investment.MaitlandASISAInstruments WHERE DataDate = " + " ' " + datetime_obj_end + "'" + " AND PortfolioIDCode IN ('95936')"
df_static = pd.read_sql(sql, db)
df_static = df_static.drop_duplicates()

df = df.merge(df_static, how='left', on=['InstrumentCode'])
df['InstrumentCode'] = df['InstrumentCode'].apply(lambda x: x.replace('CASH','SOUTH AFRICAN RAND I'))

df['IssuerName'] = df['IssuerName'].str.upper()
df['InstrumentCode'] = df['InstrumentCode'].str.upper()
df = df[df.InstrumentCode.str.contains('EXPENSE') == False]
df['%Market Value'] = df['All-in Market Value-Val']/df['All-in Market Value-Val'].sum()
df['Time to Maturity (days)'] = (pd.to_datetime(df['Inst Maty Dt']) - pd.to_datetime(df['ValueDate'])).dt.days
df['Time to Maturity (days)'] = df['Time to Maturity (days)'].fillna(0)
df['Weighted Duration'] = df['%Market Value']* df['Mod Dur']
df = df.merge(listed, how='left', on=['InstrumentCode'])
# single_issuer_exposure
single_issuer_exposure = df.groupby(['Issuer']).sum()['%Market Value'].reset_index()
single_issuer_exposure.rename(columns={'%Market Value':'Single Issuer Exposure'}, inplace=True)
df = df.merge(single_issuer_exposure, how='left', on=['Issuer'])
df['duplicated_issuer'] = df['Single Issuer Exposure'].duplicated()
df['Single Issuer Exposure'] = np.where(df['duplicated_issuer']==True,0,df['Single Issuer Exposure'])
# single_issuer_exposure
single_industry_exposure = df.groupby(['Industry']).sum()['%Market Value'].reset_index()
single_industry_exposure.rename(columns={'%Market Value':'Single Industry Exposure'}, inplace=True)
df = df.merge(single_industry_exposure, how='left', on=['Industry'])
df['duplicated_industry'] = df['Single Industry Exposure'].duplicated()
df['Single Industry Exposure'] = np.where(df['duplicated_industry']==True,0,df['Single Industry Exposure'])

df.drop(['duplicated_issuer','duplicated_industry'], axis=1, inplace=True)
df = df[['ValueDate','InstrumentCode','Instrument Name','InstrumentType','%Market Value','All-in Market Value-Val','Issuer','Yield','Inst Maty Dt','Mod Dur','Time to Maturity (days)','Single Issuer Exposure','Industry','Single Industry Exposure','Weighted Duration','Issuer Type','Guarantee','National Rating','Global Rating','Source','PD','LGD','Classification','IssuerName','Status']]
df.rename(columns={'Global Rating2':'Global Rating'}, inplace=True)
df = df.sort_values(by=['Issuer','InstrumentType'], ascending=False)

unclasified = df[df['National Rating'].isnull()]
unclasified = unclasified[['ValueDate','InstrumentCode','InstrumentType','Inst Maty Dt','IssuerName']]
unclasified_df = unclasified_df.append(unclasified)

sql = "SELECT ValuationDate AS ValuationDate, PortfolioName, InstrumentCode, InstrumentLongName, HoldingsNominal AS HoldingNominal, BaseEffectiveExposure AS AssetMarketValue FROM Investment.vwMaitlandHoldings WHERE ValuationDate = " + " ' " + datetime_obj_end + "'" + " AND PortfolioCode IN ('95936')"
rmbsi_2 = pd.read_sql(sql, db)
rmbsi_2 = rmbsi_2[rmbsi_2.InstrumentCode.str.contains('EXPENSE') == False]

df.to_excel(writer,'RMBSi', index=False)
rmbsi_2.to_excel(writer,'RMBSi_2', index=False)


#************************************************************************************************************************************************************************************


# 'MomA Excess Assets'

constr = "DRIVER={SQL Server Native Client 11.0};SERVER=ash-prdkblddbao,4071;DATABASE=AshburtonRisk;Trusted_Connection=yes;"
db = odbc.odbc(constr)

sql = "SELECT ValuationDate AS ValuationDate, PortfolioName, InstrumentCode, InstrumentLongName, HoldingsNominal AS HoldingNominal, BaseEffectiveExposure AS AssetMarketValue FROM Investment.vwMaitlandHoldings WHERE ValuationDate = " + " ' " + datetime_obj_end + "'" + " AND PortfolioCode IN ('95969')"
rmbsi_2 = pd.read_sql(sql, db)
rmbsi_2 = rmbsi_2[rmbsi_2.InstrumentCode.str.contains('EXPENSE') == False]

rmbsi_2.to_excel(writer,'MomA_Excess_Assets_2', index=False)


#************************************************************************************************************************************************************************************



# 'MomAbility Credit'
# AIG
aig_nav = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\reports\compliance\credit_funds\nav_report.xlsx', sheet_name='aig_nav')
aig_nav.rename(columns={'Maturity date':'Maturity Date'}, inplace=True)
aig_nav['Underlying Debt Transaction'] = aig_nav['Underlying Debt Transaction'].str.upper().str.strip()
aig_nav['Tranche'] = aig_nav['Tranche'].str.upper().str.strip()
aig_nav = aig_nav[['Underlying Debt Transaction','Tranche','Secured','Momentum Ability','Industry','Spread','Type','Maturity Date']]
aig_nav['Fund'] = 'Note - AIG2U'
aig_nav['Grade'] = 'Investment Grade'
aig_nav['Deal type'] = 'Loan'
aig_nav.rename(columns={'Momentum Ability': 'Value'}, inplace=True)
aig_nav['Exposure'] = aig_nav['Value']/aig_nav['Value'].sum()
aig_nav = aig_nav[aig_nav['Value'] != 0]
aig_nav['Time to Maturity'] = (pd.to_datetime(aig_nav['Maturity Date']) - pd.to_datetime(datetime_obj_end)).dt.days
aig_nav['Time to Maturity'] = aig_nav['Time to Maturity'].fillna(0)
aig_nav = aig_nav.merge(unlisted, how='left', on=['Underlying Debt Transaction','Tranche'])
aig_nav.rename(columns={'Guarantee': 'Guarantee Type'}, inplace=True)

# single_issuer_exposure
single_issuer_exposure = aig_nav.groupby(['Underlying Debt Transaction']).sum()['Exposure'].reset_index()
single_issuer_exposure.rename(columns={'Exposure':'Single Issuer Exposure'}, inplace=True)
aig_nav = aig_nav.merge(single_issuer_exposure, how='left', on=['Underlying Debt Transaction'])
aig_nav['duplicated_issuer'] = aig_nav['Single Issuer Exposure'].duplicated()
aig_nav['Single Issuer Exposure'] = np.where(aig_nav['duplicated_issuer']==True,0,aig_nav['Single Issuer Exposure'])

aig_nav = aig_nav[['Fund','Underlying Debt Transaction','Tranche','Secured','Exposure','Value','Industry','Deal type','Spread','Type','Maturity Date','Time to Maturity','Single Issuer Exposure','Issuer Type','Guarantee Type','National Rating','Global Rating2','Source','PD','LGD','Grade']]
aig_nav = aig_nav.fillna('')
aig_nav['Fund'].iloc[-1] = ''
aig_nav['Grade'].iloc[-1] = ''

# AHY
ahy_nav = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\reports\compliance\credit_funds\nav_report.xlsx', sheet_name='ahy_nav')
ahy_nav['Underlying Debt Transaction'] = ahy_nav['Underlying Debt Transaction'].str.upper().str.strip()
ahy_nav['Tranche'] = ahy_nav['Tranche'].str.upper().str.strip()
ahy_nav = ahy_nav[['Underlying Debt Transaction','Tranche','Secured','Momentum Ability (95930)','Industry','Spread','Type','Maturity Date']]
ahy_nav['Fund'] = 'Note - AHY2U'
ahy_nav['Grade'] = 'Non-Investment Grade'
ahy_nav['Deal type'] = 'Loan'
ahy_nav.rename(columns={'Momentum Ability (95930)': 'Value'}, inplace=True)
ahy_nav['Exposure'] = ahy_nav['Value']/ahy_nav['Value'].sum()
ahy_nav = ahy_nav[ahy_nav['Value'] != 0]
ahy_nav['Time to Maturity'] = (pd.to_datetime(ahy_nav['Maturity Date']) - pd.to_datetime(datetime_obj_end)).dt.days
ahy_nav['Time to Maturity'] = ahy_nav['Time to Maturity'].fillna(0)
ahy_nav = ahy_nav.merge(unlisted, how='left', on=['Underlying Debt Transaction','Tranche'])
ahy_nav.rename(columns={'Guarantee': 'Guarantee Type'}, inplace=True)

# single_issuer_exposure
single_issuer_exposure = ahy_nav.groupby(['Underlying Debt Transaction']).sum()['Exposure'].reset_index()
single_issuer_exposure.rename(columns={'Exposure':'Single Issuer Exposure'}, inplace=True)
ahy_nav = ahy_nav.merge(single_issuer_exposure, how='left', on=['Underlying Debt Transaction'])
ahy_nav['duplicated_issuer'] = ahy_nav['Single Issuer Exposure'].duplicated()
ahy_nav['Single Issuer Exposure'] = np.where(ahy_nav['duplicated_issuer']==True,0,ahy_nav['Single Issuer Exposure'])

ahy_nav = ahy_nav[['Fund','Underlying Debt Transaction','Tranche','Secured','Exposure','Value','Industry','Deal type','Spread','Type','Maturity Date','Time to Maturity','Single Issuer Exposure','Issuer Type','Guarantee Type','National Rating','Global Rating2','Source','PD','LGD','Grade']]
ahy_nav = ahy_nav.fillna('')
ahy_nav['Fund'].iloc[-1] = ''
ahy_nav['Grade'].iloc[-1] = ''

mom_ability = aig_nav.append(ahy_nav)
mom_ability = mom_ability[['Fund','Underlying Debt Transaction','Tranche','Secured','Exposure','Value','Industry','Deal type','Spread','Type','Maturity Date','Time to Maturity','Single Issuer Exposure','Issuer Type','Guarantee Type','National Rating','Global Rating2','Source','PD','LGD','Grade']]
mom_ability.rename(columns={'Global Rating2':'Global Rating'}, inplace=True)

mom_ability.to_excel(writer,'Momementum Ability Credit', index=False)

#************************************************************************************************************************************************************************************
# 'RMBSi Credit'
# AIG
aig_nav = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\reports\compliance\credit_funds\nav_report.xlsx', sheet_name='aig_nav')
aig_nav.rename(columns={'Maturity date':'Maturity Date'}, inplace=True)
aig_nav['Underlying Debt Transaction'] = aig_nav['Underlying Debt Transaction'].str.upper().str.strip()
aig_nav['Tranche'] = aig_nav['Tranche'].str.upper().str.strip()
aig_nav = aig_nav[['Underlying Debt Transaction','Tranche','Secured','(RMB Si) SPMC005','Industry','Spread','Type','Maturity Date']]
aig_nav['Fund'] = 'Note - AIG2U'
aig_nav['Grade'] = 'Investment Grade'
aig_nav['Deal type'] = 'Loan'
aig_nav.rename(columns={'(RMB Si) SPMC005': 'Value'}, inplace=True)
aig_nav['Exposure'] = aig_nav['Value']/aig_nav['Value'].sum()
aig_nav = aig_nav[aig_nav['Value'] != 0]
aig_nav['Time to Maturity'] = (pd.to_datetime(aig_nav['Maturity Date']) - pd.to_datetime(datetime_obj_end)).dt.days
aig_nav['Time to Maturity'] = aig_nav['Time to Maturity'].fillna(0)
aig_nav = aig_nav.merge(unlisted, how='left', on=['Underlying Debt Transaction','Tranche'])
aig_nav.rename(columns={'Guarantee': 'Guarantee Type'}, inplace=True)

# single_issuer_exposure
single_issuer_exposure = aig_nav.groupby(['Underlying Debt Transaction']).sum()['Exposure'].reset_index()
single_issuer_exposure.rename(columns={'Exposure':'Single Issuer Exposure'}, inplace=True)
aig_nav = aig_nav.merge(single_issuer_exposure, how='left', on=['Underlying Debt Transaction'])
aig_nav['duplicated_issuer'] = aig_nav['Single Issuer Exposure'].duplicated()
aig_nav['Single Issuer Exposure'] = np.where(aig_nav['duplicated_issuer']==True,0,aig_nav['Single Issuer Exposure'])

aig_nav = aig_nav[['Fund','Underlying Debt Transaction','Tranche','Secured','Exposure','Value','Industry','Deal type','Spread','Type','Maturity Date','Time to Maturity','Single Issuer Exposure','Issuer Type','Guarantee Type','National Rating','Global Rating2','Source','PD','LGD','Grade']]
aig_nav = aig_nav.fillna('')
aig_nav['Fund'].iloc[-1] = ''
aig_nav['Grade'].iloc[-1] = ''

# AHY
ahy_nav = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\reports\compliance\credit_funds\nav_report.xlsx', sheet_name='ahy_nav')
ahy_nav['Underlying Debt Transaction'] = ahy_nav['Underlying Debt Transaction'].str.upper().str.strip()
ahy_nav['Tranche'] = ahy_nav['Tranche'].str.upper().str.strip()
ahy_nav = ahy_nav[['Underlying Debt Transaction','Tranche','Secured','Momentum Ability (95930)','Industry','Spread','Type','Maturity Date']]
ahy_nav['Fund'] = 'Note - AHY2U'
ahy_nav['Grade'] = 'Non-Investment Grade'
ahy_nav['Deal type'] = 'Loan'
ahy_nav.rename(columns={'Momentum Ability (95930)': 'Value'}, inplace=True)
ahy_nav['Exposure'] = ahy_nav['Value']/ahy_nav['Value'].sum()
ahy_nav = ahy_nav[ahy_nav['Value'] != 0]
ahy_nav['Time to Maturity'] = (pd.to_datetime(ahy_nav['Maturity Date']) - pd.to_datetime(datetime_obj_end)).dt.days
ahy_nav['Time to Maturity'] = ahy_nav['Time to Maturity'].fillna(0)
ahy_nav = ahy_nav.merge(unlisted, how='left', on=['Underlying Debt Transaction','Tranche'])
ahy_nav.rename(columns={'Guarantee': 'Guarantee Type'}, inplace=True)

# single_issuer_exposure
single_issuer_exposure = ahy_nav.groupby(['Underlying Debt Transaction']).sum()['Exposure'].reset_index()
single_issuer_exposure.rename(columns={'Exposure':'Single Issuer Exposure'}, inplace=True)
ahy_nav = ahy_nav.merge(single_issuer_exposure, how='left', on=['Underlying Debt Transaction'])
ahy_nav['duplicated_issuer'] = ahy_nav['Single Issuer Exposure'].duplicated()
ahy_nav['Single Issuer Exposure'] = np.where(ahy_nav['duplicated_issuer']==True,0,ahy_nav['Single Issuer Exposure'])

ahy_nav = ahy_nav[['Fund','Underlying Debt Transaction','Tranche','Secured','Exposure','Value','Industry','Deal type','Spread','Type','Maturity Date','Time to Maturity','Single Issuer Exposure','Issuer Type','Guarantee Type','National Rating','Global Rating2','Source','PD','LGD','Grade']]
ahy_nav = ahy_nav.fillna('')
ahy_nav['Fund'].iloc[-1] = ''
ahy_nav['Grade'].iloc[-1] = ''

RMBSi = aig_nav.append(ahy_nav)
RMBSi = RMBSi[['Fund','Underlying Debt Transaction','Tranche','Secured','Exposure','Value','Industry','Deal type','Spread','Type','Maturity Date','Time to Maturity','Single Issuer Exposure','Issuer Type','Guarantee Type','National Rating','Global Rating2','Source','PD','LGD','Grade']]
RMBSi.rename(columns={'Global Rating2':'Global Rating'}, inplace=True)

RMBSi.to_excel(writer,'RMBSi Credit', index=False)

#************************************************************************************************************************************************************************************
# Unclassified_listed
unclasified_df = unclasified_df.drop_duplicates()
unclasified_df.to_csv(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\reports\compliance\unclassified\unclasified_listed_' + datetime_obj_end + '.csv', index=False)

# # Unclassified_unlisted
# unclasified_unlisted_df = RMBSi[RMBSi['National Rating'].isnull()]
# unclasified_unlisted_df = unclasified_unlisted_df[['Fund','Underlying Debt Transaction','Tranche']]
# unclasified_unlisted_df.to_csv(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\reports\compliance\input\unclasified_unlisted_' + datetime_obj_end + '.csv', index=False)

#************************************************************************************************************************************************************************************
# Export data
writer.save()

#************************************************************************************************************************************************************************************




