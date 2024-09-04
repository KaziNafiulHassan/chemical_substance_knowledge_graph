import pandas as pd

# Load the datasets
chemical_data = pd.read_csv('/home/hassank/Documents/Personal Projects/Chemical_Substance_Knowledge_Graph/Data/01_chemical_data.csv') # Change this path to the location of your dataset
exposure_data = pd.read_csv('/home/hassank/Documents/Personal Projects/Chemical_Substance_Knowledge_Graph/Data/03_exposure_data_measured.csv') # Change this path to the location of your dataset
hazard_data = pd.read_csv('/home/hassank/Documents/Personal Projects/Chemical_Substance_Knowledge_Graph/Data/05_hazard_data.csv') # Change this path to the location of your dataset

# Display the first few rows of each dataframe to understand their structure
print(chemical_data.head())
print(exposure_data.head())
print(hazard_data.head())

# Check for missing values and data types
print(chemical_data.info())

# Drop columns by index (if needed)
chemical_data = chemical_data.drop(chemical_data.columns[[8, 9, 10]], axis=1)

# Verify that the columns have been dropped
print(chemical_data.info())


# Fill missing values with 'NA' if needed
chemical_data = chemical_data.fillna('NA')
exposure_data = exposure_data.fillna('NA')
hazard_data = hazard_data.fillna('NA')

# Verify that there are no missing values left
print(chemical_data.isnull().sum())
print(exposure_data.isnull().sum())
print(hazard_data.isnull().sum())

# Normalize the IDs by stripping any leading/trailing whitespace, converting to uppercase, etc.
chemical_data['Norman_SusDat_ID'] = chemical_data['Norman_SusDat_ID'].str.strip().str.upper()
exposure_data['NORMAN_SusDat_ID'] = exposure_data['NORMAN_SusDat_ID'].str.strip().str.upper()

# Ensure consistency in chemical names (for demonstration, assuming they're the same across datasets)
chemical_data['Name'] = chemical_data['Name'].str.strip().str.lower()

print(chemical_data.head())
print(exposure_data.head())
print(hazard_data.head())