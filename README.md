# CSEN1095-W20-Project
This a template repository for the CSEN1095 project winter 2020. It contains the data that will be used in this project. 
Good luck :)

# Overview of the datasets used
## Life expectancy dataset

Life expectancy dataset is a dataset that aims to collect records of life expectancy of many developing and developing countries around the world. The dataset also collects different factors that are thought to affect general health. The factors include demographic factors as well as immunization records. It contains more records of more than a 100 countries from the years 2000-2015.

## 250 country data

Collected using web scraping techniques, this dataset aims to collect general information from the internet about 250 countries. The features collected include region, subregion, area and population. 

## World happiness dataset

This is a collection of 5 datasets files (records spanning 2015 -2019) that record information about how happy different countries are and what they believe influences their happiness. There are 7 factors considered such as: social support, freedom to make life decisions, and healthy life expectancy and more. It also ranks countries from happiest to saddest and gives an overall happiness score.

# Project goal and overview

The goal of the project is to explore general demographic factors and draw insights about them. We explore demographic features between developing and developed countries, and investigate how similar or different the 2 categories are.
We explore health factors as well as question how individuals who live in very different circumstances and regions think. Does the place and conditions affect what we value? This was the motive for our research question that compares which factors affect happiness the most in developing and developed countries. Would people living in developing countries define happiness and view factors contributing to it the same way as people  living in developed countries?
Furthermore we explore how immunization decisions made by governments affect other aspects of life and how life expectancy changes across the years in each region.  We also explore how healthcare quality changes with region, and to be able to get a general overview of the healthcare quality in a region we engineer a new feature that is the division of scaled life expectancy and scaled adult mortality. The inspiration for this question was to study whether living in a certain region equates confidence in being able to receive high quality healthcare. Furthermore, we wanted to investigate if living in crowded areas affected the general happiness of a population. Therefore we engineered a new feature that represents how densely packed a country is. We define density as the population divided by the area of the country. We then use this feature and explore how happiness changes with density. We generalise this question to include studying whether some regions are happier than the others, so we compare the happiness across regions.

# Steps used for the work done

The general way that we handled work on the datasets, was to define first our research questions goals, and weighing the importance of each column in the datasets in terms of answering our questions. Next we started to tidy the data. After obtaining a tidy dataframe we would start looking at the missing values and deciding whether to drop them or not. Furthermore if we chose to keep a missing value, how can we possibly impute it? After obtaining a clean dataframe we would start outlier detection and decide whether the outlier points are valid points or errors in data that should be removed or imputed. After these steps the data was ready to be used in answering questions. When we would start answering a question, we would analyse which datasets the question needs. Then we would analyse the question that we need to answer and determine which datasets to be used.

# Data exploration questions:

1. What affects the happiness of developing and developed countries the most? Comparison of how much the factors impact happiness in this 2 categories over from 2015 => 2019.
2. What is the difference in immunization trends in developing VS developed countries? Study of how do the immunization strategies affect the life of individuals.
3. How does the healthcare quality change across different regions and subregions? 
4. How does life expectancy in each region change across the years? This gives us insights about how general health changes across years.
5. Exploring the relation between region and happiness across the years. Are some regions happier than others?
6. How does density affect happiness? Density is population divided by area and it represents how much a country is packed


# Airflow
The dag folder contains the dag for pipline ccleaning and merging, The path in the dags need to be renamed to work

# Running the project
First, run the cleaning files(country_cleaning, life_cleaninf,..etc)
Second, run the integration file.
Third run the research questions files to see the insights.
