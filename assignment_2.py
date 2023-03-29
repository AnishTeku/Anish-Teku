# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 12:25:45 2023

@author: anish
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 

def transpose_dfs(data):
    data_tr=pd.DataFrame.transpose(data)
    data_tr.columns=data['Country Name']
    data_tr=data_tr.iloc[1:,:]
    data.index=data['Country Name']
    
    return data, data_tr

def bar_plot(data,lab_title):
    plt.figure()
    width=0.8/len(data.columns)
    offset=width/2
    ax=plt.subplot()
    for index,year in enumerate(data.columns):
        ax.bar([ln+offset+width*index for ln in range(len(data.index))],
               data[year],width=width,label=year)
    ax.set_xticks([j+0.4 for j in range(len(data.index))])  
    ax.set_xticklabels(data.index,rotation=90)

    ax.set_xlabel('Country Name')
    ax.set_ylabel(lab_title[0])
    ax.set_title(lab_title[1])
    ax.legend()
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

    # Show all ticks and label them with the dataframe column name
    plt.xticks(range(len(data.columns)),data.columns, rotation=65, fontsize=15)
    plt.yticks(range(len(data.columns)),data.columns, rotation=0, fontsize=15)

    # Loop over data dimensions and create text annotations
    for i in range(len(data.columns)):
        for j in range(len(data.columns)):
            plt.text(i,j, corr[i, j].round(2),
                           ha="center", va="center", color='black')
    plt.title(country)
    plt.show()


countries=['Australia','Brazil','China',
           'United Kingdom','India','Italy','Japan','Mexico',
           'United States','Pakistan']
years=['1995','2000','2005','2010','2015','2020']


#Agricultural land
agri_land=pd.read_csv('Agriculture_Land_Area.csv',skiprows=(4))

agri_land,agri_land_tr=transpose_dfs(agri_land)

agri=agri_land.loc[countries,years]

lab_title=['Agricultural Land sq Km','AGRICULTURAL LAND']
bar_plot(agri,lab_title)

#CO2 emissions in kt per capita
co2_mt=pd.read_csv('CO2_mt_per_capita.csv',skiprows=(4))

co2_mt,co2_mt_tr=transpose_dfs(co2_mt)

co2=co2_mt.loc[countries,years]

lab_title=['CO2 emission in kt','CO2 EMISSIONS IN kt PER CAPITA']
bar_plot(co2,lab_title)

#GDP_USD
gdp_usd=pd.read_csv('GDP_USD.csv',skiprows=(4))

gdp_usd,gdp_usd_tr=transpose_dfs(gdp_usd)

gdp=gdp_usd.loc[countries,years]

lab_title=['GDP in Dollars $','GDP in USD']
bar_plot(gdp,lab_title)

#Labour Force 
lab_force=pd.read_csv('Labour_Force_Total.csv',skiprows=(4))

lab_force,lab_force_tr=transpose_dfs(lab_force)

labour=lab_force.loc[countries,years]

lab_title=['Labour population','LABOUR FORCE IN TOTAL']
bar_plot(labour,lab_title)


#Total population
population_total=pd.read_csv('POP_Total.csv',skiprows=(4))

population_total,population_total_tr=transpose_dfs(population_total)

population=lab_force.loc[countries,years]

lab_title=['Population','TOTAL POPULATION']
bar_plot(population,lab_title)

indicators=['Agricultural Land','CO2 Emissions','GDP','Labour Force','Population Total']
dataframes=[agri_land,co2_mt,gdp_usd,lab_force,population_total]
dataframes_tr=[agri_land_tr,co2_mt_tr,gdp_usd_tr,lab_force_tr,population_total_tr]

australia=country(dataframes_tr, indicators, 'Australia')
print(australia)

correlation_heatmap(australia, 'AUSTRALIA', 'jet')

brazil=country(dataframes_tr,indicators,'Brazil')
correlation_heatmap(brazil,'BRAZIL','jet')

china=country(dataframes_tr,indicators,'China')
correlation_heatmap(china,'CHINA','jet')

uk=country(dataframes_tr,indicators,'United Kingdom')
correlation_heatmap(uk,'UNITED KINGDOM','jet')

india=country(dataframes_tr,indicators,'India')
correlation_heatmap(india,'INDIA','jet')

italy=country(dataframes_tr,indicators,'Italy')
correlation_heatmap(italy,'ITALY','jet')

japan=country(dataframes_tr,indicators,'Japan')
correlation_heatmap(japan,'JAPAN','jet')

mexico=country(dataframes_tr,indicators,'Mexico')
correlation_heatmap(mexico,'MEXICO','jet')

us=country(dataframes_tr,indicators,'United States')
correlation_heatmap(us,'UNITED STATES','jet')

pakistan=country(dataframes_tr,indicators,'Pakistan')
correlation_heatmap(pakistan,'PAKISTAN','jet')
 
# australia.to_csv('aus.csv')

# arr=australia.corr().to_numpy()
# print(australia)
# print('corr is')
# print(arr)

# fig = plt.subplots(figsize=(8,8))
# plt.imshow(arr, interpolation='nearest')
# plt.colorbar(orientation='vertical', fraction = 0.05)

# # Show all ticks and label them with the dataframe column name
# plt.xticks(range(len(australia.columns)),australia.columns, rotation=65, fontsize=15)
# plt.yticks(range(len(australia.columns)),australia.columns, rotation=0, fontsize=15)

# # Loop over data dimensions and create text annotations
# for i in range(len(australia.columns)):
#     for j in range(len(australia.columns)):
#         text = plt.text(j, i, arr[i, j].round(2),
#                        ha="center", va="center", color="black")
# plt.title('Australia')
# plt.show()

 


