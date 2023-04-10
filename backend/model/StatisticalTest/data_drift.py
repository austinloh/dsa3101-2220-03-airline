import numpy as np
import pandas as pd
from scipy.stats import ks_2samp
from scipy.stats import chi2_contingency

# Load the reference data
ref_data = pd.read_csv('../../database/data/2008.csv.bz2', compression='bz2')

# Load the new data
new_data = pd.read_csv('../../database/data/old/1987.csv')

#data preprocessing
ref_data.drop(['Year', 'DepTime', 'ArrTime', 'FlightNum', 'ActualElapsedTime', 'ArrDelay', 'DepDelay', 'AirTime', \
         'TaxiIn', 'TaxiOut', 'Cancelled', 'CancellationCode', 'Diverted','CarrierDelay', 'WeatherDelay', \
         'NASDelay', 'SecurityDelay', 'LateAircraftDelay'], axis=1, inplace=True)
ref_data.dropna(inplace=True)

# Separate numerical and categorical data
ref_numeric_data = ref_data.select_dtypes(include=[np.number])
ref_cat_data = ref_data.select_dtypes(exclude=[np.number])
new_numeric_data = new_data.select_dtypes(include=[np.number])
new_cat_data = new_data.select_dtypes(exclude=[np.number])

# Perform KS test for numerical data
num_ks_stats = []
for col in ref_numeric_data.columns:
    if col in new_numeric_data.columns:
        ks_statistic, p_value = ks_2samp(ref_numeric_data[col], new_numeric_data[col])
        num_ks_stats.append(p_value)

# Define a function to perform a chi-square test for a single column
def chi_square_test(col1, col2):
    contingency_table = pd.crosstab(col1, col2)
    chi2, p_value, dof, expected = chi2_contingency(contingency_table)
    return p_value

# Perform chi-square tests for all categorical columns
p_values = []
for col in ref_cat_data.columns:
    if col in new_cat_data.columns:
        p_value = chi_square_test(ref_data[col], new_data[col])
        p_values.append(p_value)

# Combine results for numerical and categorical data
ks_stats = np.concatenate((num_ks_stats, p_values), axis=None)

# Set the significance level
alpha = 0.05

# Compare the p-values with the significance level
if np.any(ks_stats < alpha):
    print('Warning: Data drift detected')
else:
    print('No data drift detected')
