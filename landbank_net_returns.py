import pandas as pd
import odbc
import numpy as np
import datetime

date_str_end = input('Enter end date (Format dd/mm/yyyy):')
format_str = '%d/%m/%Y' # The format
datetime_obj_end = str(datetime.datetime.strptime(date_str_end, format_str).date())

df = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\config\landbank_returns.xlsx')
df['date'] = pd.to_datetime(df['date'])
df = df[df.date <= datetime_obj_end]

df['Report Date'] = datetime_obj_end

# Fund Performance
df['fund_ytd'] = (np.prod(df.pf_net_return.iloc[-df['date'].max().month:]/100+1)-1)*100
df['fund_1_m'] = df.pf_net_return.iloc[-1]
df['fund_3_m'] = (np.prod(df.pf_net_return.iloc[-3:]/100+1)-1)*100
df['fund_6_m'] = (np.prod(df.pf_net_return.iloc[-6:]/100+1)-1)*100
df['fund_9_m'] = (np.prod(df.pf_net_return.iloc[-9:]/100+1)-1)*100
df['fund_1_y'] = (np.prod(df.pf_net_return.iloc[-12:]/100+1)-1)*100
df['fund_3_y'] = (np.prod(df.pf_net_return.iloc[-36:]/100+1)**(12/36)-1)*100
df['fund_5_y'] = np.where(len(df['date']) == 60, (np.prod(df.pf_net_return.iloc[-60:]/100+1)-1)*100,'')
df['fund_SI'] = (np.prod(df.pf_net_return/100+1)**(12/len(df['date']))-1)*100

# STeFI Call Performance
df['stefi_call_ytd'] = (np.prod(df.stefi_call.iloc[-df['date'].max().month:]/100+1)-1)*100
df['stefi_call_1_m'] = df.stefi_call .iloc[-1]
df['stefi_call_3_m'] = (np.prod(df.stefi_call .iloc[-3:]/100+1)-1)*100
df['stefi_call_6_m'] = (np.prod(df.stefi_call .iloc[-6:]/100+1)-1)*100
df['stefi_call_9_m'] = (np.prod(df.stefi_call .iloc[-9:]/100+1)-1)*100
df['stefi_call_1_y'] = (np.prod(df.stefi_call .iloc[-12:]/100+1)-1)*100
df['stefi_call_3_y'] = (np.prod(df.stefi_call .iloc[-36:]/100+1)**(12/36)-1)*100
df['stefi_call_5_y'] = np.where(len(df['date']) == 60, (np.prod(df.stefi_call .iloc[-60:]/100+1)-1)*100,'')
df['stefi_call_SI'] = (np.prod(df.stefi_call /100+1)**(12/len(df['date']))-1)*100

# STeFI Composite Performance
df['stefi_comp_ytd'] = (np.prod(df.stefi_comp.iloc[-df['date'].max().month:]/100+1)-1)*100
df['stefi_comp_1_m'] = df.stefi_comp .iloc[-1]
df['stefi_comp_3_m'] = (np.prod(df.stefi_comp .iloc[-3:]/100+1)-1)*100
df['stefi_comp_6_m'] = (np.prod(df.stefi_comp .iloc[-6:]/100+1)-1)*100
df['stefi_comp_9_m'] = (np.prod(df.stefi_comp .iloc[-9:]/100+1)-1)*100
df['stefi_comp_1_y'] = (np.prod(df.stefi_comp .iloc[-12:]/100+1)-1)*100
df['stefi_comp_3_y'] = (np.prod(df.stefi_comp .iloc[-36:]/100+1)**(12/36)-1)*100
df['stefi_comp_5_y'] = np.where(len(df['date']) == 60, (np.prod(df.stefi_comp .iloc[-60:]/100+1)-1)*100,'')
df['stefi_comp_SI'] = (np.prod(df.stefi_comp /100+1)**(12/len(df['date']))-1)*100

df = df[df['date'] == datetime_obj_end]

df.to_csv(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\reports\landbank_net_returns\output_data\net_returns_' + datetime_obj_end + '.csv', index=False)