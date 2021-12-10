import pandas as pd
import odbc
import numpy as np
import datetime
from my_functions import custom_dates as cd
#PfCode = ['44110','65317','65326','65336','95101','95302','95935','95106','95107','95806']
PfCode = ['95101']
date_str_start = input('Enter start date (Format dd/mm/yyyy):')
format_str = '%d/%m/%Y' # The format
datetime_obj_start = str(datetime.datetime.strptime(date_str_start, format_str).date())
date_str_end = input('Enter end date (Format dd/mm/yyyy):')
format_str = '%d/%m/%Y' # The format
datetime_obj_end = str(datetime.datetime.strptime(date_str_end, format_str).date())
daterange = pd.date_range(str((pd.to_datetime(datetime_obj_start) + pd.DateOffset(days=1)).date()), datetime_obj_end)
writer = pd.ExcelWriter(r'Z:\Investment Analytics\Python\take_on\out\RMA Attribution_' + datetime_obj_start + '_' + datetime_obj_end + '.xlsx')

def checkIfValuesExists1(dfObj, listOfValues):
    ''' Check if given elements exists in dictionary or not.
        It returns a dictionary of elements as key and thier existence value as bool'''
    resultDict = {}
    # Iterate over the list of elements one by one
    for elem in listOfValues:
        # Check if the element exists in dataframe values
        if elem in dfObj.values:
            resultDict[elem] = True
        else:
            resultDict[elem] = False
    # Returns a dictionary of values & thier existence flag        
    return resultDict

# Adjustments
df_adj = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\Input\Adj.xlsx')
df_adj.PortfolioIDCode = df_adj.PortfolioIDCode.astype(str)
df_adj.ValuationDate = df_adj.ValuationDate.astype(str)
# Cashflow adjustments
df_adj_cash = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\Input\cashflow_adj.xlsx')
df_adj_cash.PortfolioIDCode = df_adj_cash.PortfolioIDCode.astype(str)
df_adj_cash.ValuationDate = df_adj_cash.ValuationDate.astype(str)
constr = "DRIVER={SQL Server Native Client 11.0};SERVER=ash-prdkblddbao,4071;DATABASE=AshburtonRisk;Trusted_Connection=yes;"
db = odbc.odbc(constr)
for i in PfCode:
    pieces = []
    pieces1 = []
    for dates in daterange:
        # Coupons from Static data
        coupon_date = str((pd.to_datetime(dates) + pd.DateOffset(days=-5)).date())
        sql = "SELECT DataDate, InstrumentCode, InstrumentShortName, InstrumentType, InstrumentCurrency, CouponFrequency, InterestRate, IssueDate,PrevCouponDate, NextCouponDate, ExDate, MaturityDate FROM Investment.MaitlandASISAInstruments WHERE DataDate = " + " ' " + coupon_date + "'" + "  AND InstrumentCurrency = 'ZAR' AND InterestRate IS NOT NULL AND InstrumentType NOT IN ('CALL MONEY','IDEE : CURRENCY') AND CouponFrequency IS NOT NULL AND MaturityDate IS NOT NULL"
        df_cp = pd.read_sql(sql, db)
        df_cp['ValuationDate'] = df_cp.DataDate
        df_cp.NextCouponDate = pd.to_datetime(df_cp.NextCouponDate, format='%Y/%m/%d').dt.strftime("%Y-%m-%d")
        df_cp.MaturityDate = pd.to_datetime(df_cp.MaturityDate, format='%Y/%m/%d').dt.strftime("%Y-%m-%d")
        df_cp = df_cp.drop_duplicates()
        df_cp = df_cp[df_cp.InterestRate != 0 ]
        df_cp['CouponFrequencyNum'] = np.where(df_cp.CouponFrequency == 'M', 12, np.where(df_cp.CouponFrequency == 'Q', 4, np.where(df_cp.CouponFrequency == 'S', 2, 0)))
        df_cp['Coupon'] = df_cp.InterestRate / df_cp.CouponFrequencyNum
        df_cp = df_cp[df_cp.NextCouponDate == str(dates.date())]
        df_cp = df_cp[['InstrumentCode','Coupon']]
        df_cp.rename(columns={'Coupon': 'Adj_Coupon'}, inplace=True)
        # Instrument type
        sql = "SELECT InstrumentCode, InstrumentTypeDescription, MaturityDate FROM Investment.MaitlandASISAInstruments WHERE DataDate = " + " ' " + str(dates.date()) + "'" + " AND InstrumentCurrency = 'ZAR'"
        df_type = pd.read_sql(sql, db)
        sql = "SELECT InstrumentCode, Delta FROM Investment.MaitlandASISAInstruments WHERE DataDate = " + " ' " + str((pd.to_datetime(dates) + pd.DateOffset(days=-1)).date()) + "'" + " AND InstrumentCurrency = 'ZAR'"
        df_type1 = pd.read_sql(sql, db)
        df_type = df_type.merge(df_type1, how='left', on=['InstrumentCode'])
        constr = "DRIVER={SQL Server Native Client 11.0};SERVER=ash-prdkblddbao,4071;DATABASE=AshburtonRisk;Trusted_Connection=yes;"
        db = odbc.odbc(constr)
        # Previous Holdings
        sql = "SELECT InstrumentCode, PortfolioCode, PortfolioName, BaseCurrency, InstrumentLongName, HoldingsNominal, EffectiveExpoure, AccruedIncome, MarketPrice FROM Investment.vwMaitlandHoldings WHERE ValuationDate = " + " '" + str((pd.to_datetime(dates) + pd.DateOffset(days=-1)).date()) + "'" + " AND PortfolioCode = " + "'" + i + "'" +""
        df = pd.read_sql(sql, db)
        df.InstrumentCode = df.InstrumentCode.str.upper()
        df['PrevAllInPrice'] = np.where((df.HoldingsNominal == 0) | (df.InstrumentCode == 'CASH') | (df.InstrumentCode.str.contains('EXPENSE')), 1, df.EffectiveExpoure / df.HoldingsNominal )
        # df['PrevAllInPrice'] = np.where(df['InstrumentTypeDescription'] == 'OPTION : BOND FUTURE', df['MarketPrice'], df['PrevAllInPrice'] )
        df['Weight'] = df.EffectiveExpoure / df.EffectiveExpoure.sum()
        df.rename(columns={'PortfolioCode':'PortfolioIDCode','EffectiveExpoure': 'PrevEffectiveExpoure', 'AccruedIncome': 'PrevAccruedIncome', 'HoldingsNominal': 'PrevHoldingsNominal','MarketPrice': 'PrevMarketPrice'}, inplace=True)
        # Current Holdings
        sql = "SELECT InstrumentCode, ValuationDate, PortfolioCode, PortfolioName, BaseCurrency, InstrumentLongName, HoldingsNominal, EffectiveExpoure, MarketPrice FROM Investment.vwMaitlandHoldings WHERE ValuationDate = " + " ' " + str(dates.date()) + "'" + " AND PortfolioCode = " + "'" + i + "'" +""
        df1 = pd.read_sql(sql, db)
        df1.InstrumentCode = df1.InstrumentCode.str.upper()
        df1['CurAllInPrice'] = np.where((df1.HoldingsNominal == 0) | (df1.InstrumentCode == 'CASH') | (df1.InstrumentCode.str.contains('EXPENSE')), 0, df1.EffectiveExpoure / df1.HoldingsNominal )
        # df1['CurAllInPrice'] = np.where(df['InstrumentTypeDescription'] == 'OPTION : BOND FUTURE', df1['MarketPrice'], df1['CurAllInPrice'] )
        df1 = df1[['InstrumentCode', 'HoldingsNominal', 'ValuationDate', 'CurAllInPrice', 'MarketPrice']]
        df1.rename(columns={'PortfolioCode':'PortfolioIDCode','HoldingsNominal': 'CurHoldingsNominal','MarketPrice': 'CurMarketPrice'}, inplace=True)
        df = df.merge(df1, how='left', on=['InstrumentCode'])
        # Previous JSE data
        sql = "SELECT * FROM Investment.vwDailyBondMTMGap WHERE Date = " + " ' " +  str((pd.to_datetime(dates) + pd.DateOffset(days=-1)).date()) + "'"
        df1 = pd.read_sql(sql, db)
        df1 = df1[['BondCode', 'Maturity', 'Coupon', 'CompanionBond', 'BPSpread', 'MTM', 'ModifiedDuration', 'Convexity', 'ReferenceCPI']]
        df1['BondCode'] = df1['BondCode'].str.upper()
        df1['AdjMTM'] = np.where(df1['CompanionBond'] == 'JIBAR', df1.Coupon,df1.MTM)
        df1.rename(columns={'BondCode': 'InstrumentCode','AdjMTM': 'PrevMTM', 'BPSpread': 'PrevBPSpread', 'ModifiedDuration': 'PrevModifiedDuration', 'Convexity': 'PrevConvexity', 'ReferenceCPI': 'PrevReferenceCPI'}, inplace=True)
        df = df.merge(df1, how='left', on=['InstrumentCode'])
        # Current JSE data
        constr = "DRIVER={SQL Server Native Client 11.0};SERVER=ash-prdkblddbao,4071;DATABASE=AshburtonRisk;Trusted_Connection=yes;"
        db = odbc.odbc(constr)
        sql = "SELECT * FROM Investment.vwDailyBondMTMGap WHERE Date = " + " ' " + str(dates.date()) + "'"
        df1 = pd.read_sql(sql, db)
        df1 = df1[['BondCode', 'BPSpread', 'MTM', 'ModifiedDuration', 'Convexity', 'ReferenceCPI']]
        df1['BondCode'] = df1['BondCode'].str.upper()
        df1.rename(columns={'BondCode': 'InstrumentCode','MTM': 'CurMTM', 'BPSpread': 'CurBPSpread', 'ModifiedDuration': 'CurModifiedDuration', 'Convexity': 'CurConvexity', 'ReferenceCPI': 'CurReferenceCPI'}, inplace=True)
        df = df.merge(df1, how='left', on=['InstrumentCode'])
        df = df.merge(df_type, how='left', on=['InstrumentCode'])
        df = df.merge(df_cp, how='left', on=['InstrumentCode'])
        df = df.drop_duplicates() 
        # Performance
        sql = "SELECT ValueDate, PortfolioCode, MarketValue, DayPreviousMktValue, TotalCashFlow, ManagementFees FROM Investment.MaitlandDailyFundPerformance WHERE ValueDate = " + " ' " + str(dates.date()) + "'" + " AND PortfolioCode = " + i + ""
        df1 = pd.read_sql(sql, db)
        df1.rename(columns={'PortfolioCode': 'PortfolioIDCode','ValueDate': 'ValuationDate'}, inplace=True)
        
        df1 = df1.merge(df_adj_cash, how='left', on=['PortfolioIDCode', 'ValuationDate'])
        df1['PercentageChangeGross'] = np.where(df1.TotalCashFlowAdj.isnull(),(df1.MarketValue - df1.DayPreviousMktValue - df1.TotalCashFlow - df1.ManagementFees)/ df1.DayPreviousMktValue, (df1.MarketValue - df1.DayPreviousMktValue - df1.TotalCashFlow - df1.TotalCashFlowAdj - df1.ManagementFees)/ df1.DayPreviousMktValue)*100
        df1 = df1[['PortfolioIDCode', 'PercentageChangeGross']]
        df = df.merge(df1, how='left', on=['PortfolioIDCode'])
        # CPI Returns
        cpi_returns = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\Input\CPI Intepolated numbers.xlsm', sheet_name = 'Intepolated_Numbers', usecols = [0,6])
        cpi_returns = cpi_returns[cpi_returns.Date == dates.date()]
        cpi_returns = cpi_returns[['CPI_Return']].values.item(0)
        df['Return'] = np.where(df['CurAllInPrice'] == 0, 0, df.CurAllInPrice / df.PrevAllInPrice - 1) + np.where(df['Adj_Coupon'].isnull(),0,df.PrevAccruedIncome/df.PrevEffectiveExpoure)
        # df['Return'] = np.where(df['InstrumentTypeDescription'] == 'OPTION : BOND FUTURE', df['CurMarketPrice']/df['PrevMarketPrice']-1, df['Return'] )
        # df['Return'] = np.where((df['CurMarketPrice'] == 0) | (df['PrevMarketPrice'] == 0), 0, df['Return'] )
        # df['Indicator'] = np.where(len(df[df.InstrumentCode == 'R2044']['Return'].values) == 0, 0, df[df.InstrumentCode == 'R2044']['Return'].fillna(0).values )
        # df['Return'] = np.where(df['InstrumentTypeDescription'] == 'OPTION : BOND FUTURE', df['Indicator']*df['Delta'], df['Return'] )
        df['Contribution'] = df['Weight'] * df['Return']
        df = df.merge(df_adj, how='left', on=['InstrumentCode', 'PortfolioIDCode', 'ValuationDate'])
        df['FinalContribution'] = np.where((df.InstrumentLongName.str.upper().str[:4] == 'REPO') & (df['MaturityDate'] == str(dates.date())) ,0,df['Contribution'])
        # df['FinalContribution'] = np.where((df['InstrumentTypeDescription'] == 'OPTION : BOND FUTURE') ,0,df['FinalContribution'])
        df['FinalContribution'] = np.where(df['AdjContribution'].isnull(),df['FinalContribution'],df['AdjContribution'])
        df['FinalContribution'] = np.where((df['InstrumentTypeDescription'] == 'CALL MONEY') ,0,df['FinalContribution'])
        df['FinalContribution'] = np.where((df['InstrumentCode'] == 'ACIF1U') & (df['FinalContribution'] < 0),0,df['FinalContribution'])
        df['FinalContribution'] = np.where((df['InstrumentCode'] == 'AHY2U') & (df['FinalContribution'] < 0),0,df['FinalContribution'])
        df['FinalContribution'] = np.where((df['InstrumentCode'] == 'AIG2U') & (df['FinalContribution'] < 0),0,df['FinalContribution'])
        df['FinalContribution'] = np.where((df['InstrumentCode'] == 'AIRS1U') & (df['FinalContribution'] < 0),0,df['FinalContribution'])
        df['FinalContribution'] = np.where((df['InstrumentCode'] == 'AIRT1U') & (df['FinalContribution'] < 0),0,df['FinalContribution'])
        df['FinalContribution'] = np.where((df['InstrumentTypeDescription'] == 'FUND : MONEY MARKET MUTUAL FUND') & (df['FinalContribution'] < 0),0,df['FinalContribution'])
        # Perfomance df
        df['Spread'] = -df['PrevModifiedDuration']*(df['CurBPSpread'] - df['PrevBPSpread'])/10000*df['Weight']
        # df['Spread'] = np.where(df['InstrumentTypeDescription'] == 'OPTION : BOND FUTURE', df[df.InstrumentCode == 'R2044']['Spread'].values*df['Delta'], df['Spread'] )
        df['Spread'] = df['Spread'].fillna(0)
        df['Convexity'] = df['Weight']*0.5*df['PrevConvexity']*((df['CurMTM'] - df['PrevMTM'])/100)**2
        # df['Convexity'] = np.where(df['InstrumentTypeDescription'] == 'OPTION : BOND FUTURE', df[df.InstrumentCode == 'R2044']['Convexity'].values*df['Delta'], df['Convexity'] )
        df['Convexity'] = df['Convexity'].fillna(0)
        # df['Inflation'] = (df['CurReferenceCPI'] / df['PrevReferenceCPI'] - 1)*df['Weight']
        # df['Inflation'] = cpi_returns*df['Weight']
        df['Inflation'] = np.where(df.InstrumentTypeDescription == 'BOND : CPI LINKED', cpi_returns*df['Weight'],0)
        # df['Inflation'] = np.where(df['InstrumentTypeDescription'] == 'OPTION : BOND FUTURE', df[df.InstrumentCode == 'R2044']['Inflation'].values*df['Delta'], df['Inflation'] )
        df['Inflation'] = df['Inflation'].fillna(0)
        df['Repo'] = np.where((df.InstrumentLongName.str.upper().str[:4] == 'REPO'), df['FinalContribution'], 0)
        df['Repo'] = df['Repo'].fillna(0)
        df['Carry'] = df['PrevMTM']/100*1/365*df['Weight']
        df['Carry'] = np.where((df.InstrumentCode == 'AHY2U') | (df.InstrumentCode == 'AIG2U')|(df.InstrumentCode == 'ACIF1U')|(df.InstrumentTypeDescription == 'FUND : MONEY MARKET MUTUAL FUND')|(df.InstrumentTypeDescription == 'CALL MONEY'), df['FinalContribution'], df['Carry'])
        # df['Carry'] = np.where(df['InstrumentTypeDescription'] == 'OPTION : BOND FUTURE', df[df.InstrumentCode == 'R2044']['Carry'].values*df['Delta'], df['Carry'] )
        df['Carry'] = df['Carry'].fillna(0)
        df['ILBCarry'] = np.where((df.InstrumentTypeDescription.str.upper() == 'BOND : CPI LINKED'), df['Carry'], 0)
        # df['ILBCarry'] = np.where(df['InstrumentTypeDescription'] == 'OPTION : BOND FUTURE', df[df.InstrumentCode == 'R2044']['ILBCarry'].values*df['Delta'], df['ILBCarry'] )
        df['ILBCarry'] = df['ILBCarry'].fillna(0)
        df['NomCarry'] = df['Carry'] - df['ILBCarry']
        df['NomCarry'] = df['NomCarry'].fillna(0)
        df['Return'] = df['FinalContribution'] / df['Weight']
        df['Return'] = df['Return'].fillna(0)
        df['YieldCurve'] = (1+df['FinalContribution']) / ((1 + df['Spread'])*(1 + df['Convexity'])*(1 + df['Inflation'])*(1 + df['NomCarry'])*(1 + df['ILBCarry'])*(1 + df['Repo'])) - 1
        df['Diff'] = (1+df['PercentageChangeGross']/100) / (1+df['FinalContribution'].sum()) - 1
        df['AgrSpread'] = np.log(1 + df['Spread'])
        df['AgrConvexity'] = np.log(1 + df['Convexity'])
        df['AgrInflation'] = np.log(1 + df['Inflation'])
        df['AgrRepo'] = np.log(1 + df['Repo'])
        df['AgrNomCarry'] = np.log(1 + df['NomCarry'])
        df['AgrILBCarry'] = np.log(1 + df['ILBCarry'])
        df['AgrYieldCurve'] = np.log(1 + df['YieldCurve'])
        df['PortfolioReturn'] = np.log(1 + df['FinalContribution'])
        df['AgrReturn'] = np.log(1 + df['Return'])
        df['AgrDiff'] = np.log(1 + df['Diff'])
        df.rename(columns={'PortfolioIDCode': 'Portfolio Code','InstrumentCode': 'Instrument Code'}, inplace=True)				
        pieces.append(df)
    df = pd.concat(pieces, ignore_index=True)
    zzzadj = pd.DataFrame({'PortfolioReturn':df['AgrDiff']}).drop_duplicates()
    zzzadj['Portfolio Code'] = i
    zzzadj['Instrument Code'] = 'zzDUMMY'
    zzzadj['AgrSpread'] = 0.0
    zzzadj['AgrConvexity'] = 0.0
    zzzadj['AgrInflation'] = 0.0
    zzzadj['AgrRepo'] = 0.0
    zzzadj['AgrNomCarry'] = 0.0
    zzzadj['AgrILBCarry'] = 0.0
    zzzadj['AgrReturn'] = 0.0
    zzzadj['AgrYieldCurve'] = zzzadj['PortfolioReturn']
    zzzadj['InstrumentTypeDescription'] = 'DUMMY'
    df = df.append(zzzadj, sort=False)	
    # Handling missing instrument classification
    df['Instrument Type'] = np.where(df['InstrumentTypeDescription'].isnull(), 'UNCLASSIFIED',df['InstrumentTypeDescription'])
    df_w = df.groupby('Instrument Code').Weight.mean().reset_index()
    df_w = df_w.fillna(0)
    summ = df_w.Weight.sum()
    df_summ = pd.DataFrame({'Instrument Code':['Total'],'Weight':[summ]})
    df_w = df_w.append(df_summ, sort=False)	
    df = pd.pivot_table(df,index=['Portfolio Code','Instrument Code','Instrument Type'], values = ['AgrReturn','AgrSpread', 'AgrConvexity', 'AgrInflation', 'AgrNomCarry','AgrILBCarry','AgrRepo','AgrYieldCurve', 'PortfolioReturn'], aggfunc=np.sum, margins = True, margins_name = 'Total').reset_index()
    df = df[['Instrument Code','Portfolio Code','Instrument Type','AgrReturn','AgrSpread', 'AgrConvexity', 'AgrInflation', 'AgrNomCarry','AgrILBCarry','AgrRepo','AgrYieldCurve', 'PortfolioReturn']]
    df.rename(columns={'PortfolioIDCode': 'Portfolio Code','InstrumentCode': 'Instrument Code','AgrReturn': 'Return','AgrSpread': 'Spread','AgrConvexity': 'Convexity', 'AgrInflation': 'Inflation','AgrRepo': 'Repo', 'AgrNomCarry': 'NomCarry', 'AgrILBCarry': 'ILBCarry','AgrYieldCurve': 'Yield Curve', 'PortfolioReturn': 'Contribution'}, inplace=True)
    df['AgrReturn'] = (1 + df['Return']).cumprod()	
    df['AgrSpread'] = (1 + df['Spread']).cumprod()	
    df['AgrConvexity'] = (1 + df['Convexity']).cumprod()	
    df['AgrInflation'] = (1 + df['Inflation']).cumprod()
    df['AgrRepo'] = (1 + df['Repo']).cumprod()	
    df['AgrNomCarry'] = (1 + df['NomCarry']).cumprod()	
    df['AgrILBCarry'] = (1 + df['ILBCarry']).cumprod()	
    df['AgrContribution'] = (1 + df['Contribution']).cumprod()	
    df['Spread'].iloc[-1] = df['AgrSpread'].iloc[-2]-1
    df['Convexity'].iloc[-1] = df['AgrConvexity'].iloc[-2]-1
    df['Inflation'].iloc[-1] = df['AgrInflation'].iloc[-2]-1
    df['Repo'].iloc[-1] = df['AgrRepo'].iloc[-2]-1
    df['NomCarry'].iloc[-1] = df['AgrNomCarry'].iloc[-2]-1
    df['ILBCarry'].iloc[-1] = df['AgrILBCarry'].iloc[-2]-1
    df['Contribution'].iloc[-1] = df['AgrContribution'].iloc[-2]-1
    df['Return'].iloc[-1] = df['Contribution'].iloc[-1]
    df['Yield Curve'].iloc[-1] = df['Contribution'].iloc[-1] - df['Spread'].iloc[-1] - df['Convexity'].iloc[-1] - df['Inflation'].iloc[-1] - df['NomCarry'].iloc[-1] - df['ILBCarry'].iloc[-1] - df['Repo'].iloc[-1]
    df = df[['Instrument Code','Portfolio Code','Instrument Type','Return','Spread', 'Convexity', 'Inflation', 'NomCarry', 'ILBCarry', 'Repo', 'Yield Curve', 'Contribution']]
    df = df.merge(df_w, how='left', on=['Instrument Code'])
    df = df[['Portfolio Code','Instrument Code','Instrument Type','Weight','Return','Spread', 'Convexity', 'Inflation', 'NomCarry', 'ILBCarry', 'Repo', 'Yield Curve', 'Contribution']]
    df['Weight'] = df['Weight'] / df.Weight.sum()
    df['Weight'].iloc[-1] = df.Weight.sum()
    df.rename(columns={'Spread': 'Spread Contribution','Convexity': 'Convexity Contribution', 'Inflation': 'Inflation Contribution','Repo': 'Repo Contribution', 'NomCarry': 'Nominal Carry Contribution', 'ILBCarry': 'Real Carry Contribution','Yield Curve': 'Yield Curve Contribution','Contribution': 'Return Contribution'}, inplace=True)
    df.to_excel(writer, i, index=False)
    workbook  = writer.book
    worksheet = writer.sheets[i]
    percentage_center = workbook.add_format({'num_format': '0.000%', 'align': 'center', 'valign': 'vcenter'})
    left = workbook.add_format({'align': 'left', 'valign': 'vleft'})
    worksheet.set_column('D:M', 12, percentage_center)
    worksheet.set_column('B:B', 16, left)
    worksheet.set_column('C:C', 27, left)
writer.save()