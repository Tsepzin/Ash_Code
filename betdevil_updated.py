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
           'Zimbabwe-Premier':'https://www.betdevil.com/soccer/competition/Zimbabwe-Premier/218/',
           'Spain-Primera-RFEF-Group-1':'http://www.betdevil.com/soccer/competition/Spain-Primera-RFEF-Group-1/267/',
           'Spain-Segunda-RFEF-Group-1':'https://www.betdevil.com/soccer/competition/Spain-Segunda-RFEF-Group-1/269/',
           'Spain-Segunda-RFEF-Group-2':'https://www.betdevil.com/soccer/competition/Spain-Segunda-RFEF-Group-2/270/',
           '':'https://www.betdevil.com/soccer/competition/Spain-Segunda-RFEF-Group-3/271/',
           'Spain-Segunda-RFEF-Group-4':'https://www.betdevil.com/soccer/competition/Spain-Segunda-RFEF-Group-4/272/',
           'Spain-Segunda-RFEF-Group-5':'https://www.betdevil.com/soccer/competition/Spain-Segunda-RFEF-Group-5/273/',
           'England-Premier':'https://www.betdevil.com/soccer/competition/England-Premier/1/',
           'England-Championship':'http://www.betdevil.com/soccer/competition/England-Championship/2/',
           'England-League-1':'http://www.betdevil.com/soccer/competition/England-League-1/3/',
           'England-League-2':'http://www.betdevil.com/soccer/competition/England-League-2/4/',
           'Scotland-Premiership':'http://www.betdevil.com/soccer/competition/Scotland-Premiership/5/',
           'Scotland-Championship':'http://www.betdevil.com/soccer/competition/Scotland-Championship/6/',
           'Scotland-League-1':'http://www.betdevil.com/soccer/competition/Scotland-League-1/7/',
           'Scotland-League-2':'http://www.betdevil.com/soccer/competition/Scotland-League-2/8/',
           'Sweden-Allsvenskan':'http://www.betdevil.com/soccer/competition/Sweden-Allsvenskan/19/',
           'Norway-Eliteserien':'http://www.betdevil.com/soccer/competition/Norway-Eliteserien/20/',
           'France-Ligue-2':'http://www.betdevil.com/soccer/competition/France-Ligue-2/23/',
           'Norway-1-Division':'http://www.betdevil.com/soccer/competition/Norway-1-Division/25/',
           'Sweden-Superettan':'http://www.betdevil.com/soccer/competition/Sweden-Superettan/27/',
           'Finland-Veikkausliig':'http://www.betdevil.com/soccer/competition/Finland-Veikkausliiga/29/',
           'England-National-League':'https://www.betdevil.com/soccer/competition/England-National-League/30/',
           'Greece-Super-League':'http://www.betdevil.com/soccer/competition/Greece-Super-League/31/',
           'Austria-Bundesliga':'http://www.betdevil.com/soccer/competition/Austria-Bundesliga/32/',
           'Finland-Ykkonen':'http://www.betdevil.com/soccer/competition/Finland-Ykkonen/34/',
           'Ukraine-Premier':'http://www.betdevil.com/soccer/competition/Ukraine-Premier/38/',
           'Czech-Liga':'http://www.betdevil.com/soccer/competition/Czech-Liga/39/',
           'Brazil-Serie-A':'http://www.betdevil.com/soccer/competition/Brazil-Serie-A/42/',
           'Mexico-Liga-MX':'http://www.betdevil.com/soccer/competition/Mexico-Liga-MX/43/',
           'USA-MLS':'http://www.betdevil.com/soccer/competition/USA-MLS/45/',
           'Swiss%20Super%20League':'http://www.betdevil.com/soccer/competition/Swiss%20Super%20League/47/',
           'Serbia-Super-Liga':'http://www.betdevil.com/soccer/competition/Serbia-Super-Liga/49/',
           'Serbia-Prva-Liga':'https://www.betdevil.com/soccer/competition/Serbia-Prva-Liga/50/',
           'Romania-Liga-I':'https://www.betdevil.com/soccer/competition/Romania-Liga-I/54/',
           'Slovakia-Super-Liga':'http://www.betdevil.com/soccer/competition/Slovakia-Super-Liga/57/',
           'Hungary-NB-I':'http://www.betdevil.com/soccer/competition/Hungary-NB-I/58/',
           'Belgium-Division-2':'http://www.betdevil.com/soccer/competition/Belgium-Division-2/59/',
           'Greece-Football-League':'http://www.betdevil.com/soccer/competition/Greece-Football-League/60/',
           'Turkey-1.-Lig-':'http://www.betdevil.com/soccer/competition/Turkey-1.-Lig-/61/',
           'Portugal-Liga-de-Honra':'http://www.betdevil.com/soccer/competition/Portugal-Liga-de-Honra/62/',
           'Italy-Lega-Pro-1-A':'http://www.betdevil.com/soccer/competition/Italy-Lega-Pro-1-A/63/',
           'Italy-Lega-Pro-1-B':'http://www.betdevil.com/soccer/competition/Italy-Lega-Pro-1-B/64/',
           'China-Super-League':'http://www.betdevil.com/soccer/competition/China-Super-League/65/',
           'Israel%20Premier%20League':'http://www.betdevil.com/soccer/competition/Israel%20Premier%20League/66/',
           'Northern-Ireland-Premier':'http://www.betdevil.com/soccer/competition/Northern-Ireland-Premier/67/',
           'Chile-Primera':'http://www.betdevil.com/soccer/competition/Chile-Primera/68/',
           'Wales-Premier':'http://www.betdevil.com/soccer/competition/Wales-Premier/69/',
           'Australia-A-League':'http://www.betdevil.com/soccer/competition/Australia-A-League/70/',
           'Peru%20Primera':'http://www.betdevil.com/soccer/competition/Peru%20Primera/72/',
           'England-National-League-North':'https://www.betdevil.com/soccer/competition/England-National-League-North/73/',
           'England-National-League-South':'https://www.betdevil.com/soccer/competition/England-National-League-South/74/',
           'England-Southern-Central':'https://www.betdevil.com/soccer/competition/England-Southern-Central/197/',
           'England-Isthmian-League':'http://www.betdevil.com/soccer/competition/England-Isthmian-League/76/',
           'England-Northern-League':'http://www.betdevil.com/soccer/competition/England-Northern-League/77/',
           'Brazil-Paulista':'http://www.betdevil.com/soccer/competition/Brazil-Paulista/79/',
           'Brazil-Carioca':'http://www.betdevil.com/soccer/competition/Brazil-Carioca/80/',
           'Denmark-Division-2-East':'http://www.betdevil.com/soccer/competition/Denmark-Division-2-East/83/',
           'Denmark-Division-2':'https://www.betdevil.com/soccer/competition/Denmark-Division-2/82/',
           'Spain-Segunda-B-Group-1':'https://www.betdevil.com/soccer/competition/Spain-Segunda-B-Group-1/86/',
           'Spain-Segunda-B-Group-2':'https://www.betdevil.com/soccer/competition/Spain-Segunda-B-Group-2/87/',
           'Spain-Segunda-B-Group-3':'https://www.betdevil.com/soccer/competition/Spain-Segunda-B-Group-3/88/',
           'Spain-Segunda-B-Group-4':'https://www.betdevil.com/soccer/competition/Spain-Segunda-B-Group-4/89/',
           'Israel-Liga-Leumit':'http://www.betdevil.com/soccer/competition/Israel-Liga-Leumit/90/',
           'Finland-Kakkonen-North':'http://www.betdevil.com/soccer/competition/Finland-Kakkonen-North/91/',
           'Belarus-Premier':'http://www.betdevil.com/soccer/competition/Belarus-Premier/133/',
           'Costa-Rica-Primera':'http://www.betdevil.com/soccer/competition/Costa-Rica-Primera/131/',
           'India-ILeague':'http://www.betdevil.com/soccer/competition/India-ILeague/137/',
           'Macedonia-1st':'http://www.betdevil.com/soccer/competition/Macedonia-1st/138/',
           'Malta-Premier':'http://www.betdevil.com/soccer/competition/Malta-Premier/144/',
           'Iran-Persian-Gulf':'http://www.betdevil.com/soccer/competition/Iran-Persian-Gulf/146/',
           'Montenegro-First-League':'http://www.betdevil.com/soccer/competition/Montenegro-First-League/147/',
           'Kuwait-Premier/':'http://www.betdevil.com/soccer/competition/Kuwait-Premier/148/',
           'Hong-Kong-Premier-League':'https://www.betdevil.com/soccer/competition/Hong-Kong-Premier-League/150/',
           'Indonesia-Liga-1':'http://www.betdevil.com/soccer/competition/Indonesia-Liga-1/151/',
           'Albania-Superliga':'http://www.betdevil.com/soccer/competition/Albania-Superliga/153/',
           'Azerbaijan-Premyer-Liqa':'http://www.betdevil.com/soccer/competition/Azerbaijan-Premyer-Liqa/154/',
           'Bahrain-Premier':'http://www.betdevil.com/soccer/competition/Bahrain-Premier/155/',
           'Georgia-Umaglesi':'http://www.betdevil.com/soccer/competition/Georgia-Umaglesi/156/',
           'Syria-Premier':'http://www.betdevil.com/soccer/competition/Syria-Premier/159/',
           'Thailand-Premier':'http://www.betdevil.com/soccer/competition/Thailand-Premier/160/',
           'Germany-Regionalliga-Bayern':'http://www.betdevil.com/soccer/competition/Germany-Regionalliga-Bayern/161/',
           'Germany-Regionalliga-Sudwest':'http://www.betdevil.com/soccer/competition/Germany-Regionalliga-Sudwest/162/',
           'Germany-Regionalliga-Nordost':'http://www.betdevil.com/soccer/competition/Germany-Regionalliga-Nordost/163/',
           'Faroe%20Islands%20Premier':'http://www.betdevil.com/soccer/competition/Faroe%20Islands%20Premier/164/',
           'Vietnam-V-League-1':'http://www.betdevil.com/soccer/competition/Vietnam-V-League-1/165/',
           'Philippines-PFL':'https://www.betdevil.com/soccer/competition/Philippines-PFL/166/',
           'Tunisia-Ligue-1':'http://www.betdevil.com/soccer/competition/Tunisia-Ligue-1/167/',
           'Moldova-Divizia-Nationala':'http://www.betdevil.com/soccer/competition/Moldova-Divizia-Nationala/168/',
           'Japan-J3-League':'http://www.betdevil.com/soccer/competition/Japan-J3-League/169/',
           'Korea-League-2':'https://www.betdevil.com/soccer/competition/Korea-League-2/170/',
           'Australia-Queensland':'https://www.betdevil.com/soccer/competition/Australia-Queensland/172/',
           'Australia-South-Australia':'https://www.betdevil.com/soccer/competition/Australia-South-Australia/173/',
           'Australia-Tasmania':'https://www.betdevil.com/soccer/competition/Australia-Tasmania/178/',
           'Australia-Northern-New-South-Wales':'https://www.betdevil.com/soccer/competition/Australia-Northern-New-South-Wales/179/',
           'Italy-Lega-Pro-1-C':'http://www.betdevil.com/soccer/competition/Italy-Lega-Pro-1-C/180/',
           'USA-USL':'https://www.betdevil.com/soccer/competition/USA-USL/182/',
           'Slovakia-2-Liga-East':'http://www.betdevil.com/soccer/competition/Slovakia-2-Liga-East/183/',
           'Denmark-Division-2-Group-1':'http://www.betdevil.com/soccer/competition/Denmark-Division-2-Group-1/185/',
           'Denmark-Division-2-Group-2':'http://www.betdevil.com/soccer/competition/Denmark-Division-2-Group-2/186/',
           'Brazil-Serie-C':'https://www.betdevil.com/soccer/competition/Brazil-Serie-C/193/',
           'Bulgaria-Vtora-Liga':'https://www.betdevil.com/soccer/competition/Bulgaria-Vtora-Liga/194/',
           'Estonia-Esiliiga':'https://www.betdevil.com/soccer/competition/Estonia-Esiliiga/201/',
           'Iceland-1-Deild':'https://www.betdevil.com/soccer/competition/Iceland-1-Deild/202/',
           'Zambia-Super':'https://www.betdevil.com/soccer/competition/Zambia-Super/205/',
           'Nigeria-NPFL':'https://www.betdevil.com/soccer/competition/Nigeria-NPFL/206/',
           'Tanzania-Ligi-Kuu-Bara':'https://www.betdevil.com/soccer/competition/Tanzania-Ligi-Kuu-Bara/208/',
           'Rwanda-NFL':'https://www.betdevil.com/soccer/competition/Rwanda-NFL/209/',
           'South-Africa-Division-1':'https://www.betdevil.com/soccer/competition/South-Africa-Division-1/210/',
           'Cameroon-Elite-ONE':'https://www.betdevil.com/soccer/competition/Cameroon-Elite-ONE/211/',
           'Senegal-Ligue-1':'https://www.betdevil.com/soccer/competition/Senegal-Ligue-1/212/',
           'Ethiopia-Premier':'https://www.betdevil.com/soccer/competition/Ethiopia-Premier/213/',
           'Gambia-GFA':'https://www.betdevil.com/soccer/competition/Gambia-GFA/214/',
           'Algeria-Ligue-2':'https://www.betdevil.com/soccer/competition/Algeria-Ligue-2/215/',
           'Angola-Girabola':'https://www.betdevil.com/soccer/competition/Angola-Girabola/216/',
           'Congo-DR-Super':'https://www.betdevil.com/soccer/competition/Congo-DR-Super/217/',
           'Guinea-Ligue-1':'https://www.betdevil.com/soccer/competition/Guinea-Ligue-1/219/',
           'Ivory-Coast-Ligue-1':'https://www.betdevil.com/soccer/competition/Ivory-Coast-Ligue-1/220/',
           'Burkina-Faso-Premier':'https://www.betdevil.com/soccer/competition/Burkina-Faso-Premier/222/',
           'Congo-Ligue-1':'https://www.betdevil.com/soccer/competition/Congo-Ligue-1/223/',
           'Botswana-Premier':'https://www.betdevil.com/soccer/competition/Botswana-Premier/224/',
           'Burundi-Ligue-A':'https://www.betdevil.com/soccer/competition/Burundi-Ligue-A/225/',
           'Djibouti-Division-1':'https://www.betdevil.com/soccer/competition/Djibouti-Division-1/226/',
           'Gabon-Championnat-D1':'https://www.betdevil.com/soccer/competition/Gabon-Championnat-D1/227/',
           'Lesotho-Premier':'https://www.betdevil.com/soccer/competition/Lesotho-Premier/228/',
           'Malawi-Super':'https://www.betdevil.com/soccer/competition/Malawi-Super/231/',
           'Mauritania-Super':'https://www.betdevil.com/soccer/competition/Mauritania-Super/232/',
           'Mozambique-Mocambola':'https://www.betdevil.com/soccer/competition/Mozambique-Mocambola/233/',
           'Niger-Ligue-1':'https://www.betdevil.com/soccer/competition/Niger-Ligue-1/235/',
           'El-Salvador-Primera':'https://www.betdevil.com/soccer/competition/El-Salvador-Primera/240/',
           'Kosovo-Liga-Superliga':'https://www.betdevil.com/soccer/competition/Kosovo-Liga-Superliga/242/',
           'Iraq-Super-League':'https://www.betdevil.com/soccer/competition/Iraq-Super-League/244/',
           'Palestine-West-Bank-League':'https://www.betdevil.com/soccer/competition/Palestine-West-Bank-League/245/',
           'USA-USL-WC':'https://www.betdevil.com/soccer/competition/USA-USL-WC/247/',
           'Canada-Premier-League':'https://www.betdevil.com/soccer/competition/Canada-Premier-League/248/',
           'Austria-Regionalliga-West-Vorarlberg':'https://www.betdevil.com/soccer/competition/Austria-Regionalliga-West-Vorarlberg/251/',
           'Argentina-Primera-Nacional-B':'https://www.betdevil.com/soccer/competition/Argentina-Primera-Nacional-B/253/',
           'Tajikistan-Vysshaya-Liga':'https://www.betdevil.com/soccer/competition/Tajikistan-Vysshaya-Liga/256/',
           'Somalia-Championship':'https://www.betdevil.com/soccer/competition/Somalia-Championship/257/',
           'Myanmar-National-League':'https://www.betdevil.com/soccer/competition/Myanmar-National-League/258/',
           'Taiwan-Premier-League':'https://www.betdevil.com/soccer/competition/Taiwan-Premier-League/259/',
           'Belarus-Pershaya-Liga':'https://www.betdevil.com/soccer/competition/Belarus-Pershaya-Liga/260/',
           'Turkmenistan-Yokary-Liga':'https://www.betdevil.com/soccer/competition/Turkmenistan-Yokary-Liga/261/',
           'Faroe-Islands-1.-Deild':'http://www.betdevil.com/soccer/competition/Faroe-Islands-1.-Deild/263/',
           'Armenia-Premier-League':'https://www.betdevil.com/soccer/competition/Armenia-Premier-League/264/',
           'Kazakhstan-Premier-League':'https://www.betdevil.com/soccer/competition/Kazakhstan-Premier-League/265/',
           'Spain-Segunda-B-Group-5':'https://www.betdevil.com/soccer/competition/Spain-Segunda-B-Group-5/266/',
           'Greece-Super-League-2-North':'https://www.betdevil.com/soccer/competition/Greece-Super-League-2-North/274/',
           'Greece-Super-League-2-South':'http://www.betdevil.com/soccer/competition/Greece-Super-League-2-South/275/',
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