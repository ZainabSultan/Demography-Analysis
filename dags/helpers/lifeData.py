import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns; sns.set_theme()
from sklearn import preprocessing
import math
from sklearn import linear_model
from sklearn.neighbors import KNeighborsRegressor
def tidy_life_expectancy(life_expectancy_df):
    life_expectancy_df.columns = life_expectancy_df.columns.str.lstrip()
    life_expectancy_df.columns = life_expectancy_df.columns.str.rstrip()
    life_expectancy_df.rename(columns = {'HIV/AIDS':'HIV/AIDS Deaths'}, inplace = True) 
    life_expectancy_df.rename(columns = {'Measles':'Number of reported Measles cases'}, inplace = True) 
    #diseses_columns = ['Hepatitis B','Polio','Diphtheria','Measles', 'HIV/AIDS']
    #diseases_count_columns = ['Measles', 'HIV/AIDS']
    immunization_columns = ['Hepatitis B','Polio','Diphtheria']
    #melt immunization
    new_columns =  [column for column in list(life_expectancy_df.columns) if not(column in immunization_columns)]  #print([s for s in l if s != 'Bob'])
    life_expectancy_df_melted = pd.melt(life_expectancy_df,id_vars=new_columns,var_name="Disease", value_name="Immunization coverage")
    life_expectancy_df_melted.head()
    return life_expectancy_df_melted
    #Measles - number of reported cases per 1000 population
    #HIV/AID Deaths per 1 000 live births HIV/AIDS (0-4 years)
    #Hepatitis B (HepB) immunization coverage among 1-year-olds (%)
    #Polio (Pol3) immunization coverage among 1-year-olds (%)
    #Diphtheria tetanus toxoid and pertussis (DTP3) immunization coverage among 1-year-olds (%)
def turn_inaccurate_to_nan(tidy_life_expectancy_df):
    tidy_life_expectancy_df['infant deaths'].replace({0: np.nan}, inplace = True)
    tidy_life_expectancy_df['under-five deaths'].replace({0: np.nan}, inplace = True)
    tidy_life_expectancy_df['Schooling'].replace({0: np.nan},inplace = True)
    tidy_life_expectancy_df['percentage expenditure'].replace({0: np.nan}, inplace = True)
    tidy_life_expectancy_df['Number of reported Measles cases'].replace({0: np.nan},inplace = True)
    
    irrelevant_columns = ["infant deaths", "under-five deaths","Number of reported Measles cases","BMI","Alcohol","thinness  1-19 years","thinness 5-9 years","Total expenditure","Population" ]
    tidy_life_expectancy_df.drop(columns=irrelevant_columns, inplace = True)
    return tidy_life_expectancy_df
def correct_data(tidy_life_expectancy_df):
    #correcting some values
    indices_canada = tidy_life_expectancy_df.loc[tidy_life_expectancy_df["Country"]=="Canada"].index
    tidy_life_expectancy_df.loc[indices_canada, ("Status")] = "Developed"

    indices_canada = tidy_life_expectancy_df.loc[tidy_life_expectancy_df["Country"]=="Greece"].index
    tidy_life_expectancy_df.loc[indices_canada, ("Status")] = "Developed"

    tidy_life_expectancy_df.loc[tidy_life_expectancy_df["Country"]=="Greece"].head()
    
    return tidy_life_expectancy_df
def FreedmanRule(input_vector):
    #calculate IQR
    #print(input_vector)
    #using nan percentile to ignore nans
    q75, q25 = np.nanpercentile(input_vector, [75 ,25])
    #print(q25)
    iqr = q75 - q25
    #calculate Bin width
    bin_width = (2* iqr) / int(round(len(input_vector) ** (1. / 3)))
    return bin_width
def medianImputation(dataframe, feature):
    median = dataframe[feature].median()
    dataframe.loc[dataframe[feature].isnull(), (feature + '_temp')] = median
    return dataframe
def randomImputation(dataframe, feature):

    number_missing = dataframe[feature].isnull().sum()
    observed_values = dataframe.loc[dataframe[feature].notnull(), (feature)]
    dataframe.loc[dataframe[feature].isnull(), (feature + '_temp')] = np.random.choice(observed_values, number_missing, replace = True)

    return dataframe
#in: dataframe, features used by the model, feature that the model will predict, the type of model to fit, whether reshaping is needed or not
#output: fitted model, ready to be used to predict feature
def create_model(dataframe,params, feature_to_impute, model_type , reshape):
    
    if(model_type == "LR"):
        model = linear_model.LinearRegression()
    else:
        model = KNeighborsRegressor(n_neighbors=2)
    #fit model on data
    if(reshape):
        XTrain =np.array(dataframe[params]).reshape(-1, 1)
    else:
        XTrain = dataframe[params]
        
        #print(XTrain.isna().sum())
    model.fit(X = XTrain , y = dataframe[feature_to_impute + '_temp'])
    return model
def merge_dataframes(dataframe,original_dataframe,columns_to_drop, column_old, column_new, status_to_keep):
    #dropping temporary columns
    dataframe.drop(columns=columns_to_drop,inplace = True)
    #rename the imputed column
    dataframe.rename(columns = {column_old:column_new}, inplace = True)
    #drop the old part from the original data set 
    original_dataframe = original_dataframe[original_dataframe['Status'] == status_to_keep]
    original_dataframe=pd.concat([dataframe, original_dataframe], sort = False)
    #print("Number of nulls in feature now: ",original_dataframe.isna().sum()[column_new])
    
    #print(original_dataframe.columns,"megre")
    return original_dataframe
def preprocess_dataframe(status, life_expectancy_dataframe,columns_of_interest,feature_to_impute, model_type, placeholder_method_array):
    
    dataframe =  life_expectancy_dataframe[ life_expectancy_dataframe['Status'] == status].copy(deep=True)
    i =0
    for feature in columns_of_interest:
        placeholder_method = placeholder_method_array[i]
        dataframe[feature + '_temp'] = dataframe[feature]
        if(placeholder_method ==0):
            dataframe = medianImputation(dataframe, feature)
        if(placeholder_method ==1):
            dataframe = randomImputation(dataframe, feature)
        i = i+1
        
    dataframe[feature_to_impute + '_temp'] = dataframe[feature_to_impute]
    dataframe = medianImputation(dataframe, feature_to_impute)

    #print(dataframe.isna().loc[:,(feature_to_impute +"_temp")].sum())
    reshape=False
    
    if(len(columns_of_interest)==1):
        reshape = True
    
    model = create_model(dataframe,[feature_preprocessed + "_temp" for feature_preprocessed in columns_of_interest],feature_to_impute, model_type, reshape)
    #this next step is done to maintain those points that are not null
    dataframe[feature_to_impute+"_imputed"] = dataframe[feature_to_impute] 
    features_preprocessed = [feature_preprocessed + "_temp" for feature_preprocessed in columns_of_interest]
    dataframe.loc[dataframe[feature_to_impute].isnull(),  (feature_to_impute+"_imputed")] = model.predict(dataframe[features_preprocessed])[dataframe[feature_to_impute].isnull()]
    #print("number of nulls in imputed column: ",dataframe.isna().loc[:,(feature_to_impute+"_imputed")].sum())
    dataframe.loc[dataframe[feature_to_impute].isnull()].head()
    return dataframe
def get_model_features():
    feature_to_use_for_imputing_dict={} #dictionary holds which features should be used to impute which features
    feature_to_use_for_imputing_dict["Life expectancy"] = ["Schooling", "Adult Mortality", "Income composition of resources"]
    feature_to_use_for_imputing_dict["Adult Mortality"] = ["Life expectancy"]
    feature_to_use_for_imputing_dict["Income composition of resources"] = ["Life expectancy","Schooling"]
    feature_to_use_for_imputing_dict["Immunization coverage"] = ["Life expectancy", "Schooling"]
    feature_to_use_for_imputing_dict["percentage expenditure"] = ["GDP"]
    feature_to_use_for_imputing_dict["GDP"] = ["percentage expenditure"]
    feature_to_use_for_imputing_dict["Schooling"] = ["Life expectancy", "Income composition of resources"]
    
    return feature_to_use_for_imputing_dict
def clean_up_life_expectancy(life_expectancy_df_melted):
    #get model features
    feature_to_use_for_imputing_dict = get_model_features()
    #0 = developing only
    #1= both
    need_to_impute_for_which =[0,0,1,1,1,1,1]
    placeholder_methods =[[0,0,1],[0],[0,0],[0,0],[0],[0],[0,0]]
    i=0
    model_types_for_each_feature =["LR", "LR", "LR", "KNN", "LR","LR","LR"]
    #loop over model features
    for feature_to_impute in feature_to_use_for_imputing_dict:
        
        status_to_impute_for = need_to_impute_for_which[i]
        
        placeholder_methods_array = placeholder_methods[i]
        
        model_features = feature_to_use_for_imputing_dict[feature_to_impute]
        
        developing_dataframe_processed = preprocess_dataframe("Developing",life_expectancy_df_melted,model_features, feature_to_impute, model_types_for_each_feature[i], placeholder_methods_array)
        
        column_to_replace = feature_to_impute+"_imputed" 
        
        columns_to_drop = [feature_preprocessed + "_temp" for feature_preprocessed in model_features]
        temp_col_header_of_feature = feature_to_impute+"_temp"
        columns_to_drop.append(temp_col_header_of_feature)
        columns_to_drop.append(feature_to_impute)
        #print(columns_to_drop)
        
        original_dataframe = merge_dataframes(developing_dataframe_processed,life_expectancy_df_melted, columns_to_drop, column_to_replace, feature_to_impute, "Developed")
        life_expectancy_df_melted = original_dataframe
        
        if(status_to_impute_for == 1):
            
            developed_dataframe_processed = preprocess_dataframe("Developed",life_expectancy_df_melted,model_features, feature_to_impute, model_types_for_each_feature[i], placeholder_methods_array)
            original_dataframe = merge_dataframes(developed_dataframe_processed,life_expectancy_df_melted, columns_to_drop, column_to_replace, feature_to_impute, "Developing")
            
        life_expectancy_df_melted = original_dataframe
        #print(life_expectancy_df_melted.columns, "Main")
        
        i  =i +1
    return life_expectancy_df_melted
def outlier_detection(clean_life_expectancy_df):
    life_separated = [y for x, y in clean_life_expectancy_df.groupby('Country', as_index=False)]
    #display(life_separated[0]) #separate the df by country
    for i in range(0, len(life_separated)):
        life_copy = (life_separated[i]).copy(deep = True)
        life_copy.loc[life_copy["Adult Mortality"].median() - life_copy["Adult Mortality"]  >= life_copy["Adult Mortality"] * 10 , ["Adult Mortality"]] =life_copy["Adult Mortality"].median()
        life_separated[i]=life_copy

    life_expectancy_corrected = pd.DataFrame()
    for df in life_separated:
        life_expectancy_corrected=pd.concat([life_expectancy_corrected, df])
    return life_expectancy_corrected

        
           
def clean_data(**kwargs):
    life_expectancy_df = pd.read_csv('c/Users/ahmed/data/Life Expectancy Data.csv')
    tidy_life_expectancy_df = tidy_life_expectancy(life_expectancy_df)
    corrected_life_expectancy_df = turn_inaccurate_to_nan(tidy_life_expectancy_df)
    life_expectancy_df_melted = correct_data(corrected_life_expectancy_df)
    life_expectancy_df_melted_copy = life_expectancy_df_melted.copy(deep= True)
    clean_life_expectancy_df = clean_up_life_expectancy(life_expectancy_df_melted_copy)
    life_expectancy_corrected = outlier_detection(clean_life_expectancy_df)
    life_expectancy_corrected.to_csv('c/Users/ahmed/Cleaned_data/Life Expectancy Data.csv')