# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 12:25:45 2023

@author: anish
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 

def read_file(file_path):
    data=pd.read_csv(file_path,skiprows=(4))
    
    return data

def transpose_dfs(data):
    data_tr=pd.DataFrame.transpose(data)
    data_tr.columns=data['Country Name']
    data_tr=data_tr.iloc[1:,:]
    data.index=data['Country Name']
    
    return data, data_tr

def bar_plot(data,lab_title):
    fig=plt.figure()
    width=0.8/len(data.columns)
    offset=width/2
    ax=plt.subplot()
    for index,year in enumerate(data.columns):
        ax.bar([ln+offset+width*index for ln in range(len(data.index))],
               data[year],width=width,label=year)
    ax.set_xticks([j+0.4 for j in range(len(data.index))])  
    ax.set_xticklabels(data.index,rotation=65)

    ax.set_xlabel('Country Name')
    ax.set_ylabel(lab_title[0])
    ax.set_title(lab_title[1])
    ax.legend(title='Years', bbox_to_anchor=(1,1))
    plt.savefig(lab_title[1]+'.png',bbox_inches='tight', dpi=400)
    plt.show()

      
def country(datas,labels,country_name):
    country=pd.DataFrame()
    for i in range(len(datas)):
        country[labels[i]]=datas[i].loc['1990':'2019',country_name]
        
    return country

def correlation_heatmap(data,country,color):
    
    for i in data.columns:
        data[i]=data[i].astype(dtype=np.int64)
    corr=data.corr().to_numpy()
    
    fig = plt.subplots(figsize=(8,8))
    plt.imshow(corr,cmap=color, interpolation='nearest')
    plt.colorbar(orientation='vertical', fraction = 0.05)

    #To show ticks and label them with appropriate names of columns
    plt.xticks(range(len(data.columns)),data.columns, rotation=45, fontsize=15)
    plt.yticks(range(len(data.columns)),data.columns, rotation=0, fontsize=15)

    #To create text annotations and display correlation coefficient in plot
    for i in range(len(data.columns)):
        for j in range(len(data.columns)):
            plt.text(i,j, corr[i, j].round(2),
                           ha="center", va="center", color='black')
    plt.title(country)
    plt.show()


countries=['Australia','Brazil','China',
           'United Kingdom','India','Japan','Mexico',
           'United States']
years=['2000','2005','2010','2015','2019']


#Agricultural land

agri_land=read_file('Agriculture_Land_Area.csv')

agri_land,agri_land_tr=transpose_dfs(agri_land)

agri=agri_land_tr.loc['1961':'2021',countries]

plt.figure()
for i in agri.columns:
    plt.plot(agri.index,agri[i]/1000000,label=i)
plt.legend()
plt.xticks(agri.index[::10])
plt.show()
lab_title=['Agricultural Land in Million sq Km','AGRICULTURAL LAND']

agri=agri_land.loc[countries,years]
print('Agricultural Land data description of years of few countries:')
print(agri.describe())
for i in agri.columns:
    agri[i]=agri[i]/1000000
bar_plot(agri,lab_title)


#CO2 emissions in kt per capita
co2_mt=read_file('CO2_mt_per_capita.csv')

co2_mt,co2_mt_tr=transpose_dfs(co2_mt)

co2=co2_mt.loc[countries,years]
print('CO2 Emissions data description of years of few countries:')
print(co2.describe())

lab_title=['CO2 emission in kt','CO2 EMISSIONS IN kt PER CAPITA']
bar_plot(co2,lab_title)

#GDP_USD
gdp_usd=read_file('GDP_USD.csv')

gdp_usd,gdp_usd_tr=transpose_dfs(gdp_usd)

gdp=gdp_usd.loc[countries,years]

print('GDP data description of years of few countries:')
print(gdp.describe(),'\n')

#Since GDP value is so high, converted its value into Million Millions
for i in years:
    gdp[i]=gdp[i]/1000000000000
lab_title=['GDP in MM USD $','GDP']
bar_plot(gdp,lab_title)

gdp=gdp_usd_tr.loc['1961':'2021',countries]

plt.figure()
for i in gdp.columns:
    plt.plot(gdp.index,gdp[i]/1000000,label=i)
plt.legend()
plt.xticks(gdp.index[::10])
plt.show()

#Labour Force 
lab_force=read_file('Labour_Force_Total.csv')

lab_force,lab_force_tr=transpose_dfs(lab_force)

labour=lab_force.loc[countries,years]
print('Labour Force data description of years of few countries:')
print(labour.describe(),'\n')

for i in years:
    labour[i]=labour[i]/1000000
lab_title=['Labour population in Millions','LABOUR FORCE IN TOTAL']
bar_plot(labour,lab_title)


#Total population
population_total=read_file('POP_Total.csv')

population_total,population_total_tr=transpose_dfs(population_total)

population=population_total.loc[countries,years]
print('Total Population data description of years of few countries:')
print(population.describe(), '\n')

for i in years:
    population[i]=population[i]/1000000
lab_title=['Population in Millions','TOTAL POPULATION']
bar_plot(population,lab_title)

indicators=['Agricultural Land','CO2 Emissions','GDP','Labour Force',
            'Population Total']
dataframes=[agri_land,co2_mt,gdp_usd,lab_force,population_total]
dataframes_tr=[agri_land_tr,co2_mt_tr,gdp_usd_tr,lab_force_tr,
               population_total_tr]





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

us=country(dataframes_tr,indicators,'United States')
correlation_heatmap(us,'UNITED STATES','rainbow')

china=country(dataframes_tr,indicators,'China')
correlation_heatmap(china,'CHINA','jet')

brazil=country(dataframes_tr,indicators,'Brazil')
correlation_heatmap(brazil,'BRAZIL','jet')

# australia=country(dataframes_tr, indicators, 'Australia') 
# correlation_heatmap(australia, 'AUSTRALIA', 'jet')
