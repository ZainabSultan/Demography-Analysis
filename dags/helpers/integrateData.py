# M1 -> Cleaning, tidying and visualizations
# M2 -> Feature Engineering and pipeline
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
def integrate_data(**kwargs):
    root_path_happiness = 'c/Users/ahmed/Cleaned_data/happiness_data_sets'
    life_expectancy_df = pd.read_csv("c/Users/ahmed/Cleaned_data/Life Expectancy Data.csv")
    df_250_Country_Data = pd.read_csv('c/Users/ahmed/Cleaned_data/250 Country Data.csv')
    df_happinies_2015 = pd.read_csv(root_path_happiness + '/2015.csv')
    df_happinies_2016 = pd.read_csv(root_path_happiness + '/2016.csv')
    df_happinies_2017 = pd.read_csv(root_path_happiness + '/2017.csv')
    df_happinies_2018 = pd.read_csv(root_path_happiness + '/2018.csv')
    df_happinies_2019 = pd.read_csv(root_path_happiness + '/2019.csv')
    last_column_2015 = len(df_happinies_2015)*[2015]
    last_column_2016 = len(df_happinies_2016)*[2016]
    last_column_2017 = len(df_happinies_2017)*[2017]
    last_column_2018 = len(df_happinies_2018)*[2018]
    last_column_2019 = len(df_happinies_2019)*[2019]
    df_Years_2015 = pd.DataFrame({'Year': last_column_2015})
    df_Years_2016 = pd.DataFrame({'Year': last_column_2016})
    df_Years_2017 = pd.DataFrame({'Year': last_column_2017})
    df_Years_2018= pd.DataFrame({'Year': last_column_2018})
    df_Years_2019 = pd.DataFrame({'Year': last_column_2019})
    df_happinies_2015=pd.concat([df_happinies_2015, df_Years_2015],axis=1)
    df_happinies_2016=pd.concat([df_happinies_2016, df_Years_2016],axis=1)
    df_happinies_2017_WithLastColumn=pd.concat([df_happinies_2017, df_Years_2017],axis=1)
    df_happinies_2018_WithLastColumn =pd.concat([df_happinies_2018, df_Years_2018],axis=1) 
    df_happinies_2019_WithLastColumn=pd.concat([df_happinies_2019, df_Years_2019],axis=1)
    df_happinies_2019 = pd.merge(df_happinies_2019_WithLastColumn,df_happinies_2015[['Region','Country']], on = "Country")
    df_happinies_2018 = pd.merge(df_happinies_2018_WithLastColumn,df_happinies_2015[['Region','Country']], on = "Country")
    df_happinies_2017 = pd.merge(df_happinies_2017_WithLastColumn,df_happinies_2015[['Region','Country']], on = "Country")


    Integrated_Happiness = pd.concat([(pd.concat([(pd.concat([(pd.concat([df_happinies_2015[['Region','Country',"Happiness Rank",
                                    "Happiness Score","Economy (GDP per Capita)","Social support","Healthy life expectancy",
                                    "Freedom to make life choices","Trust (Government Corruption)","Generosity","Cluster","Year"]], df_happinies_2016[['Region','Country',"Happiness Rank",
                                    "Happiness Score","Economy (GDP per Capita)","Social support","Healthy life expectancy",
                                    "Freedom to make life choices","Trust (Government Corruption)","Generosity","Cluster","Year"]]], axis=0)),
                                    df_happinies_2017[['Region','Country',"Happiness Rank",
                                    "Happiness Score","Economy (GDP per Capita)","Social support","Healthy life expectancy",
                                    "Freedom to make life choices","Trust (Government Corruption)","Generosity","Cluster","Year"]]], axis = 0)),
            df_happinies_2018[['Region','Country',"Happiness Rank",
                                    "Happiness Score","Economy (GDP per Capita)","Social support","Healthy life expectancy",
                                    "Freedom to make life choices","Trust (Government Corruption)","Generosity","Cluster","Year"]]], axis = 0)),
                    df_happinies_2019[['Region','Country',"Happiness Rank",
                                    "Happiness Score","Economy (GDP per Capita)","Social support","Healthy life expectancy",
                                    "Freedom to make life choices","Trust (Government Corruption)","Generosity","Cluster","Year"]]], axis = 0)
    Integrated_Happiness.reset_index(inplace=True)
    Inegrated_data = pd.merge(Integrated_Happiness, df_250_Country_Data,left_on="Country", right_on="name", how='left')
    Inegrated_data.drop(columns=["Unnamed: 0"],inplace = True)
    Inegrated_data.drop(columns=["Unnamed: 0.1"],inplace = True)
    Inegrated_data.drop(columns=["Region"],inplace = True)
    Inegrated_data.drop(columns=["name"],inplace = True)
    Inegrated_data=Inegrated_data[~Inegrated_data['region'].isnull()]
    Inegrated_data["density"] = Inegrated_data["population"]/Inegrated_data["area"]
    minvalue = Inegrated_data['density'].min()
    maxvalue = Inegrated_data['density'].max()
    density_group = pd.cut(Inegrated_data.density, [0,400,800,1200,1600,1800,2200,2600,3000,3400,3800,4200,4600,5000,5400,5800,6200,6600,7000,7400,7800],labels=
                       ["0-400" ,"400-800" ,"800-1200" , "1200-1600","1600-2000" , "2000-2400","2400-2800", "2800-3200" , "3200-3600", "3600-4000","4000-4400" ,"4400-4800",
                        "4800-5200" , "5200-5600" ,
                        "5600-6000" ,"6000-6400", "6400-6800", "6800-7200","7200-7600"  , "7600-8000"])
    Inegrated_data["density_group"] = density_group 
    root_path='c/Users/ahmed/Integrated_Data/'
    Integrated_Happiness.to_csv("Integrated_Happiness.csv")
    Inegrated_data.to_csv("Integrated_Happiness_Country_Data.csv")
    integrated_happiness_df=Integrated_Happiness
    life_expectancy_df = life_expectancy_df[['Country', 'Status']]
    life_expectancy_df = life_expectancy_df.drop_duplicates()
    life_expectancy_df = life_expectancy_df.reset_index()
    life_expectancy_df = life_expectancy_df.drop( columns = ['index'], axis = 1)
    merged_happiness_life = pd.merge(integrated_happiness_df, life_expectancy_df,left_on="Country", right_on="Country", how='left')
    status_nulls=merged_happiness_life[merged_happiness_life['Status'].isnull()]
    status_nulls['Country'].unique()
    countries = status_nulls['Country']
    countries = countries.drop_duplicates()
    countries = countries.reset_index()
    non_developed = status_nulls.loc[status_nulls['Country'] == "Venezuela"]
    non_developed = non_developed.append(status_nulls.loc[status_nulls['Country'] == "Bolivia"])
    non_developed = non_developed.append(status_nulls.loc[status_nulls['Country'] == "Vietnam"])
    non_developed = non_developed.append(status_nulls.loc[status_nulls['Country'] == "Somaliland region"])
    non_developed = non_developed.append(status_nulls.loc[status_nulls['Country'] == "Macedonia"])
    non_developed = non_developed.append(status_nulls.loc[status_nulls['Country'] == "Laos"])
    non_developed = non_developed.append(status_nulls.loc[status_nulls['Country'] == "Palestinian Territories"])
    non_developed = non_developed.append(status_nulls.loc[status_nulls['Country'] == "Congo (Kinshasa)"])
    non_developed = non_developed.append(status_nulls.loc[status_nulls['Country'] == "Congo (Brazzaville)"])
    non_developed = non_developed.append(status_nulls.loc[status_nulls['Country'] == "Ivory Coast"])
    non_developed = non_developed.append(status_nulls.loc[status_nulls['Country'] == "Tanzania"])
    non_developed = non_developed.append(status_nulls.loc[status_nulls['Country'] == "Syria"])
    non_developed = non_developed.append(status_nulls.loc[status_nulls['Country'] == "Somaliland Region"])
    non_developed.replace(np.nan,"Developing" , inplace=True)
    non_developed = non_developed.reset_index()
    developed = status_nulls.loc[status_nulls['Country'] == "United States"]
    developed = developed.append(status_nulls.loc[status_nulls['Country'] == "United Kingdom"])
    developed = developed.append(status_nulls.loc[status_nulls['Country'] == "Czech Republic"])
    developed = developed.append(status_nulls.loc[status_nulls['Country'] == "South Korea"])
    developed = developed.append(status_nulls.loc[status_nulls['Country'] == "United Kingdom"])
    developed = developed.append(status_nulls.loc[status_nulls['Country'] == "Russia"])
    developed = developed.append(status_nulls.loc[status_nulls['Country'] == "North Cyprus"])
    developed = developed.append(status_nulls.loc[status_nulls['Country'] == "Kosovo"])
    developed = developed.append(status_nulls.loc[status_nulls['Country'] == "Hong Kong"])
    developed = developed.append(status_nulls.loc[status_nulls['Country'] == "Iran"])
    developed = developed.append(status_nulls.loc[status_nulls['Country'] == "Puerto Rico"])
    developed = developed.append(status_nulls.loc[status_nulls['Country'] == "Taiwan"])
    developed.replace(np.nan,"Developed" , inplace=True)
    developed = developed.reset_index()
    developed_and_non_developed = developed
    developed_and_non_developed = developed_and_non_developed.append(non_developed)
    developed_and_non_developed = developed_and_non_developed.drop(columns = ["level_0", "index"], axis = 1)
    developed_and_non_developed = developed_and_non_developed.reset_index(drop=True)
    for index, row in countries.iterrows():
        merged_happiness_life = merged_happiness_life[merged_happiness_life["Country"] != row["Country"]]
    merged_happiness_life = merged_happiness_life.append(developed_and_non_developed)
    merged_happiness_life = merged_happiness_life.reset_index(drop=True)
    merged_happiness_life = merged_happiness_life.reset_index(drop=True)
    merged_happiness_life.to_csv(root_path+"Q1_Integrated_Happiness_with_life.csv")
    df_happinies_2019.to_csv(root_path+"Q5_df_happinies_2019_with_Region.csv")
    df_happinies_2018.to_csv(root_path+"Q5_df_happinies_2018_with_Region.csv")
    df_happinies_2017.to_csv(root_path+"Q5_df_happinies_2017_with_Region.csv")