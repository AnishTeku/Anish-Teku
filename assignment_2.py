# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 12:25:45 2023

@author: anish
"""

#Importing necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#read_file function to read csv files
def read_file(file_path):
    '''
    Creates DataFrame of given filepath

    Parameters
    ----------
    file_path : STR
        File path of our csv file.

    Returns
    -------
    dataframe : DataFrame
        Dataframe created with given csv file.

    '''
    dataframe = pd.read_csv(file_path, skiprows=(4))

    return dataframe


#transpose_dfs to create transpose of given data
def transpose_dfs(dataframe):
    '''
    Creates transpose dataframe of given dataframe

    Parameters
    ----------
    dataframe : DataFrame
        Dataframe for which transpose to be found.

    Returns
    -------
    dataframe : DataFrame
        Given dataframe.
    dataframe_tr : TYPE
        Transpose of given dataframe.

    '''
    dataframe_tr = pd.DataFrame.transpose(dataframe)
    dataframe_tr.columns = dataframe['Country Name']
    dataframe_tr = dataframe_tr.iloc[1:, :]
    dataframe.index = dataframe['Country Name']

    return dataframe, dataframe_tr


#bar_plot to plot data over multiple columns as bars
def bar_plot(my_data, ylabel, title):
    '''
    Plots a barplot of data over multiple columns

    Parameters
    ----------
    my_data : DataFrame
        Dataframe for which barplot to be plotted.
    ylabel : STR
        Plot y-axis label as string.
    title : STR
        Plot title as string.

    Returns
    -------
    fig : Figure
        Plot saved as fig.

    '''
    fig = plt.figure()
    width = 0.8/len(my_data.columns)
    offset = width/2
    ax = plt.subplot()
    for index, year in enumerate(my_data.columns):
        ax.bar([ln+offset+width*index for ln in range(len(my_data.index))],
               my_data[year], width=width, label=year)
    ax.set_xticks([j+0.4 for j in range(len(my_data.index))])
    ax.set_xticklabels(my_data.index, rotation=65)

    ax.set_xlabel('Country Name')
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend(title='Years', bbox_to_anchor=(1, 1))
    plt.savefig(title+'.png', bbox_inches='tight', dpi=400)
    plt.show()

    return fig


#country to create dataframe of a specific country
def country(my_dataframes, labels, country_name):
    '''
    Creates new dataframe where all data from my_dataframes of my country 
    will be in it from index 1990 to 2019

    Parameters
    ----------
    my_dataframes : List
        List of dataframes of world bank where countries are given as columns.
    labels : List
        List of string values used as column names of my new dataframe.
    country_name : STR
        Country fow which data to be extracted.

    Returns
    -------
    country : DataFrame
        Dataframe with my country data from all given dataframes from year 
        1990 to 2019.

    '''
    country = pd.DataFrame()
    for i in range(len(my_dataframes)):
        country[labels[i]] = my_dataframes[i].loc['1990':'2019', country_name]

    return country


#correlation_heatmap to produce correlation heatmap
def correlation_heatmap(country_data, country, color):
    '''
    Plots a heatmap of given data correlation of its columns

    Parameters
    ----------
    country_data : DataFrame
         Dataframe from which heatmap is produced.
    country : STR
        Country name as string.
    color : STR
        cmap value as sring.

    Returns
    -------
    fig : Figure
        Plot saved as figure.

    '''

    for i in country_data.columns:
        country_data[i] = country_data[i].astype(dtype=np.int64)
    corr = country_data.corr().to_numpy()

    print('Correlation Coefficient matrix of ', country, ' is:')
    print(corr, '\n')

    fig = plt.subplots(figsize=(8, 8))
    plt.imshow(corr, cmap=color, interpolation='nearest')
    plt.colorbar(orientation='vertical', fraction=0.05)

    #To show ticks and label them with appropriate names of columns
    plt.xticks(range(len(country_data.columns)),
               country_data.columns, rotation=45, fontsize=15)
    plt.yticks(range(len(country_data.columns)),
               country_data.columns, rotation=0, fontsize=15)

    #To create text annotations and display correlation coefficient in plot
    for i in range(len(country_data.columns)):
        for j in range(len(country_data.columns)):
            plt.text(i, j, corr[i, j].round(2),
                     ha="center", va="center", color='black')
    plt.title(country)
    plt.savefig(country+'.png', bbox_inches='tight', dpi=300)
    plt.show()

    return fig


#I randomly chose these countries for which analysis is proceeded
countries = ['Australia', 'Brazil', 'China',
             'United Kingdom', 'India', 'Japan', 'Mexico',
             'United States']
print('Countries for which analysis is proceeded:')
print(countries, '\n')


#Reading Agricultural land data and creating its transpose
agri_land = read_file('Agriculture_Land_Area.csv')
agri_land, agri_land_tr = transpose_dfs(agri_land)

#Slicing data to limit data to my countries
agri = agri_land_tr.loc['1961':'2021', countries]

#Plotting Agricultural land area variation of my countries
plt.figure()
#Values are divided by a million to get data in millions
for i in agri.columns:
    plt.plot(agri.index, agri[i]/1000000, label=i, linestyle='--')
plt.legend(title='Country', bbox_to_anchor=(1, 1))
plt.xlabel('Year')
plt.ylabel('Agricultural land area in M sq-KM')
plt.title('AGRICULTURAL LAND AREA VARIATION OF COUNTRIES OVER YEARS')
plt.xticks(agri.index[::10])
plt.savefig('Agricultural_land_area.png', bbox_inches='tight', dpi=300)
plt.show()

#Selecting few years from 2000 to 2019
years = ['2000', '2005', '2010', '2015', '2019']
agri = agri_land.loc[countries, years]
print('Agricultural Land data description of years of few countries:')
print(agri.describe(), '\n')

#Values are plotted in Millions
for i in agri.columns:
    agri[i] = agri[i]/1000000

#Plotting Agricultural land area variation of my countries in given years
bar_plot(agri, 'Agricultural Land in Million sq Km', 'AGRICULTURAL LAND')


#Reading CO2 emissions in kt per capita data and creating its transpose
co2_mt = read_file('CO2_mt_per_capita.csv')
co2_mt, co2_mt_tr = transpose_dfs(co2_mt)

co2 = co2_mt.loc[countries, years]
print('CO2 Emissions data description of years of few countries:')
print(co2.describe(), '\n')

#Plotting CO2 emission variation of my countries in given years
bar_plot(co2, 'CO2 emission in kt', 'CO2 EMISSIONS IN kt PER CAPITA')

#Reading GDP data and creating its transpose
gdp_usd = read_file('GDP_USD.csv')
gdp_usd, gdp_usd_tr = transpose_dfs(gdp_usd)

gdp = gdp_usd.loc[countries, years]
print('GDP data description of years of few countries:')
print(gdp.describe(), '\n')

#Since GDP value is so high, converted its value into Trillions
for i in years:
    gdp[i] = gdp[i]/1000000000000

#Plotting GDP variation of my countries in given years
bar_plot(gdp, 'GDP in Trillion USD $', 'GDP')

#Plotting GDP history of my countries in Trillions
gdp = gdp_usd_tr.loc['1961':'2021', countries]
plt.figure()
for i in gdp.columns:
    plt.plot(gdp.index, gdp[i]/1000000000000, label=i)
plt.legend(title='Country', bbox_to_anchor=(1, 1))
plt.xlabel('Year')
plt.ylabel('GDP in Trillion USD')
plt.xticks(gdp.index[::10])
plt.title('GDP GROWTH OF COUNTRIES OVER YEARS')
plt.savefig('GDP_variation.png', bbox_inches='tight', dpi=300)
plt.show()

#Reading Labour Force data and creating its transpose
lab_force = read_file('Labour_Force_Total.csv')
lab_force, lab_force_tr = transpose_dfs(lab_force)

labour = lab_force.loc[countries, years]
print('Labour Force data description of years of few countries:')
print(labour.describe(), '\n')

#Labour Force population values are converted to Millions
for i in years:
    labour[i] = labour[i]/1000000

#Plotting Labour force varion of my countries in given years
bar_plot(labour, 'Labour population in Millions', 'LABOUR FORCE IN TOTAL')

#Reading Population Total and creating its transpose
population_total = read_file('POP_Total.csv')
population_total, population_total_tr = transpose_dfs(population_total)

population = population_total.loc[countries, years]
print('Total Population data description of years of few countries:')
print(population.describe(), '\n')

#Converting Population Total values into Millions
for i in years:
    population[i] = population[i]/1000000

#Plotting Population Total variation of my countries in given years
bar_plot(population, 'Population in Millions', 'TOTAL POPULATION')

#Creating list of indicator names and its dataframes to create country
#specific data and do further analysis
indicators = ['Agricultural Land', 'CO2 Emissions', 'GDP', 'Labor Force',
              'Population Total']
dataframes = [agri_land, co2_mt, gdp_usd, lab_force, population_total]
dataframes_tr = [agri_land_tr, co2_mt_tr, gdp_usd_tr, lab_force_tr,
                 population_total_tr]

'''
By looking at previous plots, for United States, China and Brazil I felt 
there exists a small relation between the indicators that are used to plot 
bargraphs above.
So created seperate datasets of these countries and produced heatmap of its 
correlation coefficients
'''

#Creating United States dataframe and plotting its heatmap
us = country(dataframes_tr, indicators, 'United States')
correlation_heatmap(us, 'UNITED STATES', 'rainbow')

#Creating China dataframe and plotting its heatmap
china = country(dataframes_tr, indicators, 'China')
correlation_heatmap(china, 'CHINA', 'jet')

#Creating Brazil dataframe and plotting its heatmap
brazil = country(dataframes_tr, indicators, 'Brazil')
correlation_heatmap(brazil, 'BRAZIL', 'ocean_r')

#Correlation heatmaps of other countries (commented)

# uk=country(dataframes_tr,indicators,'United Kingdom')
# correlation_heatmap(uk,'UNITED KINGDOM','jet')

# india=country(dataframes_tr,indicators,'India')
# correlation_heatmap(india,'INDIA','jet')

# italy=country(dataframes_tr,indicators,'Italy')
# correlation_heatmap(italy,'ITALY','jet')

# japan=country(dataframes_tr,indicators,'Japan')
# correlation_heatmap(japan,'JAPAN','jet')

# mexico=country(dataframes_tr,indicators,'Mexico')
# correlation_heatmap(mexico,'MEXICO','jet')

# australia=country(dataframes_tr, indicators, 'Australia')
# correlation_heatmap(australia, 'AUSTRALIA', 'jet')

'''
Seeing at the variations and correlations of our countries, further analysis 
is done to find the impact on whole world.
'''

co2_emissions = read_file('co2_emissions.csv')
co2_emissions, co2_emissions_tr = transpose_dfs(co2_emissions)
co2_e = co2_emissions_tr.loc['1990':'2019', ['World', 'Australia', 'Brazil',
                                             'China', 'United Kingdom',
                                             'India', 'Japan', 'Mexico',
                                             'United States']]
co2_pct_world = pd.DataFrame()
for i in countries:
    co2_pct_world[i] = (co2_e[i]/co2_e['World'])*100
    co2_pct_world[i] = co2_pct_world[i].astype(float)

print('CO2 Emissions impact on world data description:')
print(co2_pct_world.describe(), '\n')

#Plotting CO2 emissions % of World
plt.figure(figsize=(5, 4))
for i in co2_pct_world.columns:
    plt.plot(co2_pct_world.index, co2_pct_world[i], label=i, linestyle='--')
plt.legend(title='Country', bbox_to_anchor=(1, 1))
plt.xlabel('Year')
plt.ylabel('%o CO2 emission of country in the world')
plt.title('IMPACT OF CO2 EMISSIONS OF COUNTRY IN THE WORLD')
plt.xticks(co2_pct_world.index[::4])
plt.savefig('%impact.png', bbox_inches='tight', dpi=400)
plt.show()

#Finding skewness and Kurtosis of the CO2 emissions impact data
skewness = []
for i in countries:
    skewness.append(co2_pct_world[i].skew())
kurtosis = []
for i in countries:
    kurtosis.append(co2_pct_world[i].kurtosis())

skew_kurt = pd.DataFrame()
skew_kurt.index = countries
skew_kurt['Skewness'] = skewness
skew_kurt['Kurtosis'] = kurtosis
#skew_kurt.to_csv('skewness&kurtosis_of_co2_emissions.csv')
print(skew_kurt)
