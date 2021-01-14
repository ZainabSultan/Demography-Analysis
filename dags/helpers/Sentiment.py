import os
import tweepy as tw
import pandas as pd
import pandas as pd
import numpy as np
from textblob import TextBlob
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()
consumer_key= os.getenv("consumer_key")
consumer_secret= os.getenv("consumer_secret")
access_token= os.getenv("access_token")
access_token_secret= os.getenv("access_token_secret")
def TwitterAnalysis(country,date):
    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)
    places = api.geo_search(query=country, granularity="country")
    date_until = (date+ timedelta(1)).strftime("%Y-%m-%d")
    place_id = places[0].id
    new_search="place:%s" % place_id + " -filter:retweets"
    tweets = tw.Cursor(api.search,
                        q=new_search,
                        lang="en",
                        until=date_until).items(20)
    total=0
    sent=0
    for tweter in tweets:
        blob = TextBlob(tweter.text)
        blob.tags           
        blob.noun_phrases
        for sentence in blob.sentences:
            if(sentence.sentiment.polarity!=0):
                sent+=sentence.sentiment.polarity
                total+=1
    return sent/total

def TwitterPipline(**kwargs):
   root_path = 'c/Users/ahmed/Twitter_Analysis/'
   Twitter_Analysis = pd.read_csv(root_path+'Twitter_Analysis.csv')
   date= kwargs['execution_date']
   country=kwargs['country']
   happiness=TwitterAnalysis(country,date)
   data = {'Happiness Score':happiness,'TimeStamp':date,'Country':country} 
   Twitter_Analysis=Twitter_Analysis.drop(['Unnamed: 0'], axis=1)
   df=Twitter_Analysis.append(data, ignore_index = True)
   df.to_csv(root_path+"Twitter_Analysis.csv")