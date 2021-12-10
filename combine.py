import pandas as pd 

df = pd.read_csv(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\instrument_data\input\zero_coupon.csv', usecols=['InstrumentCode','InstrumentLongName','InstrumentTypeDescription','shift_100d','shift_75d','shift_50d','shift_25d','shift_25u','shift_50u','shift_75u','shift_100u'])

df_temp = pd.read_csv(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\instrument_data\input\t_bill.csv', usecols=['InstrumentCode','InstrumentLongName','InstrumentTypeDescription','shift_100d','shift_75d','shift_50d','shift_25d','shift_25u','shift_50u','shift_75u','shift_100u'])
df = df.append(df_temp)

df_temp = pd.read_csv(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\instrument_data\input\promissory_notes.csv', usecols=['InstrumentCode','InstrumentLongName','InstrumentTypeDescription','shift_100d','shift_75d','shift_50d','shift_25d','shift_25u','shift_50u','shift_75u','shift_100u'])
df = df.append(df_temp)

df_temp = pd.read_csv(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\instrument_data\input\ncd.csv', usecols=['InstrumentCode','InstrumentLongName','InstrumentTypeDescription','shift_100d','shift_75d','shift_50d','shift_25d','shift_25u','shift_50u','shift_75u','shift_100u'])
df = df.append(df_temp)

df_temp = pd.read_csv(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\instrument_data\input\commercial_paper.csv', usecols=['InstrumentCode','InstrumentLongName','InstrumentTypeDescription','shift_100d','shift_75d','shift_50d','shift_25d','shift_25u','shift_50u','shift_75u','shift_100u'])
df = df.append(df_temp)

df_temp = pd.read_csv(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\instrument_data\input\listed_frb.csv', usecols=['InstrumentCode','InstrumentLongName','InstrumentTypeDescription','shift_100d','shift_75d','shift_50d','shift_25d','shift_25u','shift_50u','shift_75u','shift_100u'])
df = df.append(df_temp)

df_temp = pd.read_csv(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\instrument_data\input\fixed_coupon_cd.csv', usecols=['InstrumentCode','InstrumentLongName','InstrumentTypeDescription','shift_100d','shift_75d','shift_50d','shift_25d','shift_25u','shift_50u','shift_75u','shift_100u'])
df = df.append(df_temp)

df_temp = pd.read_csv(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\instrument_data\input\listed_frn.csv', usecols=['InstrumentCode','InstrumentLongName','InstrumentTypeDescription','shift_100d','shift_75d','shift_50d','shift_25d','shift_25u','shift_50u','shift_75u','shift_100u'])
df = df.append(df_temp)

df_temp = pd.read_csv(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\instrument_data\input\stepped_rate_note.csv', usecols=['InstrumentCode','InstrumentLongName','InstrumentTypeDescription','shift_100d','shift_75d','shift_50d','shift_25d','shift_25u','shift_50u','shift_75u','shift_100u'])
df = df.append(df_temp)

df_temp = pd.read_csv(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\instrument_data\input\zero_shocks.csv', usecols=['InstrumentCode','InstrumentLongName','InstrumentTypeDescription','shift_100d','shift_75d','shift_50d','shift_25d','shift_25u','shift_50u','shift_75u','shift_100u'])
df = df.append(df_temp)

df_temp = pd.read_csv(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\instrument_data\input\foreign_bond_vlin.csv', usecols=['InstrumentCode','InstrumentLongName','InstrumentTypeDescription','shift_100d','shift_75d','shift_50d','shift_25d','shift_25u','shift_50u','shift_75u','shift_100u'])
df = df.append(df_temp)

df_temp = pd.read_csv(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\instrument_data\input\unlisted_interest_rate_note.csv', usecols=['InstrumentCode','InstrumentLongName','InstrumentTypeDescription','shift_100d','shift_75d','shift_50d','shift_25d','shift_25u','shift_50u','shift_75u','shift_100u'])
df = df.append(df_temp)

df_temp = pd.read_csv(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\instrument_data\input\unlisted_frn.csv', usecols=['InstrumentCode','InstrumentLongName','InstrumentTypeDescription','shift_100d','shift_75d','shift_50d','shift_25d','shift_25u','shift_50u','shift_75u','shift_100u'])
df = df.append(df_temp)

df_temp = pd.read_csv(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\instrument_data\input\cpi_bonds.csv', usecols=['InstrumentCode','InstrumentLongName','InstrumentTypeDescription','shift_100d','shift_75d','shift_50d','shift_25d','shift_25u','shift_50u','shift_75u','shift_100u'])
df = df.append(df_temp)

df.to_csv(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\instrument_data\input\combine.csv',index=False)