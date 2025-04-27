# 2019-Happiness-data-analysis
This project explores global data to uncover patterns that help explain the happiness of the people around the world, using three datasets:
1. '2019': contains data from the 2019 happiness index covering the following variables: freedom to make life choices, GDP per capita, Social Support, healthy life expectancy, generosity, and perceptions of corruptions
2. 'Country': Includes total GDP for each country and region of the world from 1961 to 2023
3. 'metadata': provides general information from all the countries listed in the 'Country' dataset, including the income group, geographic region, and country code.

Before the analysis, a data cleaning process was performed on the 'metadata' and 'Country' datasets to remove rows corresponding to regions rather than individual countries, which cannot be used in the analysis, and rows with excessive missing values values. Aditionally, the data was pivoted to facilitate different visualizations and then values from countries with 4 or less missing values were imputed through bfill(), extrapolation, and moving average.

# Conclusions
The happiness seems to have a strong and positive relationship with the GDP, therefore, the happiness is higher in high-income countries than in low-income ones.
Also, the income is segmented into geographic regions: Sub-Saharan Africa has the most countries in the low and lower middle income group, while Europe & Central Asia, Latin America & Caribbean, and North America are predominantly High and upper middle income countries; lastly, East Asia contains similar number of countries among high and middle income groups, and South Asia has 6 countries mainly in the lower middle group.

On the other hand, the perception of corruption is higher in countries with high incomes, followed by low, lower middle and upper middle. in East Asia and pacific, the high income countries have way higer perceptions of corruption than Lower middle and upper middle; In Europe and Central Asiathe lower income percieves more corruption than high income and upper middle. This patterns repeat on the rest of geographic regions except for Sub-Saharan Africa in which the Low income countries percieved the most corruption.
In general, the higher the income the higher the corruption perception, that's why the top three of this measure by region is formed by North America, East Asia and Pacific, and Europe and Central Asia, which are high or middle income group regions.

Lastly, this behaviour is similar to a healthy life expectancy
