# M1 -> Cleaning, tidying and visualizations
# M2 -> Feature Engineering and pipeline
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns;
from sklearn import preprocessing
def clean_data(**kwargs):
    country_data_df = pd.read_csv('c/Users/ahmed/data/250 Country Data.csv')
    country_data_df
    country_data_df= country_data_df.drop(["gini","Real Growth Rating(%)","Literacy Rate(%)","Inflation(%)","Unemployement(%)"], axis=1)
    country_data_df =  country_data_df[country_data_df['population'] != 0]
    null_count=country_data_df.isnull()
    country_data_df2 =  country_data_df[null_count['subregion'] == True]
    if((country_data_df2['name'].all()=="Antarctica")& (len(country_data_df2)==1)):
        country_data_df['subregion'].replace(np.nan, "Polar", inplace=True)
    country_data_df2 =  country_data_df[country_data_df['population'] < country_data_df.population.mean()/4]
    country_data_df2 = country_data_df.sort_values(by=['area'])
    country_data_df2['area_index'] = range(0, len(country_data_df2))
    country_data_df =  country_data_df2[country_data_df2['area_index'] <= len(country_data_df2)*0.95]
    country_data_df.drop(["area_index"], axis=1)
    country_data_df = country_data_df.sort_index()
    root_path='c/Users/ahmed/Cleaned_data/'
    country_data_df.to_csv(root_path+'250 Country Data.csv')