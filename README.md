# E-commerce Market Data Analysis 

## Project description
_**Disclaimer**_: The following is a brief introduction of the project. For the full analysis please download the file **"e-commerce-analysis.html"** available in this repository (html version) or **"e-commerce-analysis.ipynb"** (Python script)
<br>
In this project, we analyse the **transactions of an e-commerce platform** occurring over the years 2010 and 2011 to extract customer and market insights. Our goal is to design and obtain Key Performance Indicators (KPIs) to identify room for improvement in the platform performance.  
<br> Some of the **questions** we will address include:
- Which country expends the most in aggregate?
- Is there a relationship between a country's GDP and its purchases on the platform?
- Which products are most popular in the platform?

The analysis will be conducted following **three steps**:
1. Loading three datasets
2. Data cleaning and manipulation
3. Data Analysis:
  - Exploratory Data Analysis (EDA) to find salient patterns and infer relationships between data elements.
  - Market and product analysis.
  
For the analysis, we employed the following **packages**:

- NumPy
- Pandas
- Matplotlib
- Seaborn

##Main results 
- The UK is largest market in terms of total sales and number of sales.
- Considering the observed customer behavior in certain markets, such as Portugal, there are growth opportunities: in such markets customers tend to purchase more expensive items, however the number of sales is significantly smaller compared to other markets.
- The positive relationship between GDP per capita and wholesale sales represents a chance to increase the sales volumes in countries associated with higher GDP per capita, which currently are among the least relevant markets.
- Seasonality trends show that there is room to develop tailor-made sales strategies for each peak season.

## Data 
The data used for this project is publicly available at the following sources: 
- [E-commerce data](https://archive-beta.ics.uci.edu/ml/datasets/online+retail)
- [GDP data](https://data.worldbank.org/indicator/NY.GDP.PCAP.CD) 
- [Colors data](https://data.world/dilumr/color-names)

## Statement of contributions 
The code and analysis for this project were developed jointly by **Sofia Lai** and **[Elena García Mañes](https://github.com/ElenaGarciaManes)**
