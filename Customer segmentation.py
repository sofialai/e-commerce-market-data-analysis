#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 10:32:56 2022

@author: sofialai
"""

import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np


cust = pd.read_csv("/Users/sofialai/Documents/Python/Projects/Customer Segmentation/data_cust.csv", encoding = 'unicode_escape')
cust.dtypes #checking variables types 
cust = cust.astype({"CustomerID":"str"}) #convert "CustomerID" to string 
len(cust["CustomerID"].unique()) # 4373 unique customers 
len(cust["Country"].unique()) # 38 countries

cust.isna().any()
#Separate date and time 

#Focus analysis on orders, not considering returns 
cust = cust[cust["Quantity"] > 0 ]
cust = cust[cust["CustomerID"] != "nan"] #dropping NaN in CustomerID
#Total purchases by country and by customer
cust["UnitPrice_EUR"] = cust["UnitPrice"] * 1.166 #convert prices from GBP to EUR (conversion rate taken at the time of the data collection (2010-2011): 1 GBP = 1.166 EUR
cust["tot_purch_country"] = cust.groupby("Country")["Quantity"].transform(sum)
cust["tot_exp_country"] = cust.groupby("Country")["UnitPrice_EUR"].transform(sum)
cust["unique_cust_per_country"] = cust.groupby("Country")["CustomerID"].transform('nunique')
cust["tot_purch_country_per_cust"] = cust["tot_purch_country"]/cust["unique_cust_per_country"]
cust["tot_exp_country_per_cust"] = cust["tot_exp_country"]/cust["unique_cust_per_country"]

#Average purchases by country and by customer
cust["avg_purch_country"] = cust.groupby("Country")["Quantity"].transform('mean') #Average number of purchases by country
cust["avg_exp_country"] = cust.groupby("Country")["UnitPrice_EUR"].transform('mean') #Average unit price by country
cust["avg_cust_per_country"] = cust.groupby("Country")["CustomerID"].transform('nunique') #Average number of unique customers per country
cust["avg_purch_country_per_cust"] = cust["avg_purch_country"]/cust["unique_cust_per_country"] #Average number of purchases by country, by unique customer
cust["avg_exp_country_per_cust"] = cust["avg_exp_country"]/cust["unique_cust_per_country"] #Average expenditure per country, by unique customer
cust["tot_exp_cust"] = cust.groupby("CustomerID")["UnitPrice_EUR"].transform(sum) #Total expenditure by unique customer

#negative quantities mean that the order was canceled. This is not a problem since the order is counted twice (once when placed and once when canceled, so in the end it is balanced out)
#idea: analyze which products are most canceled. 

#Limit analysis to total purchase >= 10K
cust_selected = cust[cust['tot_purch_country'] >= 10000] #selecting markets with 10K purchases or more

cust_selected_plot = cust_selected.drop_duplicates(subset = 'Country', keep = 'last')  #ensure at least one row from the duplicates is kept, if keep = False then ALL duplicates are removed, only rows that have no duplicate are kept

cust_selected_plot = cust_selected_plot.sort_values('tot_purch_country')

cust_selected_plot

#Add GDP per capita for 2010
gdp = pd.read_excel("/Users/sofialai/Documents/Python/Projects/Customer Segmentation/gdp_per_cap.xlsx")
gdp = gdp.iloc[:, [0, -12]]
cust_selected_gdp = cust_selected.merge(gdp, left_on = "Country", right_on = "Country Name")
cust_selected_gdp = cust_selected_gdp.drop(columns = "Country Name")
cust_selected_gdp = cust_selected_gdp.rename(columns = {cust_selected_gdp.columns[-1]:"gdp_per_cap"})

#Convert gdp_per_cap (USD to EUR) 
cust_selected_gdp["gdp_per_cap"] = cust_selected_gdp["gdp_per_cap"] * 0.755
cust_selected_gdp = cust_selected_gdp.round(decimals = 2)
cust_selected_gdp

#Create region variable
cust_selected_gdp["Country"].unique()
eu_countries = ["France", "Netherlands", "Germany", "Spain", "Portugal", "Belgium", "Sweden", "Finland"] 

cust_selected_gdp = cust_selected_gdp.assign(EU_member = ["EU" if Country in eu_countries 
                                                          else "Non-EU"
                                                          for Country in cust_selected_gdp["Country"]])


cust_selected_gdp = cust_selected_gdp.rename(columns={'EU_member' :'EU Membership'})

#Create type of sale variable
cust_selected_gdp = cust_selected_gdp.assign(type_sale = ["Retail" if Quantity <= 15
                                                          else "Wholesale"
                                                          for Quantity in cust_selected_gdp["Quantity"]])


import seaborn as sns
sns.countplot(x = "Country", data = cust_selected_gdp)

#EU and non-EU 
sns.countplot(x = "EU Membership", data = cust_selected_gdp)


#Number of total purchases by country
cust_selected_gdp_plot_1 = cust_selected_gdp.drop_duplicates(subset = 'Country', keep = 'last') #different subset for each plot
cust_selected_gdp_plot_1 = cust_selected_gdp_plot_1.sort_values("tot_purch_country")

fig, ax = plt.subplots(figsize = (30, 15))

def plot_fun(axes, x, y, xlabel, ylabel, title): 
    axes.barh(x, y)
    axes.set_xlabel(xlabel, fontsize = 30)
    axes.set_ylabel(ylabel, fontsize = 30)
    axes.set_title(title, fontsize = 40)

plot_fun(ax, 
         cust_selected_gdp_plot_1['Country'], 
         cust_selected_gdp_plot_1['tot_purch_country'],
         "Number of purchases (M)",
         "Country", 
         "Total number of purchases (M) by country")
ax.set_yticklabels(cust_selected_gdp_plot_1["Country"], rotation = 0, fontsize = 20) #find a way to add this to function 
#find a way to change x axis font size
plt.show()


#Total expenditure by country
cust_selected_gdp_plot_3 = cust_selected_gdp.drop_duplicates(subset = 'Country', keep = 'last')
cust_selected_gdp_plot_3 = cust_selected_gdp_plot_3.sort_values("tot_exp_country")

fig, ax = plt.subplots(figsize = (30, 15))

ax.barh(cust_selected_gdp_plot_3["Country"],
       cust_selected_gdp_plot_3["tot_exp_country"])
ax.set_xlabel("Total expenditure by country (EUR)", fontsize = 25)
ax.set_yticklabels(cust_selected_gdp_plot_3["Country"], fontsize = 20)
ax.set_ylabel("Country", fontsize = 25)
ax.set_xticklabels(cust_selected_gdp_plot_3["tot_exp_country"], fontsize = 20)
ax.set_title("Total expenditure by country (EUR)", fontsize = 40)


#Average expenditure by country 
cust_selected_gdp_plot_2 = cust_selected_gdp.drop_duplicates(subset = 'Country', keep = 'last')
cust_selected_gdp_plot_2 = cust_selected_gdp_plot_2.sort_values("avg_exp_country")

fig, ax = plt.subplots(figsize = (30, 15))

ax.barh(cust_selected_gdp_plot_2["Country"],
       cust_selected_gdp_plot_2["avg_exp_country"])
ax.set_xlabel("Average item price (EUR)", fontsize = 25)
ax.set_yticklabels(cust_selected_gdp_plot_2["Country"], fontsize = 20)
ax.set_ylabel("Country", fontsize = 25)
ax.set_xticklabels(cust_selected_gdp_plot_2["avg_exp_country"], fontsize = 20)
ax.set_title("Average item price (EUR) by country", fontsize = 40)


# Scatter plot on total expenditure by unique customer, by country (EU, non-EU)

sns.set_context("paper", rc={"font.size":20,"axes.titlesize":25,"axes.labelsize":20})  

plot = sns.relplot(x = "tot_exp_cust",
            y = "gdp_per_cap", 
            data = cust_selected_gdp,
            height = 10, 
            aspect = 1.5, 
            kind = "scatter", 
            col = "EU Membership", 
            col_order = ["EU", "Non-EU"],
            row = "type_sale", 
            row_order = ["Wholesale", "Retail"],
            alpha = 0.2, 
            s = 100)

plot.set(xscale="log")

# Set labels
plot.set(xlabel = 'Average expenditure by country', 
         ylabel= 'GDP per capita'
         )

#Regression line on average expenditure by country and gdp per capita 

sns.set_context("paper", rc={"font.size":20,"axes.titlesize":25,"axes.labelsize":20})  

plot = sns.lmplot(x = "tot_exp_cust",
            y = "gdp_per_cap", 
            data = cust_selected_gdp,
            height = 10, 
            aspect = 1.5,
            hue = "type_sale")


# Set labels
plot.set(xlabel = 'Average expenditure by country', 
         ylabel= 'GDP per capita',
         title = 'Relationship between GDP per capita and Average Expenditure by customer')



#Sales by date 

sns.relplot(x = "InvoiceDate", 
            y = "Quantity", 
            data = cust_selected_gdp, 
            kind = "line", 
            hue = "Country")




