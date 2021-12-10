import pandas as pd
import odbc
import numpy as np
import datetime
from my_functions import custom_dates as cd

# date_str_end = input('Enter end date (Format dd/mm/yyyy):')
# format_str = '%d/%m/%Y' # The format
# datetime_obj_end = str(datetime.datetime.strptime(date_str_end, format_str).date())

datetime_obj_end = cd.t_1

writer = pd.ExcelWriter(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\reports\compliance\prelim\prelim_' + datetime_obj_end + '.xlsx')

#************************************************************************************************************************************************************************************
# 'FNB Life Shareholder'

# Config file
df = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\reports\compliance\holdings\combined\holdings_' + datetime_obj_end + '.xlsx', sheet_name='FNB Life')
x = df[df['Classification']==1]['%Market Value'].sum()
df_dict = pd.DataFrame({'Description':'1. Instruments issued or guaranteed by the South African Government','Limits':[1],'Exposure': [x],'Compliance':[np.where(x>1,'No','Yes')]})

x = df[df['Classification']==2]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'2. Bank deposits, Notes, Bills, NCDs or other securities issues endorsed by banks','Limits':[1],'Exposure': [x],'Compliance':[np.where(x>1,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[df['Classification']==3]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'3. Bank issued conduit paper (listed)','Limits':[0.15],'Exposure': [x],'Compliance':[np.where(x>0.15,'No','Yes')]})
df_dict = df_dict.append(df_2)

df[df['Classification']==4]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'4. Direct look through notes','Limits':[0.15],'Exposure': [x], 'Compliance':[np.where(x>0.15,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[df['Classification']==5]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'5. Commercial paper','Limits':[1],'Exposure': [x], 'Compliance':[np.where(x>1,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[df['Classification']==6]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'6. Listed bonds','Limits':[1],'Exposure': [x], 'Compliance':[np.where(x>1,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[df['Classification']==7]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'7. Repurchase agreements','Limits':[0],'Exposure': [x], 'Compliance':[np.where(x>0,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[df['Classification']==8]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'8. Interest rate derivatives for hedging purposes only','Limits':[0.25],'Exposure': [x], 'Compliance':[np.where(x>0.25,'No','Yes')]})
df_dict = df_dict.append(df_2)

df_2 = pd.DataFrame({'Description':[''],'Limits':[''],'Exposure':[''], 'Compliance':['']})
df_dict = df_dict.append(df_2)

x = df[df['Issuer']=='REPUBLIC OF SOUTH AFRICA']['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'RSA Government','Limits':[1],'Exposure': [x], 'Compliance':[np.where(x>1,'No','Yes')]})
df_dict = df_dict.append(df_2)

df_2 = pd.DataFrame({'Description':[''],'Limits':[''],'Exposure':[''], 'Compliance':['']})
df_dict = df_dict.append(df_2)

x = df[((df['Industry']=='SOE') | (df['Industry']=='Banks')) & (df['Guarantee']=='Government Guaranteed') & (df['Issuer']!='RMB') & (df['Issuer']!='ABSA BANK LIMITED')
& (df['Issuer']!='NEDBANK GROUP') & (df['Issuer']!='NEDBANK') & (df['Issuer']!='STANDARD BANK SOUTH AFRICA')]['Single Issuer Exposure'].max()
df_2 = pd.DataFrame({'Description':'Any Government guaranteed issuer','Limits':[0.15],'Exposure': [x], 'Compliance':[np.where(x>0.15,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[((df['Industry']=='SOE') | (df['Industry']=='Banks')) & (df['Issuer']!='REPUBLIC OF SOUTH AFRICA') & (df['Guarantee']!='Government Guaranteed') & (df['Issuer']!='RMB') & 
(df['Issuer']!='ABSA BANK LIMITED') & (df['Issuer']!='NEDBANK GROUP') & (df['Issuer']!='NEDBANK') & (df['Issuer']!='STANDARD BANK SOUTH AFRICA') & ((df['National Rating']=='AAA') | (df['National Rating']=='AA+') | (df['National Rating']=='AA') | (df['National Rating']=='AA-'))]['Single Issuer Exposure'].max()
df_2 = pd.DataFrame({'Description':'Any AAA, AA+, AA or AA-','Limits':[0.1],'Exposure': [x], 'Compliance':[np.where(x>0.1,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[((df['Industry']=='SOE') | (df['Industry']=='Banks')) & (df['Issuer']!='REPUBLIC OF SOUTH AFRICA') & (df['Guarantee']!='Government Guaranteed') & (df['Issuer']!='RMB') & 
(df['Issuer']!='ABSA BANK LIMITED') & (df['Issuer']!='NEDBANK GROUP') & (df['Issuer']!='NEDBANK') & (df['Issuer']!='STANDARD BANK SOUTH AFRICA') & ((df['National Rating']=='A+') | (df['National Rating']=='A') | (df['National Rating']=='A-'))]['Single Issuer Exposure'].max()
df_2 = pd.DataFrame({'Description':'Any A+, A or A-','Limits':[0.07],'Exposure': [x], 'Compliance':[np.where(x>0.07,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[((df['Industry']=='SOE') | (df['Industry']=='Banks')) & (df['Issuer']!='REPUBLIC OF SOUTH AFRICA') & (df['Guarantee']!='Government Guaranteed') & (df['Issuer']!='RMB') & 
(df['Issuer']!='ABSA BANK LIMITED') & (df['Issuer']!='NEDBANK GROUP') & (df['Issuer']!='NEDBANK') & (df['Issuer']!='STANDARD BANK SOUTH AFRICA') & ((df['National Rating']=='BBB+') | (df['National Rating']=='BBB') | (df['National Rating']=='BBB-'))]['Single Issuer Exposure'].max()
df_2 = pd.DataFrame({'Description':'Any BBB+, BBB and BBB-','Limits':[0.03],'Exposure': [x], 'Compliance':[np.where(x>0.03,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[((df['Industry']=='SOE') | (df['Industry']=='Banks')) & (df['Issuer']!='REPUBLIC OF SOUTH AFRICA') & (df['Guarantee']!='Government Guaranteed') & (df['Issuer']!='RMB') & 
(df['Issuer']!='ABSA BANK LIMITED') & (df['Issuer']!='NEDBANK GROUP') & (df['Issuer']!='NEDBANK') & (df['Issuer']!='STANDARD BANK SOUTH AFRICA') & (df['National Rating']!='AAA') & (df['National Rating']!='AA+') & (df['National Rating']!='AA') & (df['National Rating']!='AA-') & (df['National Rating']!='A+') 
& (df['National Rating']!='A') & (df['National Rating']!='A-') & (df['National Rating']!='BBB+') & (df['National Rating']!='BBB') & (df['National Rating']!='BBB-')]['Single Issuer Exposure'].max()
df_2 = pd.DataFrame({'Description':'Any BB+ or lower*','Limits':[0],'Exposure': [x], 'Compliance':[np.where(x>0,'No','Yes')]})
df_dict = df_dict.append(df_2)

df_2 = pd.DataFrame({'Description':[''],'Limits':[''],'Exposure':[''], 'Compliance':['']})
df_dict = df_dict.append(df_2)

x = df[(df['Issuer Type']=='Corporate') & (df['Guarantee']=='Government Guaranteed')]['Single Issuer Exposure'].max()
df_2 = pd.DataFrame({'Description':'Any Government guaranteed issuer','Limits':[0.15],'Exposure': [x], 'Compliance':[np.where(x>0.15,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[(df['Issuer Type']=='Corporate') & (df['Issuer']!='REPUBLIC OF SOUTH AFRICA') & (df['Guarantee']!='Government Guaranteed') & ((df['National Rating']=='AAA') | (df['National Rating']=='AA+') | (df['National Rating']=='AA') | (df['National Rating']=='AA-'))]['Single Issuer Exposure'].max()
df_2 = pd.DataFrame({'Description':'Any AAA, AA+, AA or AA-','Limits':[0.08],'Exposure': [x], 'Compliance':[np.where(x>0.08,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[(df['Issuer Type']=='Corporate') & (df['Issuer']!='REPUBLIC OF SOUTH AFRICA') & (df['Guarantee']!='Government Guaranteed') & ((df['National Rating']=='A+') | (df['National Rating']=='A') | (df['National Rating']=='A-'))]['Single Issuer Exposure'].max()
df_2 = pd.DataFrame({'Description':'Any A+, A or A-','Limits':[0.05],'Exposure': [x], 'Compliance':[np.where(x>0.05,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[(df['Issuer Type']=='Corporate') & (df['Issuer']!='REPUBLIC OF SOUTH AFRICA') & (df['Guarantee']!='Government Guaranteed') & ((df['National Rating']=='BBB+') | (df['National Rating']=='BBB') | (df['National Rating']=='BBB-'))]['Single Issuer Exposure'].max()
df_2 = pd.DataFrame({'Description':'Any BBB+, BBB and BBB-','Limits':[0.03],'Exposure': [x], 'Compliance':[np.where(x>0.03,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[(df['Issuer Type']=='Corporate') & (df['Issuer']!='REPUBLIC OF SOUTH AFRICA') & (df['Guarantee']!='Government Guaranteed') & (df['National Rating']!='AAA') & (df['National Rating']!='AA+') & (df['National Rating']!='AA') & (df['National Rating']!='AA-') & (df['National Rating']!='A+') 
& (df['National Rating']!='A') & (df['National Rating']!='A-') & (df['National Rating']!='BBB+') & (df['National Rating']!='BBB') & (df['National Rating']!='BBB-')]['Single Issuer Exposure'].max()
df_2 = pd.DataFrame({'Description':'Any BB+ or lower*','Limits':[0],'Exposure': [x], 'Compliance':[np.where(x>0,'No','Yes')]})
df_dict = df_dict.append(df_2)

df_2 = pd.DataFrame({'Description':[''],'Limits':[''],'Exposure':[''], 'Compliance':['']})
df_dict = df_dict.append(df_2)

x = df[((df['National Rating']=='AAA') | (df['National Rating']=='AA+') | (df['National Rating']=='AA') | (df['National Rating']=='AA-'))]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'RSA Government, Government guaranteed, AAA or AA-','Limits':[1],'Exposure': [x], 'Compliance':[np.where(x>1,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[((df['National Rating']=='A+') | (df['National Rating']=='A') | (df['National Rating']=='A-'))]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'A+, A, A-','Limits':[0.5],'Exposure': [x], 'Compliance':[np.where(x>0.5,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[((df['National Rating']=='BBB+') | (df['National Rating']=='BBB') | (df['National Rating']=='BBB-'))]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'BBB+, BBB and BBB-','Limits':[0.1],'Exposure': [x], 'Compliance':[np.where(x>0.1,'No','Yes')]})
df_dict = df_dict.append(df_2)

df_2 = pd.DataFrame({'Description':[''],'Limits':[''],'Exposure':[''], 'Compliance':['']})
df_dict = df_dict.append(df_2)

x = df[((df['Issuer']=='RMB') | (df['Issuer']=='ABSA BANK LIMITED') | (df['Issuer']=='NEDBANK GROUP') | (df['Issuer']=='NEDBANK') | (df['Issuer']=='STANDARD BANK SOUTH AFRICA'))]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'Big Four SA Bank Combined','Limits':[0.75],'Exposure': [x], 'Compliance':[np.where(x>0.75,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[((df['Issuer']=='INVESTEC BANK LTD') | (df['Issuer']=='CAPITEC'))]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'Investec Bank and Capitec Bank combined exposure','Limits':[0.15],'Exposure': [x], 'Compliance':[np.where(x>0.15,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[((df['Issuer']=='BNP PARIBAS') | (df['Issuer']=='HSBC'))]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'Non-SA owned banks with SA branch combined exposure','Limits':[0.15],'Exposure': [x], 'Compliance':[np.where(x>0.15,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[(df['Industry']=='Real Estate')]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'Real estate and property','Limits':[0.2],'Exposure': [x], 'Compliance':[np.where(x>0.2,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[(df['Industry']!='Government') & (df['Industry']!='Banks')]['Single Industry Exposure'].max()
df_2 = pd.DataFrame({'Description':'Single Industry Exposure','Limits':[0.15],'Exposure': [x], 'Compliance':[np.where(x>0.15,'No','Yes')]})
df_dict = df_dict.append(df_2)

df_2 = pd.DataFrame({'Description':[''],'Limits':[''],'Exposure':[''], 'Compliance':['']})
df_dict = df_dict.append(df_2)

x = df[(df['Issuer']=='ABSA BANK LIMITED')]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'ABSA/Barclays','Limits':[0.2],'Exposure': [x], 'Compliance':[np.where(x>0.2,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[((df['Issuer']=='NEDBANK GROUP') | (df['Issuer']=='NEDBANK'))]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'Nedbank','Limits':[0.2],'Exposure': [x], 'Compliance':[np.where(x>0.2,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[(df['Issuer']=='STANDARD BANK SOUTH AFRICA')]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'Standard Bank','Limits':[0.2],'Exposure': [x], 'Compliance':[np.where(x>0.2,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[(df['Issuer']=='RMB')]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'FirstRand','Limits':[0.15],'Exposure': [x], 'Compliance':[np.where(x>0.15,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = 0
df_2 = pd.DataFrame({'Description':'Tier II Subordinated Debt (Standard Bank, Nedbank, ABSA Bank/Barclays)','Limits':[0],'Exposure': [x], 'Compliance':[np.where(x>0,'No','Yes')]})
df_dict = df_dict.append(df_2)

df_2 = pd.DataFrame({'Description':[''],'Limits':[''],'Exposure':[''], 'Compliance':['']})
df_dict = df_dict.append(df_2)

x = df[(df['Classification']==3)]['Single Issuer Exposure'].max()
df_2 = pd.DataFrame({'Description':'Single Conduit','Limits':[0.05],'Exposure': [x], 'Compliance':[np.where(x>0.05,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df['Weighted Duration'].sum()
df_2 = pd.DataFrame({'Description':'Weighted Average Modified Duration','Limits':'1 year','Exposure': [x], 'Compliance':[np.where(x>1,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = (df['Time to Maturity (days)']/365).max()
df_2 = pd.DataFrame({'Description':'Term to Maturity of a Single Instrument','Limits':'12 years','Exposure': [x], 'Compliance':[np.where(x>12,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[(df['Time to Maturity (days)']<=365)]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'Term to Maturity less than one year','Limits':'Minimum 65%','Exposure': [x], 'Compliance':[np.where(x<0.65,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = 1
df_2 = pd.DataFrame({'Description':'South African Rand','Limits':[1],'Exposure':[x], 'Compliance':[np.where(x>1,'No','Yes')]})
df_dict = df_dict.append(df_2)

df_dict = df_dict.fillna(0)
df_dict.to_excel(writer,'FNB Life Shareholder', index=False)


#************************************************************************************************************************************************************************************
# 'FNB FLI LT Cap'

# Config file
df = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\reports\compliance\holdings\combined\holdings_' + datetime_obj_end + '.xlsx', sheet_name='FNB FLI LT Cap')
x = df[df['Classification']==1]['%Market Value'].sum()
df_dict = pd.DataFrame({'Description':'1. Instruments issued or guaranteed by the South African Government','Limits':[1],'Exposure': [x],'Compliance':[np.where(x>1,'No','Yes')]})

x = df[df['Classification']==2]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'2. Bank deposits, Notes, Bills, NCDs or other securities issues endorsed by banks','Limits':[1],'Exposure': [x],'Compliance':[np.where(x>1,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[df['Classification']==3]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'3. Bank issued conduit paper (listed)','Limits':[0.15],'Exposure': [x],'Compliance':[np.where(x>0.15,'No','Yes')]})
df_dict = df_dict.append(df_2)

df[df['Classification']==4]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'4. Direct look through notes','Limits':[0.15],'Exposure': [x], 'Compliance':[np.where(x>0.15,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[df['Classification']==5]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'5. Commercial paper','Limits':[1],'Exposure': [x], 'Compliance':[np.where(x>1,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[df['Classification']==6]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'6. Listed bonds','Limits':[1],'Exposure': [x], 'Compliance':[np.where(x>1,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[df['Classification']==7]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'7. Repurchase agreements','Limits':[0],'Exposure': [x], 'Compliance':[np.where(x>0,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[df['Classification']==8]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'8. Interest rate derivatives for hedging purposes only','Limits':[0.25],'Exposure': [x], 'Compliance':[np.where(x>0.25,'No','Yes')]})
df_dict = df_dict.append(df_2)

df_2 = pd.DataFrame({'Description':[''],'Limits':[''],'Exposure':[''], 'Compliance':['']})
df_dict = df_dict.append(df_2)

x = df[df['Issuer']=='REPUBLIC OF SOUTH AFRICA']['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'RSA Government','Limits':[1],'Exposure': [x], 'Compliance':[np.where(x>1,'No','Yes')]})
df_dict = df_dict.append(df_2)

df_2 = pd.DataFrame({'Description':[''],'Limits':[''],'Exposure':[''], 'Compliance':['']})
df_dict = df_dict.append(df_2)

x = df[((df['Industry']=='SOE') | (df['Industry']=='Banks')) & (df['Guarantee']=='Government Guaranteed') & (df['Issuer']!='RMB') & (df['Issuer']!='ABSA BANK LIMITED')
& (df['Issuer']!='NEDBANK GROUP') & (df['Issuer']!='NEDBANK') & (df['Issuer']!='STANDARD BANK SOUTH AFRICA')]['Single Issuer Exposure'].max()
df_2 = pd.DataFrame({'Description':'Any Government guaranteed issuer','Limits':[0.15],'Exposure': [x], 'Compliance':[np.where(x>0.15,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[((df['Industry']=='SOE') | (df['Industry']=='Banks')) & (df['Issuer']!='REPUBLIC OF SOUTH AFRICA') & (df['Guarantee']!='Government Guaranteed') & (df['Issuer']!='RMB') & 
(df['Issuer']!='ABSA BANK LIMITED') & (df['Issuer']!='NEDBANK GROUP') & (df['Issuer']!='NEDBANK') & (df['Issuer']!='STANDARD BANK SOUTH AFRICA') & ((df['National Rating']=='AAA') | (df['National Rating']=='AA+') | (df['National Rating']=='AA') | (df['National Rating']=='AA-'))]['Single Issuer Exposure'].max()
df_2 = pd.DataFrame({'Description':'Any AAA, AA+, AA or AA-','Limits':[0.1],'Exposure': [x], 'Compliance':[np.where(x>0.1,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[((df['Industry']=='SOE') | (df['Industry']=='Banks')) & (df['Issuer']!='REPUBLIC OF SOUTH AFRICA') & (df['Guarantee']!='Government Guaranteed') & (df['Issuer']!='RMB') & 
(df['Issuer']!='ABSA BANK LIMITED') & (df['Issuer']!='NEDBANK GROUP') & (df['Issuer']!='NEDBANK') & (df['Issuer']!='STANDARD BANK SOUTH AFRICA') & ((df['National Rating']=='A+') | (df['National Rating']=='A') | (df['National Rating']=='A-'))]['Single Issuer Exposure'].max()
df_2 = pd.DataFrame({'Description':'Any A+, A or A-','Limits':[0.07],'Exposure': [x], 'Compliance':[np.where(x>0.07,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[((df['Industry']=='SOE') | (df['Industry']=='Banks')) & (df['Issuer']!='REPUBLIC OF SOUTH AFRICA') & (df['Guarantee']!='Government Guaranteed') & (df['Issuer']!='RMB') & 
(df['Issuer']!='ABSA BANK LIMITED') & (df['Issuer']!='NEDBANK GROUP') & (df['Issuer']!='NEDBANK') & (df['Issuer']!='STANDARD BANK SOUTH AFRICA') & ((df['National Rating']=='BBB+') | (df['National Rating']=='BBB') | (df['National Rating']=='BBB-'))]['Single Issuer Exposure'].max()
df_2 = pd.DataFrame({'Description':'Any BBB+, BBB and BBB-','Limits':[0.03],'Exposure': [x], 'Compliance':[np.where(x>0.03,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[((df['Industry']=='SOE') | (df['Industry']=='Banks')) & (df['Issuer']!='REPUBLIC OF SOUTH AFRICA') & (df['Guarantee']!='Government Guaranteed') & (df['Issuer']!='RMB') & 
(df['Issuer']!='ABSA BANK LIMITED') & (df['Issuer']!='NEDBANK GROUP') & (df['Issuer']!='NEDBANK') & (df['Issuer']!='STANDARD BANK SOUTH AFRICA') & (df['National Rating']!='AAA') & (df['National Rating']!='AA+') & (df['National Rating']!='AA') & (df['National Rating']!='AA-') & (df['National Rating']!='A+') 
& (df['National Rating']!='A') & (df['National Rating']!='A-') & (df['National Rating']!='BBB+') & (df['National Rating']!='BBB') & (df['National Rating']!='BBB-')]['Single Issuer Exposure'].max()
df_2 = pd.DataFrame({'Description':'Any BB+ or lower*','Limits':[0],'Exposure': [x], 'Compliance':[np.where(x>0,'No','Yes')]})
df_dict = df_dict.append(df_2)

df_2 = pd.DataFrame({'Description':[''],'Limits':[''],'Exposure':[''], 'Compliance':['']})
df_dict = df_dict.append(df_2)

x = df[(df['Issuer Type']=='Corporate') & (df['Guarantee']=='Government Guaranteed')]['Single Issuer Exposure'].max()
df_2 = pd.DataFrame({'Description':'Any Government guaranteed issuer','Limits':[0.15],'Exposure': [x], 'Compliance':[np.where(x>0.15,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[(df['Issuer Type']=='Corporate') & (df['Issuer']!='REPUBLIC OF SOUTH AFRICA') & (df['Guarantee']!='Government Guaranteed') & ((df['National Rating']=='AAA') | (df['National Rating']=='AA+') | (df['National Rating']=='AA') | (df['National Rating']=='AA-'))]['Single Issuer Exposure'].max()
df_2 = pd.DataFrame({'Description':'Any AAA, AA+, AA or AA-','Limits':[0.08],'Exposure': [x], 'Compliance':[np.where(x>0.08,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[(df['Issuer Type']=='Corporate') & (df['Issuer']!='REPUBLIC OF SOUTH AFRICA') & (df['Guarantee']!='Government Guaranteed') & ((df['National Rating']=='A+') | (df['National Rating']=='A') | (df['National Rating']=='A-'))]['Single Issuer Exposure'].max()
df_2 = pd.DataFrame({'Description':'Any A+, A or A-','Limits':[0.05],'Exposure': [x], 'Compliance':[np.where(x>0.05,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[(df['Issuer Type']=='Corporate') & (df['Issuer']!='REPUBLIC OF SOUTH AFRICA') & (df['Guarantee']!='Government Guaranteed') & ((df['National Rating']=='BBB+') | (df['National Rating']=='BBB') | (df['National Rating']=='BBB-'))]['Single Issuer Exposure'].max()
df_2 = pd.DataFrame({'Description':'Any BBB+, BBB and BBB-','Limits':[0.03],'Exposure': [x], 'Compliance':[np.where(x>0.03,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[(df['Issuer Type']=='Corporate') & (df['Issuer']!='REPUBLIC OF SOUTH AFRICA') & (df['Guarantee']!='Government Guaranteed') & (df['National Rating']!='AAA') & (df['National Rating']!='AA+') & (df['National Rating']!='AA') & (df['National Rating']!='AA-') & (df['National Rating']!='A+') 
& (df['National Rating']!='A') & (df['National Rating']!='A-') & (df['National Rating']!='BBB+') & (df['National Rating']!='BBB') & (df['National Rating']!='BBB-')]['Single Issuer Exposure'].max()
df_2 = pd.DataFrame({'Description':'Any BB+ or lower*','Limits':[0],'Exposure': [x], 'Compliance':[np.where(x>0,'No','Yes')]})
df_dict = df_dict.append(df_2)

df_2 = pd.DataFrame({'Description':[''],'Limits':[''],'Exposure':[''], 'Compliance':['']})
df_dict = df_dict.append(df_2)

x = df[((df['National Rating']=='AAA') | (df['National Rating']=='AA+') | (df['National Rating']=='AA') | (df['National Rating']=='AA-'))]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'RSA Government, Government guaranteed, AAA or AA-','Limits':[1],'Exposure': [x], 'Compliance':[np.where(x>1,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[((df['National Rating']=='A+') | (df['National Rating']=='A') | (df['National Rating']=='A-'))]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'A+, A, A-','Limits':[0.5],'Exposure': [x], 'Compliance':[np.where(x>0.5,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[((df['National Rating']=='BBB+') | (df['National Rating']=='BBB') | (df['National Rating']=='BBB-'))]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'BBB+, BBB and BBB-','Limits':[0.1],'Exposure': [x], 'Compliance':[np.where(x>0.1,'No','Yes')]})
df_dict = df_dict.append(df_2)

df_2 = pd.DataFrame({'Description':[''],'Limits':[''],'Exposure':[''], 'Compliance':['']})
df_dict = df_dict.append(df_2)

x = df[((df['Issuer']=='RMB') | (df['Issuer']=='ABSA BANK LIMITED') | (df['Issuer']=='NEDBANK GROUP') | (df['Issuer']=='NEDBANK') | (df['Issuer']=='STANDARD BANK SOUTH AFRICA'))]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'Big Four SA Bank Combined','Limits':[0.75],'Exposure': [x], 'Compliance':[np.where(x>0.75,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[((df['Issuer']=='INVESTEC BANK LTD') | (df['Issuer']=='CAPITEC'))]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'Investec Bank and Capitec Bank combined exposure','Limits':[0.15],'Exposure': [x], 'Compliance':[np.where(x>0.15,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[((df['Issuer']=='BNP PARIBAS') | (df['Issuer']=='HSBC'))]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'Non-SA owned banks with SA branch combined exposure','Limits':[0.15],'Exposure': [x], 'Compliance':[np.where(x>0.15,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[(df['Industry']=='Real Estate')]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'Real estate and property','Limits':[0.2],'Exposure': [x], 'Compliance':[np.where(x>0.2,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[(df['Industry']!='Government') & (df['Industry']!='Banks')]['Single Industry Exposure'].max()
df_2 = pd.DataFrame({'Description':'Single Industry Exposure','Limits':[0.15],'Exposure': [x], 'Compliance':[np.where(x>0.15,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = 0
df_2 = pd.DataFrame({'Description':'Listed bank issued conduit paper','Limits':[0.05],'Exposure': [x], 'Compliance':[np.where(x>0.05,'No','Yes')]})
df_dict = df_dict.append(df_2)

df_2 = pd.DataFrame({'Description':[''],'Limits':[''],'Exposure':[''], 'Compliance':['']})
df_dict = df_dict.append(df_2)

x = df[(df['Issuer']=='ABSA BANK LIMITED')]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'ABSA/Barclays','Limits':[0.2],'Exposure': [x], 'Compliance':[np.where(x>0.2,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[((df['Issuer']=='NEDBANK GROUP') | (df['Issuer']=='NEDBANK'))]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'Nedbank','Limits':[0.2],'Exposure': [x], 'Compliance':[np.where(x>0.2,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[(df['Issuer']=='STANDARD BANK SOUTH AFRICA')]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'Standard Bank','Limits':[0.2],'Exposure': [x], 'Compliance':[np.where(x>0.2,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[(df['Issuer']=='RMB')]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'FirstRand','Limits':[0.15],'Exposure': [x], 'Compliance':[np.where(x>0.15,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = 0
df_2 = pd.DataFrame({'Description':'Tier II Subordinated Debt (Standard Bank, Nedbank, ABSA Bank/Barclays)','Limits':[0],'Exposure': [x], 'Compliance':[np.where(x>0,'No','Yes')]})
df_dict = df_dict.append(df_2)

df_2 = pd.DataFrame({'Description':[''],'Limits':[''],'Exposure':[''], 'Compliance':['']})
df_dict = df_dict.append(df_2)

x = df[(df['Classification']==3)]['Single Issuer Exposure'].max()
df_2 = pd.DataFrame({'Description':'Single Conduit','Limits':[0.05],'Exposure': [x], 'Compliance':[np.where(x>0.05,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df['Weighted Duration'].sum()
df_2 = pd.DataFrame({'Description':'Weighted Average Modified Duration','Limits':'1 year','Exposure': [x], 'Compliance':[np.where(x>1,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = (df['Time to Maturity (days)']/365).max()
df_2 = pd.DataFrame({'Description':'Term to Maturity of a Single Instrument','Limits':'12 years','Exposure': [x], 'Compliance':[np.where(x>12,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[(df['Time to Maturity (days)']<=365)]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'Term to Maturity less than one year','Limits':'Minimum 65%','Exposure': [x], 'Compliance':[np.where(x<0.65,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = 1
df_2 = pd.DataFrame({'Description':'South African Rand','Limits':[1],'Exposure':[x], 'Compliance':[np.where(x>1,'No','Yes')]})
df_dict = df_dict.append(df_2)

df_dict = df_dict.fillna(0)
df_dict.to_excel(writer,'FNB FLI LT Cap', index=False)


#************************************************************************************************************************************************************************************
# 'Friscol'

# Config file
df = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\reports\compliance\holdings\combined\holdings_' + datetime_obj_end + '.xlsx', sheet_name='Friscol')
x = df[df['Classification']==1]['%Market Value'].sum()
df_dict = pd.DataFrame({'Description':'1. Instruments issued or guaranteed by the South African Government','Limits':[1],'Exposure': [x], 'Compliance':[np.where(x>1,'No','Yes')]})

x = df[df['Classification']==2]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'2. Bank deposits, Notes, Bills, NCDs or other securities issues endorsed by banks','Limits':[1],'Exposure': [x], 'Compliance':[np.where(x>1,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[df['Classification']==3]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'3. Bank issued conduit paper (listed)','Limits':[0.15],'Exposure': [x], 'Compliance':[np.where(x>0.15,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[df['Classification']==4]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'4. Direct look through notes','Limits':[0.15],'Exposure': [x], 'Compliance':[np.where(x>0.15,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[df['Classification']==5]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'5. Commercial paper','Limits':[1],'Exposure': [x], 'Compliance':[np.where(x>1,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[df['Classification']==6]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'6. Listed bonds','Limits':[1],'Exposure': [x], 'Compliance':[np.where(x>1,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[df['Classification']==7]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'7. Repurchase agreements','Limits':[0],'Exposure': [x], 'Compliance':[np.where(x>0,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[df['Classification']==8]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'8. Interest rate derivatives for hedging purposes only','Limits':[0.25],'Exposure': [x], 'Compliance':[np.where(x>0.25,'No','Yes')]})
df_dict = df_dict.append(df_2)

df_2 = pd.DataFrame({'Description':[''],'Limits':[''],'Exposure':[''], 'Compliance':['']})
df_dict = df_dict.append(df_2)

x = df[df['Issuer']=='REPUBLIC OF SOUTH AFRICA']['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'RSA Government','Limits':[1],'Exposure': [x], 'Compliance':[np.where(x>1,'No','Yes')]})
df_dict = df_dict.append(df_2)

df_2 = pd.DataFrame({'Description':[''],'Limits':[''],'Exposure':[''], 'Compliance':['']})
df_dict = df_dict.append(df_2)

x = df[((df['Industry']=='SOE') | (df['Industry']=='Banks')) & (df['Guarantee']=='Government Guaranteed') & (df['Issuer']!='RMB') & (df['Issuer']!='ABSA BANK LIMITED')
& (df['Issuer']!='NEDBANK GROUP') & (df['Issuer']!='NEDBANK') & (df['Issuer']!='STANDARD BANK SOUTH AFRICA')]['Single Issuer Exposure'].max()
df_2 = pd.DataFrame({'Description':'Any Government guaranteed issuer','Limits':[0.15],'Exposure': [x], 'Compliance':[np.where(x>0.15,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[((df['Industry']=='SOE') | (df['Industry']=='Banks')) & (df['Issuer']!='REPUBLIC OF SOUTH AFRICA') & (df['Guarantee']!='Government Guaranteed') & (df['Issuer']!='RMB') & 
(df['Issuer']!='ABSA BANK LIMITED') & (df['Issuer']!='NEDBANK GROUP') & (df['Issuer']!='NEDBANK') & (df['Issuer']!='STANDARD BANK SOUTH AFRICA') & ((df['National Rating']=='AAA') | (df['National Rating']=='AA+') | (df['National Rating']=='AA') | (df['National Rating']=='AA-'))]['Single Issuer Exposure'].max()
df_2 = pd.DataFrame({'Description':'Any AAA, AA+, AA or AA-','Limits':[0.1],'Exposure': [x], 'Compliance':[np.where(x>0.1,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[((df['Industry']=='SOE') | (df['Industry']=='Banks')) & (df['Issuer']!='REPUBLIC OF SOUTH AFRICA') & (df['Guarantee']!='Government Guaranteed') & (df['Issuer']!='RMB') & 
(df['Issuer']!='ABSA BANK LIMITED') & (df['Issuer']!='NEDBANK GROUP') & (df['Issuer']!='NEDBANK') & (df['Issuer']!='STANDARD BANK SOUTH AFRICA') & ((df['National Rating']=='A+') | (df['National Rating']=='A') | (df['National Rating']=='A-'))]['Single Issuer Exposure'].max()
df_2 = pd.DataFrame({'Description':'Any A+, A or A-','Limits':[0.07],'Exposure': [x], 'Compliance':[np.where(x>0.07,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[((df['Industry']=='SOE') | (df['Industry']=='Banks')) & (df['Issuer']!='REPUBLIC OF SOUTH AFRICA') & (df['Guarantee']!='Government Guaranteed') & (df['Issuer']!='RMB') & 
(df['Issuer']!='ABSA BANK LIMITED') & (df['Issuer']!='NEDBANK GROUP') & (df['Issuer']!='NEDBANK') & (df['Issuer']!='STANDARD BANK SOUTH AFRICA') & ((df['National Rating']=='BBB+') | (df['National Rating']=='BBB') | (df['National Rating']=='BBB-'))]['Single Issuer Exposure'].max()
df_2 = pd.DataFrame({'Description':'Any BBB+, BBB and BBB-','Limits':[0.03],'Exposure': [x], 'Compliance':[np.where(x>0.03,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[((df['Industry']=='SOE') | (df['Industry']=='Banks')) & (df['Issuer']!='REPUBLIC OF SOUTH AFRICA') & (df['Guarantee']!='Government Guaranteed') & (df['Issuer']!='RMB') & 
(df['Issuer']!='ABSA BANK LIMITED') & (df['Issuer']!='NEDBANK GROUP') & (df['Issuer']!='NEDBANK') & (df['Issuer']!='STANDARD BANK SOUTH AFRICA') & (df['National Rating']!='AAA') & (df['National Rating']!='AA+') & (df['National Rating']!='AA') & (df['National Rating']!='AA-') & (df['National Rating']!='A+') 
& (df['National Rating']!='A') & (df['National Rating']!='A-') & (df['National Rating']!='BBB+') & (df['National Rating']!='BBB') & (df['National Rating']!='BBB-')]['Single Issuer Exposure'].max()
df_2 = pd.DataFrame({'Description':'Any BB+ or lower*','Limits':[0],'Exposure': [x], 'Compliance':[np.where(x>0,'No','Yes')]})
df_dict = df_dict.append(df_2)

df_2 = pd.DataFrame({'Description':[''],'Limits':[''],'Exposure':[''], 'Compliance':['']})
df_dict = df_dict.append(df_2)

x = df[(df['Issuer Type']=='Corporate') & (df['Guarantee']=='Government Guaranteed')]['Single Issuer Exposure'].max()
df_2 = pd.DataFrame({'Description':'Any Government guaranteed issuer','Limits':[0.15],'Exposure': [x], 'Compliance':[np.where(x>0.15,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[(df['Issuer Type']=='Corporate') & (df['Issuer']!='REPUBLIC OF SOUTH AFRICA') & (df['Guarantee']!='Government Guaranteed') & ((df['National Rating']=='AAA') | (df['National Rating']=='AA+') | (df['National Rating']=='AA') | (df['National Rating']=='AA-'))]['Single Issuer Exposure'].max()
df_2 = pd.DataFrame({'Description':'Any AAA, AA+, AA or AA-','Limits':[0.08],'Exposure': [x], 'Compliance':[np.where(x>0.08,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[(df['Issuer Type']=='Corporate') & (df['Issuer']!='REPUBLIC OF SOUTH AFRICA') & (df['Guarantee']!='Government Guaranteed') & ((df['National Rating']=='A+') | (df['National Rating']=='A') | (df['National Rating']=='A-'))]['Single Issuer Exposure'].max()
df_2 = pd.DataFrame({'Description':'Any A+, A or A-','Limits':[0.05],'Exposure': [x], 'Compliance':[np.where(x>0.05,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[(df['Issuer Type']=='Corporate') & (df['Issuer']!='REPUBLIC OF SOUTH AFRICA') & (df['Guarantee']!='Government Guaranteed') & ((df['National Rating']=='BBB+') | (df['National Rating']=='BBB') | (df['National Rating']=='BBB-'))]['Single Issuer Exposure'].max()
df_2 = pd.DataFrame({'Description':'Any BBB+, BBB and BBB-','Limits':[0.03],'Exposure': [x], 'Compliance':[np.where(x>0.03,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[(df['Issuer Type']=='Corporate') & (df['Issuer']!='REPUBLIC OF SOUTH AFRICA') & (df['Guarantee']!='Government Guaranteed') & (df['National Rating']!='AAA') & (df['National Rating']!='AA+') & (df['National Rating']!='AA') & (df['National Rating']!='AA-') & (df['National Rating']!='A+') 
& (df['National Rating']!='A') & (df['National Rating']!='A-') & (df['National Rating']!='BBB+') & (df['National Rating']!='BBB') & (df['National Rating']!='BBB-')]['Single Issuer Exposure'].max()
df_2 = pd.DataFrame({'Description':'Any BB+ or lower*','Limits':[0],'Exposure': [x], 'Compliance':[np.where(x>0,'No','Yes')]})
df_dict = df_dict.append(df_2)

df_2 = pd.DataFrame({'Description':[''],'Limits':[''],'Exposure':[''], 'Compliance':['']})
df_dict = df_dict.append(df_2)

x = df[((df['National Rating']=='AAA') | (df['National Rating']=='AA+') | (df['National Rating']=='AA') | (df['National Rating']=='AA-'))]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'RSA Government, Government guaranteed, AAA or AA-','Limits':[1],'Exposure': [x], 'Compliance':[np.where(x>1,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[((df['National Rating']=='A+') | (df['National Rating']=='A') | (df['National Rating']=='A-'))]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'A+, A, A-','Limits':[0.5],'Exposure': [x], 'Compliance':[np.where(x>0.5,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[((df['National Rating']=='BBB+') | (df['National Rating']=='BBB') | (df['National Rating']=='BBB-'))]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'BBB+, BBB and BBB-','Limits':[0.1],'Exposure': [x], 'Compliance':[np.where(x>0.1,'No','Yes')]})
df_dict = df_dict.append(df_2)

df_2 = pd.DataFrame({'Description':[''],'Limits':[''],'Exposure':[''], 'Compliance':['']})
df_dict = df_dict.append(df_2)

x = df[((df['Issuer']=='RMB') | (df['Issuer']=='ABSA BANK LIMITED') | (df['Issuer']=='NEDBANK GROUP') | (df['Issuer']=='NEDBANK') | (df['Issuer']=='STANDARD BANK SOUTH AFRICA'))]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'Big Four SA Bank Combined','Limits':[0.75],'Exposure': [x], 'Compliance':[np.where(x>0.75,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[((df['Issuer']=='INVESTEC BANK LTD') | (df['Issuer']=='CAPITEC'))]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'Investec Bank and Capitec Bank combined exposure','Limits':[0.15],'Exposure': [x], 'Compliance':[np.where(x>0.15,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[((df['Issuer']=='BNP PARIBAS') | (df['Issuer']=='HSBC'))]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'Non-SA owned banks with SA branch combined exposure','Limits':[0.15],'Exposure': [x], 'Compliance':[np.where(x>0.15,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[(df['Industry']=='Real Estate')]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'Real estate and property','Limits':[0.15],'Exposure': [x], 'Compliance':[np.where(x>0.15,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[(df['Industry']!='Government') & (df['Industry']!='Banks')]['Single Industry Exposure'].max()
df_2 = pd.DataFrame({'Description':'Single Industry Exposure','Limits':[0.15],'Exposure': [x], 'Compliance':[np.where(x>0.15,'No','Yes')]})
df_dict = df_dict.append(df_2)

df_2 = pd.DataFrame({'Description':[''],'Limits':[''],'Exposure':[''], 'Compliance':['']})
df_dict = df_dict.append(df_2)

x = df[(df['Issuer']=='ABSA BANK LIMITED')]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'ABSA/Barclays','Limits':[0.2],'Exposure': [x], 'Compliance':[np.where(x>0.2,'No','Yes')]})
df_dict = df_dict.append(df_2)

x  = df[((df['Issuer']=='NEDBANK GROUP') | (df['Issuer']=='NEDBANK'))]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'Nedbank','Limits':[0.2],'Exposure': [x], 'Compliance':[np.where(x>0.2,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[(df['Issuer']=='STANDARD BANK SOUTH AFRICA')]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'Standard Bank','Limits':[0.2],'Exposure': [x], 'Compliance':[np.where(x>0.2,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[(df['Issuer']=='RMB')]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'FirstRand','Limits':[0.15],'Exposure': [x], 'Compliance':[np.where(x>0.15,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = 0
df_2 = pd.DataFrame({'Description':'Tier II Subordinated Debt (Standard Bank, Nedbank, ABSA Bank/Barclays)','Limits':[0],'Exposure': [x], 'Compliance':[np.where(x>0,'No','Yes')]})
df_dict = df_dict.append(df_2)

df_2 = pd.DataFrame({'Description':[''],'Limits':[''],'Exposure':[''], 'Compliance':['']})
df_dict = df_dict.append(df_2)

x = df[(df['Classification']==3)]['Single Issuer Exposure'].max()
df_2 = pd.DataFrame({'Description':'Single Conduit','Limits':[0.05],'Exposure': [x], 'Compliance':[np.where(x>0.05,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df['Weighted Duration'].sum()
df_2 = pd.DataFrame({'Description':'Weighted Average Modified Duration','Limits':'1 year','Exposure': [x], 'Compliance':[np.where(x>1,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = (df['Time to Maturity (days)']/365).max()
df_2 = pd.DataFrame({'Description':'Term to Maturity of a Single Instrument','Limits':'12 years','Exposure': [x], 'Compliance':[np.where(x>12,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[(df['Time to Maturity (days)']<=365)]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'Term to Maturity less than one year','Limits':'Minimum 75%','Exposure': [x], 'Compliance':[np.where(x<0.75,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = 1
df_2 = pd.DataFrame({'Description':'South African Rand','Limits':[1],'Exposure':[x], 'Compliance':[np.where(x>1,'No','Yes')]})
df_dict = df_dict.append(df_2)

df_dict = df_dict.fillna(0)
df_dict.to_excel(writer,'Friscol', index=False)


#************************************************************************************************************************************************************************************
# 'FNB IBNR RPF'

# Config file
df = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\reports\compliance\holdings\combined\holdings_' + datetime_obj_end + '.xlsx', sheet_name='FNB IBNR RPF')
x = df[df['Classification']==1]['%Market Value'].sum()
df_dict = pd.DataFrame({'Description':'1. Instruments issued or guaranteed by the South African Government','Limits':[1],'Exposure': [x], 'Compliance':[np.where(x>1,'No','Yes')]})

x = df[(df['Classification']==2) & (df['InstrumentType']!='FundingAccount')]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'2. Bank deposits, Notes, Bills, NCDs or other securities issues endorsed by banks','Limits':[0.3],'Exposure': [x], 'Compliance':[np.where(x>0.3,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[df['Classification']==3]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'3. Bank issued conduit paper (listed)','Limits':[0],'Exposure': [x], 'Compliance':[np.where(x>0,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[df['Classification']==4]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'4. Direct look through notes','Limits':[0],'Exposure': [x], 'Compliance':[np.where(x>0,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[df['Classification']==5]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'5. Commercial paper','Limits':[0],'Exposure': [x], 'Compliance':[np.where(x>0,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[df['Classification']==6]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'6. Listed bonds','Limits':[0],'Exposure': [x], 'Compliance':[np.where(x>0,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[df['Classification']==7]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'7. Repurchase agreements','Limits':[0],'Exposure': [x], 'Compliance':[np.where(x>0,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[df['Classification']==8]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'8. Interest rate derivatives for hedging purposes only','Limits':[0.25],'Exposure': [x], 'Compliance':[np.where(x>0.25,'No','Yes')]})
df_dict = df_dict.append(df_2)

df_2 = pd.DataFrame({'Description':[''],'Limits':[''],'Exposure':[''], 'Compliance':['']})
df_dict = df_dict.append(df_2)

x = df[df['Issuer']=='REPUBLIC OF SOUTH AFRICA']['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'RSA Government','Limits':[1],'Exposure': [x], 'Compliance':[np.where(x>1,'No','Yes')]})
df_dict = df_dict.append(df_2)

df_2 = pd.DataFrame({'Description':[''],'Limits':[''],'Exposure':[''], 'Compliance':['']})
df_dict = df_dict.append(df_2)

# Portfolio level issuer limits
x = df[((df['National Rating']=='AAA') | (df['National Rating']=='AA+') | (df['National Rating']=='AA') | (df['National Rating']=='AA-'))]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'RSA Government, Government guaranteed, AAA or AA-','Limits':[1],'Exposure': [x], 'Compliance':[np.where(x>1,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[((df['National Rating']=='A+') | (df['National Rating']=='A') | (df['National Rating']=='A-'))]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'A+, A, A-','Limits':[0.5],'Exposure': [x], 'Compliance':[np.where(x>0.5,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[((df['National Rating']=='BBB+') | (df['National Rating']=='BBB') | (df['National Rating']=='BBB-'))]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'BBB+, BBB and BBB-','Limits':[0.1],'Exposure': [x], 'Compliance':[np.where(x>0.1,'No','Yes')]})
df_dict = df_dict.append(df_2)

df_2 = pd.DataFrame({'Description':[''],'Limits':[''],'Exposure':[''], 'Compliance':['']})
df_dict = df_dict.append(df_2)

# Big Four Banks
x = df[(df['Issuer']=='ABSA BANK LIMITED')]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'ABSA/Barclays','Limits':[0.2],'Exposure': [x], 'Compliance':[np.where(x>0.2,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[((df['Issuer']=='NEDBANK GROUP') | (df['Issuer']=='NEDBANK'))]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'Nedbank','Limits':[0.2],'Exposure': [x], 'Compliance':[np.where(x>0.2,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[(df['Issuer']=='STANDARD BANK SOUTH AFRICA')]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'Standard Bank','Limits':[0.2],'Exposure': [x], 'Compliance':[np.where(x>0.2,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[(df['Issuer']=='RMB')]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'FirstRand','Limits':[0.1],'Exposure': [x], 'Compliance':[np.where(x>0.1,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = 0
df_2 = pd.DataFrame({'Description':'Tier II Subordinated Debt (Standard Bank, Nedbank, ABSA Bank/Barclays)','Limits':[0],'Exposure': [x], 'Compliance':[np.where(x>0,'No','Yes')]})
df_dict = df_dict.append(df_2)

df_2 = pd.DataFrame({'Description':[''],'Limits':[''],'Exposure':[''], 'Compliance':['']})
df_dict = df_dict.append(df_2)

# Additional Limits
x = df['Weighted Duration'].sum()
df_2 = pd.DataFrame({'Description':'Weighted Average Modified Duration','Limits':'1 year','Exposure': [x], 'Compliance':[np.where(x>1,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = (df['Time to Maturity (days)']/365*12).max()
df_2 = pd.DataFrame({'Description':'Term to Maturity of a Single Instrument','Limits':'12 years','Exposure': [x], 'Compliance':[np.where(x>12,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[(df['Time to Maturity (days)']<=91)]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'Term to Maturity less than one year','Limits':'Minimum 30%','Exposure': [x], 'Compliance':[np.where(x<0.3,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = 1
df_2 = pd.DataFrame({'Description':'South African Rand','Limits':[1],'Exposure':[x], 'Compliance':[np.where(x>1,'No','Yes')]})
df_dict = df_dict.append(df_2)

df_dict = df_dict.fillna(0)
df_dict.to_excel(writer,'FNB IBNR RPF', index=False)


#************************************************************************************************************************************************************************************
# 'FNB IBNR IPF'

# Config file
df = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\reports\compliance\holdings\combined\holdings_' + datetime_obj_end + '.xlsx', sheet_name='FNB IBNR IPF')
x = df[df['Classification']==1]['%Market Value'].sum()
df_dict = pd.DataFrame({'Description':'1. Instruments issued or guaranteed by the South African Government','Limits':[1],'Exposure': [x], 'Compliance':[np.where(x>1,'No','Yes')]})

x = df[(df['Classification']==2) & (df['InstrumentType']!='FundingAccount')]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'2. Bank deposits, Notes, Bills, NCDs or other securities issues endorsed by banks','Limits':[0.3],'Exposure': [x], 'Compliance':[np.where(x>0.3,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[df['Classification']==3]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'3. Bank issued conduit paper (listed)','Limits':[0],'Exposure': [x], 'Compliance':[np.where(x>0,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[df['Classification']==4]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'4. Direct look through notes','Limits':[0],'Exposure': [x], 'Compliance':[np.where(x>0,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[df['Classification']==5]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'5. Commercial paper','Limits':[0],'Exposure': [x], 'Compliance':[np.where(x>0,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[df['Classification']==6]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'6. Listed bonds','Limits':[0],'Exposure': [x], 'Compliance':[np.where(x>0,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[df['Classification']==7]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'7. Repurchase agreements','Limits':[0],'Exposure': [x], 'Compliance':[np.where(x>0,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[df['Classification']==8]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'8. Interest rate derivatives for hedging purposes only','Limits':[0.25],'Exposure': [x], 'Compliance':[np.where(x>0.25,'No','Yes')]})
df_dict = df_dict.append(df_2)

df_2 = pd.DataFrame({'Description':[''],'Limits':[''],'Exposure':[''], 'Compliance':['']})
df_dict = df_dict.append(df_2)

x = df[df['Issuer']=='REPUBLIC OF SOUTH AFRICA']['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'RSA Government','Limits':[1],'Exposure': [x], 'Compliance':[np.where(x>1,'No','Yes')]})
df_dict = df_dict.append(df_2)

df_2 = pd.DataFrame({'Description':[''],'Limits':[''],'Exposure':[''], 'Compliance':['']})
df_dict = df_dict.append(df_2)

# Portfolio level issuer limits
x = df[((df['National Rating']=='AAA') | (df['National Rating']=='AA+') | (df['National Rating']=='AA') | (df['National Rating']=='AA-'))]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'RSA Government, Government guaranteed, AAA or AA-','Limits':[1],'Exposure': [x], 'Compliance':[np.where(x>1,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[((df['National Rating']=='A+') | (df['National Rating']=='A') | (df['National Rating']=='A-'))]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'A+, A, A-','Limits':[0.5],'Exposure': [x], 'Compliance':[np.where(x>0.5,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[((df['National Rating']=='BBB+') | (df['National Rating']=='BBB') | (df['National Rating']=='BBB-'))]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'BBB+, BBB and BBB-','Limits':[0.1],'Exposure': [x], 'Compliance':[np.where(x>0.1,'No','Yes')]})
df_dict = df_dict.append(df_2)

df_2 = pd.DataFrame({'Description':[''],'Limits':[''],'Exposure':[''], 'Compliance':['']})
df_dict = df_dict.append(df_2)

# Big Four Banks
x = df[(df['Issuer']=='ABSA BANK LIMITED')]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'ABSA/Barclays','Limits':[0.2],'Exposure': [x], 'Compliance':[np.where(x>0.2,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[((df['Issuer']=='NEDBANK GROUP') | (df['Issuer']=='NEDBANK'))]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'Nedbank','Limits':[0.2],'Exposure': [x], 'Compliance':[np.where(x>0.2,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[(df['Issuer']=='STANDARD BANK SOUTH AFRICA')]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'Standard Bank','Limits':[0.2],'Exposure': [x], 'Compliance':[np.where(x>0.2,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[(df['Issuer']=='RMB')]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'FirstRand','Limits':[0.1],'Exposure': [x], 'Compliance':[np.where(x>0.1,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = 0
df_2 = pd.DataFrame({'Description':'Tier II Subordinated Debt (Standard Bank, Nedbank, ABSA Bank/Barclays)','Limits':[0],'Exposure': [x], 'Compliance':[np.where(x>0,'No','Yes')]})
df_dict = df_dict.append(df_2)

df_2 = pd.DataFrame({'Description':[''],'Limits':[''],'Exposure':[''], 'Compliance':['']})
df_dict = df_dict.append(df_2)

# Additional Limits
x = df['Weighted Duration'].sum()
df_2 = pd.DataFrame({'Description':'Weighted Average Modified Duration','Limits':'1 year','Exposure': [x], 'Compliance':[np.where(x>1,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = (df['Time to Maturity (days)']/365*12).max()
df_2 = pd.DataFrame({'Description':'Term to Maturity of a Single Instrument','Limits':'12 years','Exposure': [x], 'Compliance':[np.where(x>12,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[(df['Time to Maturity (days)']<=91)]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'Term to Maturity less than one year','Limits':'Minimum 30%','Exposure': [x], 'Compliance':[np.where(x<0.3,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = 1
df_2 = pd.DataFrame({'Description':'South African Rand','Limits':[1],'Exposure':[x], 'Compliance':[np.where(x>1,'No','Yes')]})
df_dict = df_dict.append(df_2)

df_dict = df_dict.fillna(0)
df_dict.to_excel(writer,'FNB IBNR IPF', index=False)


#************************************************************************************************************************************************************************************
# 'FNB FLI Working Cap '

# Config file
df = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\reports\compliance\holdings\combined\holdings_' + datetime_obj_end + '.xlsx', sheet_name='FNB FLI Working')
x = df[df['Classification']==1]['%Market Value'].sum()
df_dict = pd.DataFrame({'Description':'1. Instruments issued or guaranteed by the South African Government','Limits':[1],'Exposure': [x], 'Compliance':[np.where(x>1,'No','Yes')]})

x = df[(df['Classification']==2) & (df['InstrumentType']!='FundingAccount')]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'2. Bank deposits, Notes, Bills, NCDs or other securities issues endorsed by banks','Limits':[0.3],'Exposure': [x], 'Compliance':[np.where(x>0.3,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[df['Classification']==3]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'3. Bank issued conduit paper (listed)','Limits':[0],'Exposure': [x], 'Compliance':[np.where(x>0,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[df['Classification']==4]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'4. Direct look through notes','Limits':[0],'Exposure': [x], 'Compliance':[np.where(x>0,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[df['Classification']==5]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'5. Commercial paper','Limits':[0],'Exposure': [x], 'Compliance':[np.where(x>0,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[df['Classification']==6]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'6. Listed bonds','Limits':[0],'Exposure': [x], 'Compliance':[np.where(x>0,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[df['Classification']==7]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'7. Repurchase agreements','Limits':[0],'Exposure': [x], 'Compliance':[np.where(x>0,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[df['Classification']==8]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'8. Interest rate derivatives for hedging purposes only','Limits':[0.25],'Exposure': [x], 'Compliance':[np.where(x>0.25,'No','Yes')]})
df_dict = df_dict.append(df_2)

df_2 = pd.DataFrame({'Description':[''],'Limits':[''],'Exposure':[''], 'Compliance':['']})
df_dict = df_dict.append(df_2)

x = df[df['Issuer']=='REPUBLIC OF SOUTH AFRICA']['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'RSA Government','Limits':[1],'Exposure': [x], 'Compliance':[np.where(x>1,'No','Yes')]})
df_dict = df_dict.append(df_2)

df_2 = pd.DataFrame({'Description':[''],'Limits':[''],'Exposure':[''], 'Compliance':['']})
df_dict = df_dict.append(df_2)

# Portfolio level issuer limits
x = df[((df['National Rating']=='AAA') | (df['National Rating']=='AA+') | (df['National Rating']=='AA') | (df['National Rating']=='AA-'))]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'RSA Government, Government guaranteed, AAA or AA-','Limits':[1],'Exposure': [x], 'Compliance':[np.where(x>1,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[((df['National Rating']=='A+') | (df['National Rating']=='A') | (df['National Rating']=='A-'))]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'A+, A, A-','Limits':[0.5],'Exposure': [x], 'Compliance':[np.where(x>0.5,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[((df['National Rating']=='BBB+') | (df['National Rating']=='BBB') | (df['National Rating']=='BBB-'))]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'BBB+, BBB and BBB-','Limits':[0.1],'Exposure': [x], 'Compliance':[np.where(x>0.1,'No','Yes')]})
df_dict = df_dict.append(df_2)

df_2 = pd.DataFrame({'Description':[''],'Limits':[''],'Exposure':[''], 'Compliance':['']})
df_dict = df_dict.append(df_2)

# Big Four Banks
x = df[(df['Issuer']=='ABSA BANK LIMITED')]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'ABSA/Barclays','Limits':[0.2],'Exposure': [x], 'Compliance':[np.where(x>0.2,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[((df['Issuer']=='NEDBANK GROUP') | (df['Issuer']=='NEDBANK'))]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'Nedbank','Limits':[0.2],'Exposure': [x], 'Compliance':[np.where(x>0.2,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[(df['Issuer']=='STANDARD BANK SOUTH AFRICA')]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'Standard Bank','Limits':[0.2],'Exposure': [x], 'Compliance':[np.where(x>0.2,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[(df['Issuer']=='RMB')]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'FirstRand','Limits':[0.1],'Exposure': [x], 'Compliance':[np.where(x>0.1,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = 0
df_2 = pd.DataFrame({'Description':'Tier II Subordinated Debt (Standard Bank, Nedbank, ABSA Bank/Barclays)','Limits':[0],'Exposure': [x], 'Compliance':[np.where(x>0,'No','Yes')]})
df_dict = df_dict.append(df_2)

df_2 = pd.DataFrame({'Description':[''],'Limits':[''],'Exposure':[''], 'Compliance':['']})
df_dict = df_dict.append(df_2)

# Additional Limits
x = df['Weighted Duration'].sum()
df_2 = pd.DataFrame({'Description':'Weighted Average Modified Duration','Limits':'1 year','Exposure': [x], 'Compliance':[np.where(x>1,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = (df['Time to Maturity (days)']/365*12).max()
df_2 = pd.DataFrame({'Description':'Term to Maturity of a Single Instrument','Limits':'12 years','Exposure': [x], 'Compliance':[np.where(x>12,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = df[(df['Time to Maturity (days)']<=91)]['%Market Value'].sum()
df_2 = pd.DataFrame({'Description':'Term to Maturity less than one year','Limits':'Minimum 70%','Exposure': [x], 'Compliance':[np.where(x<0.7,'No','Yes')]})
df_dict = df_dict.append(df_2)

x = 1
df_2 = pd.DataFrame({'Description':'South African Rand','Limits':[1],'Exposure':[x], 'Compliance':[np.where(x>1,'No','Yes')]})
df_dict = df_dict.append(df_2)

df_dict = df_dict.fillna(0)
df_dict.to_excel(writer,'FNB FLI Working Cap', index=False)


writer.save()