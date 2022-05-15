import pandas as pd
import numpy as np
from datetime import datetime
import os
import pytz

my_dict = {'Egypt-Premier':'https://www.betdevil.com/soccer/competition/Egypt-Premier/136/',
          'Spain-La-Liga':'https://www.betdevil.com/soccer/competition/Spain-La-Liga/13/',
           'Germany-Bundesliga':'https://www.betdevil.com/soccer/competition/Germany-Bundesliga/15/',
           'France-Ligue-1':'https://www.betdevil.com/soccer/competition/France-Ligue-1/11/',
           'Italy-Serie-A':'https://www.betdevil.com/soccer/competition/Italy-Serie-A/12/',
           'Netherlands-Eredivisie':'https://www.betdevil.com/soccer/competition/Netherlands-Eredivisie/14/',
           'Portugal-Primeira-Liga':'https://www.betdevil.com/soccer/competition/Portugal-Primeira-Liga/17/',
           'Russia-Premier':'https://www.betdevil.com/soccer/competition/Russia-Premier/28/',
           'Spain-Primera-RFEF-Group-2':'https://www.betdevil.com/soccer/competition/Spain-Primera-RFEF-Group-2/268/',
           'Argentina-Copa-Liga-Profesional':'https://www.betdevil.com/soccer/competition/Argentina-Copa-Liga-Profesional/823/',
           'Algeria-Ligue-1':'https://www.betdevil.com/soccer/competition/Algeria-Ligue-1/149/',
           'Argentina-Primera':'https://www.betdevil.com/soccer/competition/Argentina-Primera/41/',
           'Argentina-Primera-C-Metropolitana-':'https://www.betdevil.com/soccer/competition/Argentina-Primera-C-Metropolitana-/191/',
           'Australia-New-South-Wales':'https://www.betdevil.com/soccer/competition/Australia-New-South-Wales/177/',
           'Australia-Victoria':'https://www.betdevil.com/soccer/competition/Australia-Victoria/176/',
           'Australia-Western-Australia':'https://www.betdevil.com/soccer/competition/Australia-Western-Australia/174/',
           'Austria-1-Liga':'https://www.betdevil.com/soccer/competition/Austria-1-Liga/36/',
           'Austria-Regionalliga-Mitte':'https://www.betdevil.com/soccer/competition/Austria-Regionalliga-Mitte/121/',
           'Austria-Regionalliga-Ost':'https://www.betdevil.com/soccer/competition/Austria-Regionalliga-Ost/123/',
           'Austria-Regionalliga-West-Salzburg':'https://www.betdevil.com/soccer/competition/Austria-Regionalliga-West-Salzburg/250/',
           'Austria-Regionalliga-West-Tyrol':'https://www.betdevil.com/soccer/competition/Austria-Regionalliga-West-Tyrol/249/',
           'Belgium-Pro-League':'https://www.betdevil.com/soccer/competition/Belgium-Pro-League/18/',
           'Bosnia-Herzegovina-Premier':'https://www.betdevil.com/soccer/competition/Bosnia-Herzegovina-Premier/125/',
           'Brazil-Serie-B':'https://www.betdevil.com/soccer/competition/Brazil-Serie-B/78/',
           'Bulgaria-Parva-Liga':'https://www.betdevil.com/soccer/competition/Bulgaria-Parva-Liga/53/',
           'Chile-Primera-B':'https://www.betdevil.com/soccer/competition/Chile-Primera-B/195/',
           'Croatia-1-HNL':'https://www.betdevil.com/soccer/competition/Croatia-1-HNL/52/',
           'Croatia-2-HNL':'https://www.betdevil.com/soccer/competition/Croatia-2-HNL/200/',
           'Cyprus-Division-1':'https://www.betdevil.com/soccer/competition/Cyprus-Division-1/81/',
           'Czech-FNL':'https://www.betdevil.com/soccer/competition/Czech-FNL/124/',
           'Denmark-Division-1':'https://www.betdevil.com/soccer/competition/Denmark-Division-1/26/',
           'Denmark-Division-2':'https://www.betdevil.com/soccer/competition/Denmark-Division-2/82/',
           'Denmark-Superliga':'https://www.betdevil.com/soccer/competition/Denmark-Superliga/16/',
           'Estonia-Meistriliiga':'https://www.betdevil.com/soccer/competition/Estonia-Meistriliiga/126/',
           'France-National':'https://www.betdevil.com/soccer/competition/France-National/85/',
           'Germany-2-Bundesliga':'https://www.betdevil.com/soccer/competition/Germany-2-Bundesliga/21/',
           'Germany-3-Liga':'https://www.betdevil.com/soccer/competition/Germany-3-Liga/117/',
           'Ghana-Premier':'https://www.betdevil.com/soccer/competition/Ghana-Premier/204/',
           'Iceland-Urvalsdeild':'https://www.betdevil.com/soccer/competition/Iceland-Urvalsdeild/44/',
           'Ireland-First-Division':'https://www.betdevil.com/soccer/competition/Ireland-First-Division/10/',
           'Ireland-Premier':'https://www.betdevil.com/soccer/competition/Ireland-Premier/9/',
           'Italy-Serie-B':'https://www.betdevil.com/soccer/competition/Italy-Serie-B/22/',
           'Japan-J-League':'https://www.betdevil.com/soccer/competition/Japan-J-League/46/',
           'Jordan-League':'https://www.betdevil.com/soccer/competition/Jordan-League/157/',
           'Kenya-Premier':'https://www.betdevil.com/soccer/competition/Kenya-Premier/203/',
           'Korea-K3-League':'https://www.betdevil.com/soccer/competition/Korea-K3-League/262/',
           'Latvia-Virsliga':'https://www.betdevil.com/soccer/competition/Latvia-Virsliga/108/',
           'Libya-Premier':'https://www.betdevil.com/soccer/competition/Libya-Premier/230/',
           'Malaysia-Super':'https://www.betdevil.com/soccer/competition/Malaysia-Super/158/',
           'Mali-Premiere':'https://www.betdevil.com/soccer/competition/Mali-Premiere/238/',
           'Morocco-GNF-1':'https://www.betdevil.com/soccer/competition/Morocco-GNF-1/140/',
           'Netherlands-Eerste-Divisie':'https://www.betdevil.com/soccer/competition/Netherlands-Eerste-Divisie/35/',
           'Oman-Elite-League':'https://www.betdevil.com/soccer/competition/Oman-Elite-League/141/',
           'Poland-Ekstraklasa':'https://www.betdevil.com/soccer/competition/Poland-Ekstraklasa/33/',
           'Poland-I-Liga':'https://www.betdevil.com/soccer/competition/Poland-I-Liga/106/',
           'Russia-FNL':'https://www.betdevil.com/soccer/competition/Russia-FNL/104/',
           'Saudi-Arabia-Pro-League':'https://www.betdevil.com/soccer/competition/Saudi-Arabia-Pro-League/142/',
           'Seychelles-Division-One':'https://www.betdevil.com/soccer/competition/Seychelles-Division-One/236/',
           'Singapore-Premier-League':'https://www.betdevil.com/soccer/competition/Singapore-Premier-League/51/',
           'Slovakia-2-Liga':'https://www.betdevil.com/soccer/competition/Slovakia-2-Liga/134/',
           'Slovenia-1-SNL':'https://www.betdevil.com/soccer/competition/Slovenia-1-SNL/40/',
           'South-Africa-Premier':'https://www.betdevil.com/soccer/competition/South-Africa-Premier/132/',
           'Spain-Segunda':'https://www.betdevil.com/soccer/competition/Spain-Segunda/24/',
           'Sudan-Premier':'https://www.betdevil.com/soccer/competition/Sudan-Premier/221/',
           'Sweden-Div-1-North':'https://www.betdevil.com/soccer/competition/Sweden-Div-1-North/102/',
           'Sweden-Div-1-South':'https://www.betdevil.com/soccer/competition/Sweden-Div-1-South/103/',
           'Switzerland-Challenge':'https://www.betdevil.com/soccer/competition/Switzerland-Challenge/48/',
           'Turkey-Super-Lig':'https://www.betdevil.com/soccer/competition/Turkey-Super-Lig/37/',
           'UAE-Arabian-Gulf-League':'https://www.betdevil.com/soccer/competition/UAE-Arabian-Gulf-League/143/',
           'Uganda-Premier':'https://www.betdevil.com/soccer/competition/Uganda-Premier/207/',
           'Uruguay-Primera':'https://www.betdevil.com/soccer/competition/Uruguay-Primera/71/',
           'Uzbekistan-Super-League':'https://www.betdevil.com/soccer/competition/Uzbekistan-Super-League/243/',
           'Venezuela-Primera':'https://www.betdevil.com/soccer/competition/Venezuela-Primera/114/',
           'Zimbabwe-Premier':'https://www.betdevil.com/soccer/competition/Zimbabwe-Premier/218/'
          }
		  
		  
		  

df1 = pd.DataFrame()
for link,fund in zip(my_dict.values(),my_dict.keys()):
    # print(fund)
    df = pd.read_html(link)
    df[15].rename(columns=df[15].iloc[0], inplace=True)
    df[15].drop(df[15].index[0], inplace=True)
    df[15].dropna(axis=1, inplace=True)
    df[15] = df[15].rename(columns={'All':'ALL'})
    df[15] = df[15].rename(columns={df[15].columns[0]:'Position','ALL':'Team'})
    df[15].iloc[:,2:] = df[15].iloc[:,2:].astype(float)
    df[15]['A_Ave'] = df[15]['A']/df[15]['P']
    df[15]['HA_Ave'] = df[15]['HA']/df[15]['HP']
    df[15]['AA_Ave'] = df[15]['AA']/df[15]['AP']
    df[15]['F_Ave'] = df[15]['F']/df[15]['P']
    df[15]['HF_Ave'] = df[15]['HF']/df[15]['HP']
    df[15]['AF_Ave'] = df[15]['AF']/df[15]['AP']
    df[15]['League_W %'] = df[15]['W'].sum()/df[15]['P'].sum()*100
    df[15]['League_D %'] = df[15]['D'].sum()/df[15]['P'].sum()*100
    df[15]['League_L %'] = df[15]['L'].sum()/df[15]['P'].sum()*100  
    df[15]['MaxGame'] = (len(df[15])-1)*2
    df[15]['CompletionRate %'] = round(df[15]['P']/((df[15]['Position'].max()-1)*2)*100,1)
    df[15]['Position %'] = df[15]['Position']/len(df[15])*100
    df[15]['League'] = fund
    df[15]['Date'] = pd.to_datetime(datetime.today()).strftime('%Y-%m-%d')
    
    # Get next matches
    df[14].rename(columns=df[14].iloc[0], inplace=True)
    df[14].drop(df[14].index[0], inplace=True)
    df[14] = df[14].rename(columns={'Date':'NextMatchDate'})
    df[14] = df[14][['Home Team','Away Team','NextMatchDate']]
    df[14] = df[14][['Home Team','NextMatchDate']].append(df[14][['Away Team','NextMatchDate']].rename(columns={'Away Team':'Home Team'}), ignore_index=True)
    df[14]['Date'] = pd.to_datetime(datetime.now()).strftime('%Y-%m-%d %H:%M')
    df[14]['NextMatchDate'] = pd.to_datetime('2022 ' + df[14]['NextMatchDate'], format='%Y %d %b %H:%M')
    df[14]= df[14][df[14]['NextMatchDate'] >= df[14]['Date'].iloc[0]]

    df[15] = pd.merge(df[15], df[14][['Home Team','NextMatchDate']], how='left', left_on=['Team'], right_on=['Home Team'])
    df[15].drop(['Home Team'], axis=1, inplace=True)
    df[15].sort_values(by=['League','Team','NextMatchDate'],ascending=[True,True,True], inplace=True)
    df[15].drop_duplicates(['League','Team'], keep='first', inplace=True)
    
    df1 = df1.append(df[15])
    
df1.to_csv(os.path.join(r'C:\Users\LENOVO\Desktop\soccer_analysis\input', df1['Date'].iloc[0] + '_betdevil.csv'), sep=';', index=False)



# get last results
my_path = r'C:\Users\LENOVO\Desktop\soccer_analysis\input'
df = pd.DataFrame()
for filename in os.listdir(my_path):
    df2 = pd.read_csv(os.path.join(my_path,filename), sep=';')
    df = df.append(df2)
    df['Date'] = pd.to_datetime(df['Date'])
    
df = pd.pivot_table(df, values='Pts', index=['League','Team','Date','P','F','A']).reset_index().sort_values(by=['League','Team','Date'],ascending=[True,True,False])

df['P_Change'] = np.where(df['Team'] == df['Team'].shift(-1),df['P'] - df['P'].shift(-1),0)
df['Score'] = np.where(df['Team'] == df['Team'].shift(-1),df['Pts'] - df['Pts'].shift(-1),0)

df3 = df.copy()
df4 = df.copy()

def my_results(x):
    if x == 3:
        y = 'W'
    elif x == 1:
        y ='D'
    else:
        y ='L'
    return y

df["Results"] = np.where(df['P_Change'] !=0, df.apply(lambda x: my_results(x['Score']), axis=1),0)
df = df[df['Results'] !=0]

df = df.sort_values(by=['League','Team','Date'],ascending=[True,True,False])
df.drop_duplicates(['League','Team'], keep='first', inplace=True)

df2 = df1.merge(df[['League','Team','Results']], on=['League','Team'], how='left')



# Previous goals
df3['Previous_F_Goals'] = np.where(df3['Team'] == df3['Team'].shift(-1),df3['F'] - df3['F'].shift(-1),0)
df3['Previous_A_Goals'] = np.where(df3['Team'] == df3['Team'].shift(-1),df3['A'] - df3['A'].shift(-1),0)
df3 = df3[df3['P_Change'] != 0]
df3 = df3[['League','Team','Previous_F_Goals','Previous_A_Goals']]



# Cumulative goals for previous 5 games
df4['Cum_F_Goals'] = np.where(df4['Team'] == df4['Team'].shift(-1),df4['F'] - df4['F'].shift(-1),0)
df4['Cum_F_Freq'] = np.where(df4['Cum_F_Goals'] == 0, 0, 1)
df4['Cum_F_Freq'] = np.where(df4['Team'] == df4['Team'].shift(-1),df4['Cum_F_Freq'] + df4['Cum_F_Freq'].shift(-1),0)
df4['Cum_F_Goals'] = np.where(df4['Team'] == df4['Team'].shift(-1),df4['Cum_F_Goals'] + df4['Cum_F_Goals'].shift(-1),0)


df4['Cum_A_Goals'] = np.where(df4['Team'] == df4['Team'].shift(-1),df4['A'] - df4['A'].shift(-1),0)
df4['Cum_A_Freq'] = np.where(df4['Cum_A_Goals'] == 0, 0, 1)
df4['Cum_A_Freq'] = np.where(df4['Team'] == df4['Team'].shift(-1),df4['Cum_A_Freq'] + df4['Cum_A_Freq'].shift(-1),0)
df4['Cum_A_Goals'] = np.where(df4['Team'] == df4['Team'].shift(-1),df4['Cum_A_Goals'] + df4['Cum_A_Goals'].shift(-1),0)

df4 = df4[df4['P_Change'] != 0]

df4 = df4[['League','Team','Cum_F_Goals','Cum_A_Goals','Cum_F_Freq','Cum_A_Freq']]


df2 = df2.merge(df3, on=['League','Team'], how='left')
df2 = df2.merge(df4, on=['League','Team'], how='left')


df2.to_csv(r'C:\Users\LENOVO\Desktop\soccer_analysis\input\input_betdevil.csv', sep=';', index=False)