import pandas as pd
import odbc
import numpy as np
import datetime
from my_functions import custom_dates as cd

writer = pd.ExcelWriter(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\config\returns_pivot_table.xlsx')

df = pd.read_excel(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\config\returns.xlsx')

df['pf_gross_return'] = df['pf_gross_return']/100
df['active_return']=df.pf_gross_return - df.bm_return/100

df_abs = pd.pivot_table(df,index=['date'], columns=['fund_name'], values = ['pf_gross_return']).reset_index()

df_abs.to_excel(writer, 'absolute', index=True)

df_alpha = pd.pivot_table(df,index=['date'], columns=['fund_name'], values = ['active_return']).reset_index()

df_alpha.to_excel(writer, 'alpha', index=True)

writer.save()