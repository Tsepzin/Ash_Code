import pandas as pd

dates = pd.date_range('2019-11-01','2019-12-31')

pieces = []

for date in dates:
    path = 'Z:/Investment Analytics/Python/take_on/reports/liability_models/gilbx15/gilbx15_' + str(date.date()) + '.csv'
    frame = pd.read_csv(path)
    frame['date'] = date
    pieces.append(frame)
    
# Concatenate everything into a single DataFrame
df = pd.concat(pieces, ignore_index=True)