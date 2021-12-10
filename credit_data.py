import pandas as pd

writer = pd.ExcelWriter(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\reports\credit\out\Transactions_AHY2U.xlsx')
writer1 = pd.ExcelWriter(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\reports\credit\out\Month-end Holdings_AHY2U.xlsx')
writer2 = pd.ExcelWriter(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\reports\credit\out\Total Holdings_AHY2U.xlsx')
df = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\reports\credit\in\holdings.xlsx', sheet_name='holdings')
col = df.columns.values
nav = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\reports\credit\in\Daily_NAV_Values_AHY2U.xlsx', usecols=[0,1])
nav2 = pd.DataFrame(pd.date_range(start=nav['Date'].min(),end=nav['Date'].max()), columns=['Date']  )
nav2 = nav2.merge(nav, how='left', on=['Date'])
nav2 = nav2.ffill(axis ='rows') 
nav2.to_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\reports\credit\out\Daily_NAV_Values_AHY2U.xlsx', index=False)

mv = pd.DataFrame(columns=['NAV date','MV', 'Fund Name'])

for i in range(2,len(col)):
    print(col[i])
    data = df[['Date','NAV date',col[i]]]
    data = data.dropna()
    data.sort_values(by=['NAV date'], ascending=True, inplace=True)
    data.to_excel(writer, col[i], index=False)
    
    # per = data['NAV date'].dt.to_period("M")
    # g = data.groupby(per).sum()
    # g = g.reset_index()
    # g.drop(['AHY2U Daily NAV values'], axis=1, inplace=True)
    # g.sort_values(by=['NAV date'], ascending=True, inplace=True)
    # g['MV'] = g[col[i]].cumsum(axis=0)
    # g.drop([col[i]], axis=1, inplace=True)
    # g['Fund Name'] = col[i]
    # mv = mv.append(g)
    # g.to_excel(writer1, col[i], index=False)

# mv = pd.pivot_table(mv,index=['NAV date'], columns=['Fund Name'], values = ['MV'], aggfunc=np.sum, margins = True, margins_name = 'Total').reset_index()
# mv = mv.drop(mv.index[len(mv)-1])
# mv.to_excel(writer2, index=True)
    
writer.save()
# writer1.save()
# writer2.save()