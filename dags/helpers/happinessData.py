import requests
import json
import pandas as pd
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns; sns.set_theme()
import numpy as np
from numpy import unique
from numpy import where
from sklearn.cluster import KMeans
from sklearn import preprocessing
from sklearn.datasets import make_classification
from sklearn.neighbors import LocalOutlierFactor
def create_clusters(data,k):
    # define dataset
    columns=data.columns.values
    i=np.where(columns == "Happiness Score")[0][0]
    X = data.iloc[:, i:].values
    # define the model
    model = KMeans(n_clusters = k, init = 'k-means++', random_state = 42)
    # fit the model
    model.fit(X)
    # assign a cluster to each example
    y_kmeans = model.predict(X)
    clusters = pd.DataFrame(y_kmeans)
    clusters.columns = ["Cluster"] 
    newdata=pd.concat([data, clusters], axis=1)
    return newdata

def clean_data(**kwargs):
   root_path_happiness = 'c/Users/ahmed/data/Happiness_Dataset/'
   world_happiness_2015_df = pd.read_csv(root_path_happiness+'2015.csv')
   world_happiness_2016_df = pd.read_csv(root_path_happiness+'2016.csv')
   world_happiness_2017_df = pd.read_csv(root_path_happiness+'2017.csv')
   world_happiness_2018_df = pd.read_csv(root_path_happiness+'2018.csv')
   world_happiness_2019_df = pd.read_csv(root_path_happiness+'2019.csv')
   world_happiness_2015_df = world_happiness_2015_df.rename(columns={'Family': 'Social support','Health (Life Expectancy)':'Healthy life expectancy','Freedom':'Freedom to make life choices'})
   world_happiness_2016_df = world_happiness_2016_df.rename(columns={'Family': 'Social support','Health (Life Expectancy)':'Healthy life expectancy','Freedom':'Freedom to make life choices'})
   world_happiness_2017_df = world_happiness_2017_df.rename(columns={'Happiness.Rank' : 'Happiness Rank','Family':'Social support',"Happiness.Score" : 'Happiness Score','Health..Life.Expectancy.': 'Healthy life expectancy','Economy..GDP.per.Capita.': 'Economy (GDP per Capita)', 'Freedom':  'Freedom to make life choices', 'Trust..Government.Corruption.' : 'Trust (Government Corruption)', 'Dystopia.Residual': 'Dystopia Residual'})
   world_happiness_2018_df = world_happiness_2018_df.rename(columns={"Country or region": "Country","Score": "Happiness Score", 'GDP per capita' :'Economy (GDP per Capita)','Perceptions of corruption' : 'Trust (Government Corruption)', 'Overall rank' : 'Happiness Rank'})
   world_happiness_2019_df = world_happiness_2019_df.rename(columns={"Country or region": "Country","Score": "Happiness Score", 'GDP per capita' :'Economy (GDP per Capita)','Perceptions of corruption' : 'Trust (Government Corruption)', 'Overall rank' : 'Happiness Rank'})
   columns=world_happiness_2015_df.columns.tolist()
   for column in columns:
      if (world_happiness_2015_df[column].isnull().sum().any()>0):
         world_happiness_2015_df[column].replace(np.nan,0 , inplace=True)
   columns=world_happiness_2016_df.columns.tolist()
   for column in columns:
      if (world_happiness_2016_df[column].isnull().sum().any()>0):
         world_happiness_2016_df[column].replace(np.nan,0 , inplace=True)
   columns=world_happiness_2017_df.columns.tolist()
   for column in columns:
      if (world_happiness_2017_df[column].isnull().sum().any()>0):
         world_happiness_2017_df[column].replace(np.nan,0 , inplace=True)
   columns=world_happiness_2018_df.columns.tolist()
   for column in columns:
      if (world_happiness_2018_df[column].isnull().sum().any()>0):
         world_happiness_2018_df[column].replace(np.nan,0 , inplace=True)
   columns=world_happiness_2019_df.columns.tolist()
   for column in columns:
      if (world_happiness_2019_df[column].isnull().sum().any()>0):
         world_happiness_2019_df[column].replace(np.nan,0 , inplace=True)
   clustered_2015=create_clusters(world_happiness_2015_df,3)
   clustered_2016=create_clusters(world_happiness_2016_df,3)
   clustered_2017=create_clusters(world_happiness_2017_df,3)
   clustered_2018=create_clusters(world_happiness_2018_df,3)
   clustered_2019=create_clusters(world_happiness_2019_df,3)
   root_path='c/Users/ahmed/Cleaned_data/happiness_data_sets/'
   clustered_2015.to_csv(root_path+'2015.csv')
   clustered_2016.to_csv(root_path+'2016.csv')
   clustered_2017.to_csv(root_path+'2017.csv')
   clustered_2018.to_csv(root_path+'2018.csv')
   clustered_2019.to_csv(root_path+'2019.csv')







