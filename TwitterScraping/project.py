import streamlit as st
from datetime import datetime
import snscrape.modules.twitter as sntwitter
import pandas as pd
import pymongo
from datetime import date,timedelta


def scraped_data(keyword,limit,start_date,end_date):
    
    # Creating list to append Scrapped data 
    tweets_list = []
    
    # Using TwitterSearchScraper to scrape data and append tweets to list
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'{keyword} since:{start_date} until:{end_date}').get_items()):                 

        if i>limit:
            break
        tweets_list.append([tweet.user.username,tweet.user.id,tweet.id,tweet.date,tweet.rawContent,
                 tweet.url,tweet.source,tweet.lang,tweet.replyCount,tweet.retweetCount,tweet.likeCount])
        
        
    # Creating a dataframe from the tweets list 
    Tweets_df = pd.DataFrame(tweets_list, columns=['Username','User_ID','Tweet Id','Datetime', 'Text',
                    'Url','Source','Language','ReplyCount','RetweetCount','LikeCount'])
        
    return Tweets_df    
        


# Making a Connection with MongoClient
client = pymongo.MongoClient("mongodb://localhost:27017/")
# creating database
db = client["Twitter1"]
def upload(df,keyword):
    # creating new collection
    col= db[f'{keyword}Tweets']
    # Converting the dataframe into list of dict
    Tweets_dict = df.to_dict("records")
    # Inserting the list of dict into database collection
    col.insert_many(Tweets_dict)
    
  
#Input features of web app:
Keyword=st.text_input("Enter the keyword to scrape from Twitter")

Starting_date=st.date_input("Tweets belonging from(starting date):")
    
Ending_date=st.date_input("Tweets upto(Ending date):")
    
Tweets_counts=st.number_input("How much tweets you want to scrape(max 10000):")
    
    
tab1, tab2, tab3, tab4 = st.tabs(["Scrape", "Upload", "Download","Saved"])

# Scraping the data and displaying it
with tab1:
    if st.button("Show"):
        Tweets = scraped_data(Keyword, Tweets_counts, Starting_date, Ending_date)
        st.dataframe(Tweets)

# Uploading the scraped data in database
with tab2:
    if st.button("Upload"):
        Tweets = scraped_data(Keyword, Tweets_counts, Starting_date, Ending_date)
        upload_to_db=upload(Tweets,Keyword)
        st.success("Tweets are uploaded Successfully")
    
# Downloading the scraped data in deirable formats:
with tab3:
    #For Downloading csv file
    col1,col2=st.columns(2)
    Tweets = scraped_data(Keyword, Tweets_counts, Starting_date, Ending_date)
    Tweets_csv=Tweets.to_csv().encode('utf-8')
    col1.download_button("Download CSV file",data=Tweets_csv,file_name=f'{Keyword}.csv',mime='text/csv')

    #For Downloading json file
    Tweets = scraped_data(Keyword, Tweets_counts, Starting_date, Ending_date)
    Tweetsjson=Tweets.to_json(orient ='records')
    col2.download_button("Download JSON file",data=Tweetsjson,file_name=f'{Keyword}.json',mime='application/json')
with tab4:
    #Dispalying already saved files
    st.write('Uploaded Datasets: ')
    for i in db.list_collection_names():
        mycollection=db[i]        
        if st.button(i):            
            df = pd.DataFrame(list(mycollection.find()))
            st.dataframe(df)
                             
      
