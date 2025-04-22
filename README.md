# 2019-Happiness-data-analysis
This project explores global data to uncover patterns that help explain the happiness of the people around the world, using three datasets:
1. '2019': contains data from the 2019 happiness index covering the following variables: freedom to make life choices, GDP per capita, Social Support, healthy life expectancy, generosity, and perceptions of corruptions
2. 'Country': Includes total GDP for each country and region of the world from 1961 to 2023
3. 'metadata': provides general information from all the countries listed in the 'Country' dataset, including the income group, geographic region, and country code.

Before the analysis, a data cleaning process was performed on the 'metadata' and 'Country' datasets to remove rows corresponding to regions rather than individual countries, which cannot be used in the analysis, and rows with excessive missing values values. Aditionally, the data was pivoted to facilitate different visualizations and then values from countries with 4 or less missing values were imputed through bfill(), extrapolation, and moving average.
