"""
This script reads a CSV of time series data, and displays any notable deviations
of manually-selected columns from the average value of those columns.
This display is done in a graph, with an 'error' column added.
"""
import pandas as pd
from os import path
import matplotlib.pyplot as plt
import numpy as np


csv_file_name = 'last_test_alberto.csv'  # The name of the file we want to read.
# Read in data.
data_path = path.join('data', csv_file_name)
cleaned_data_path = path.join('data', f'cleaned-{csv_file_name}')
df = pd.read_csv(data_path)

list_of_column_names = list(df.columns)
df_no_empty_rows = df.dropna(axis=0, how='all', subset=list_of_column_names[1:])
# axis = 0 = rows. how='all' = drop when all empty, subset = all columns except for time
# Data is only measured on the minutes. This has the effect of removing the 20 and 40 second rows.
data = df_no_empty_rows.set_index('Time')  # Reassign for brevity later, and to set our index to Time.

columns=['ceph-gw4.gridpp.rl.ac.uk', 'ceph-gw5.gridpp.rl.ac.uk'] #List column names of your cleaned csv-file data

# data_path = path.join('data', 'cleaned-last_test_alberto.csv') #Get the csv-file. <Mika: from average_series.py>
# data = pd.read_csv(data_path, delimiter=',', index_col=0) #Read a comma-separated values (csv) file into DataFrame.

# Get rid of columns that are flat i.e. time series where values are all 1's for example.
for col in data.columns[:-1]: #Iterate cols except time col.
    if col in columns and data[col].sum()/data.shape[0] <1:
        columns.remove(col)

data = data[columns]
data_rolling = data.rolling(50, min_periods=1, center=True).mean()
data_rolling['average'] = data_rolling.mean(numeric_only=True, axis=1)  # Calculate moving average of timeseries.

data_rolling['errors']=[0]*data.shape[0]  # Initialise error rows with zeros.
small=0.0001  # Avoid division by 0.
for col in data_rolling.columns[:-1]:  # Iterate cols except time col.
    relative_distance=np.abs((data_rolling[col]- data_rolling['average'])/(data_rolling['average'] + small))  # Calculate the relative distance fom th mean
    data_rolling['errors'] = (data_rolling['errors']) | (relative_distance>0.25).astype('int')  # Add the error to the table. Fine-tune the number relative_distance is relative to.

data_rolling.plot(logy=False)
plt.show()