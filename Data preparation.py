# General exploration and check of datasets
## Importing pandas to read and process datasets
import pandas as pd

## Loading the datasets
happiness_2019 = pd.read_csv('2019.csv') ### Contains happiness scores by country
GDP_2023 = pd.read_csv('Country.csv', skiprows=4) ### Contains GDP score by country
metadata = pd.read_csv('Metadata_Country.csv') ### provides general country information like geographic region, income group, and country code

## visualizing frist rows for each dataset
happiness_2019.head()
GDP_2023.head()
metadata.head() ### happiness_2019 is clean, so it won't be necessary for now

## Data cleaning
### Deleting unecessary columns from 'GDP_2023'
cols_to_delete = list(GDP_2023.columns[2:46]) + list(GDP_2023.columns[64:69]) #deletes from 1961 to 2001 and 2020 to 2023.
GDP_2023 = GDP_2023.drop(cols_to_delete, axis = 1)
GDP_2023.head()

### Deleting unecessary columns from 'metadata'
metadata = metadata.drop([metadata.columns[5], metadata.columns[3]], axis = 1)
metadata = metadata.rename(columns = {'TableName':'Country Name'}) # renaming 'TableName' as 'Country Name' to match with GDP_2023 dataset
metadata.head()

## checking for null values in 'metadata'
metadata[metadata.isnull().any(axis=1)] # prints all rows where there is at least one missing value
# almost all rows that contain a missing value are for regions instead of countries (except for Venezuela), 
# the main problem with this is that they aren't linked to any country, so these rows are useless and must be deleted.

## Deleting region rows in 'metadata'
metadata = metadata[~metadata['Region'].isnull()].reset_index(drop = True) #keeps all rows which have no missing value

## checking for null values by column in 'metadata'
metadata.isnull().sum() # only the Income Group from Venezuela is missing

## Visualizing rows with null or empty values in 'GDP_2023' dataset
GDP_2023[GDP_2023.isnull().any(axis=1)] #

## Merging datasets
### Since 'metadata' only contains country codes, applying an inner join will remove non-matching rows from 'GDP_2023', effectively filtering out regions.
GDP_metadata = GDP_2023.merge(metadata, on = 'Country Code', how = 'inner')
GDP_metadata.head()

## refining little details about column names and order
GDP_metadata['Country Name_x'] = GDP_metadata['Country Name_y'] # Replacing country names from with the metadata's 'Country Name' for standardization purposes
GDP_metadata = GDP_metadata.drop(columns = ['Country Name_y']) # deleting 'Country Name_y'
GDP_metadata = GDP_metadata.rename(columns={'Country Name_x':'Country Name'}) # renaming the country name column
### Ordering columns to have information first and GDP at last
GDP_metadata = GDP_metadata[['Country Name', 'Country Code', 'Region', 'IncomeGroup'] + list(GDP_metadata.columns[2:20])]
GDP_metadata.head()

## Dealing with null values in 'GDP_metadata'
GDP_metadata.isnull().sum() # null values by columns
GDP_metadata['null_count'] = GDP_metadata[GDP_metadata.columns[4:24]].isnull().sum(axis=1) # counting empty rows by country
GDP_metadata[['Country Name', 'Region',
              'IncomeGroup', 'null_count']][GDP_metadata['null_count'] >= 1].sort_values('null_count', ascending = True) # visualizing countries with empty rows
### after manual exploration of these countries in the original file, it was decided to keep countries with less than 5 missing values
GDP_metadata = GDP_metadata[GDP_metadata['null_count'] < 5] # deleting rows with more than 5 missing values
GDP_metadata = GDP_metadata.drop(columns = ['null_count']) # droping the null_count column
GDP_metadata.head() # visualizing first 5 rows of the data

## Pivoting the data
# transforming from wide to long format
GDP_metadata_long = pd.melt(GDP_metadata, id_vars = list(GDP_metadata.columns[0:4]), var_name = 'Year', value_name = 'GDP')
GDP_metadata_long.head()

# Cayman Islands, Channel Islands, and Yemen will have their null values imputed through different methods:
#  1.Cayman Islands will requiere rear projection to fill the empty values at the beginning of the temporal period
#  2.Channel Islands needs a interpolation (from year 2007 and 2009) to fill the 2008 value.
#  3.Yemen will have imputed values by a moving average

## delimiting the dataset for each country
### creates a boolean object (True or False) to select rows where the country coincides with the search pattern
cayman_islands = GDP_metadata_long['Country Name'] == 'Cayman Islands'
channel_islands = GDP_metadata_long['Country Name'] == 'Channel Islands'
yemen = GDP_metadata_long['Country Name'] == 'Yemen, Rep.'

## imputing values
GDP_metadata_long.loc[cayman_islands, 'GDP'] = GDP_metadata_long.loc[cayman_islands, 'GDP'].bfill() #fills with next value
GDP_metadata_long.loc[channel_islands, 'GDP'] = GDP_metadata_long.loc[channel_islands, 'GDP'].interpolate()
GDP_metadata_long.loc[yemen, 'GDP'] = GDP_metadata_long.loc[yemen, 'GDP'].fillna(GDP_metadata_long.loc[yemen, 'GDP']\
.rolling(window = 4, min_periods = 1).mean()) # applies a moving average

##checking for null values
GDP_metadata_long[GDP_metadata_long['Country Name'].isin(['Cayman Islands', 'Channel Islands', 'Yemen, Rep.'])].isna().sum()

## visualizing GDP tendency from these countries
import matplotlib.pyplot as plt
import seaborn as sns

### creating the graph
plt.figure(figsize = (15,8))

sns.lineplot(data=GDP_metadata_long[GDP_metadata_long['Country Name'].isin(['Cayman Islands','Channel Islands','Yemen, Rep.' ])
                                   ], x = 'Year', y = 'GDP', hue = 'Country Name', marker = 'o')
plt.title("GDP's evolution from 2002 to 2019")
plt.ylabel('GDP')
plt.xlabel('Years')
plt.tight_layout()
plt.show()

## Saving the dataset as a csv file
GDP_metadata_long.to_csv('GDP_metadata_long.csv', index=False)
