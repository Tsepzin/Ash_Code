import shutil, os
from my_functions import custom_dates as cd

# Instrument Data
if os.path.exists(os.path.join(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\instrument_data\input\archive',cd.t)) == False:
	os.mkdir(os.path.join(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\instrument_data\input\archive',cd.t)) # create path

source = os.listdir(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\instrument_data\input')
destination = os.path.join(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\instrument_data\input\archive',cd.t)
for files in source:
	if files.endswith('.csv'):
		os.chdir(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\\Python\take_on\instrument_data\input')
		shutil.copy(files,destination)

# IR Sensitivity Reports
if os.path.exists(os.path.join(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\reports\ir_sensitivity\archive',cd.t)) == False:
	os.mkdir(os.path.join(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\reports\ir_sensitivity\archive',cd.t)) # create path
	
source = os.listdir(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\reports\ir_sensitivity')
destination = os.path.join(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\reports\ir_sensitivity\archive',cd.t)
for files in source:
	if files.endswith('.csv'):
		os.chdir(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\reports\ir_sensitivity')
		shutil.copy(files,destination)
		
for files in source:
	if files.endswith('.xlsx'):
		os.chdir(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Python\take_on\reports\ir_sensitivity')
		shutil.move(files,destination)
		

		
		
