![TS](https://user-images.githubusercontent.com/121713702/220956201-c4f38d16-cf71-4ef8-8e5b-109edc1af9c8.png)


# What is Twitter Scraping?
  Scraping is a technique to get information from Social Network sites. Scraping Twitter can yield many insights into sentiments, opinions and social media trends. Analysing tweets, shares, likes, URLs and interests is a powerful way to derive insight into public conversations.
  It is legal to scrape Twitter or any other SNS(Social Networking Sites) to extract publicly available information, but you should be aware that the data extracted might contain personal data.
  
# How to Scrape the Twitter Data?
  Scraping can be done with the help of many opensource libraries like 
	
  1. Tweepy
  2. Twint
  3. Snscrape
  4. Getoldtweets3
  
  For my project I have used SNSCRAPE library.
   
# Libraries and Modules needed for the project!

 1. snscrape.modules.twitter - (To Scrape the Data from Twitter)
 2. Pandas - (To Create a DataFrame with the scraped data)
 3. Pymongo - (To upload the dataframe to MongoDB database)
 4. Streamlit - (To Create Graphical user Interface)
 5. Datetime - (To get the current date)
	

# Snscrape
  Snscrape allows you to scrape basic information such as a user's profile, tweet content, source, and so on. Snscrape is not limited to Twitter, but can also scrape content from other prominent social media networks like Facebook, Instagram, and others. Its advantages are that there are no limits to the number of tweets you can retrieve or the window of tweets (that is, the date range of tweets). So Snscrape allows you to retrieve old data.

# Streamlit
  Streamlit is an open source app framework in Python language. It helps us create web apps for data science and machine learning in a short time. It is compatible with major Python libraries such as scikit-learn, Keras, PyTorch, SymPy(latex), NumPy, pandas, Matplotlib etc. Streamlit allows you to re-use any Python code you have already written. This can save considerable amounts of time compared to non-Python based tools where all code to create visualizations needs to be re-written.
  
  In my project I've extensively used streamlit API Reference feature for creation of Titles, Images, Headers, Input boxes, Buttons, Checkbox, Download buttons.
 
  To know more about Streamlit do visit the official site- https://docs.streamlit.io/library/api-reference
  
# Workflow
  Lets us see the workflow of the twitter scraping project by breakingdown it step by step.
  
  ### To view the demo video of my project checkout this link - https://www.linkedin.com/posts/jafar-hussain-1bbb6313a_project-share-video-activity-7036613421672390656-wHKX?utm_source=share&utm_medium=member_desktop
  
### Step 1
  Importing the libraries.
  As I have already mentioned above the list of libraries/modules needed for the project. First we have to import all those libraries. Before that check if the libraries are already installed or not by using the below piece of code.
  	
	!pip install ["Name of the library"]
	
  If the libraries are already installed then we have to import those into our script by mentioning the below codes.
  	
	import snscrape.modules.twitter as sntwitter
	import pandas as pd
	import pymongo
	import streamlit as st
	from datetime import date	
### Step 2
  Getting inputs from the user. In the below code I have created the list of variables for getting user input. In the below codes st.sidebar denotes the streamlit user interface menu. With the help of streamlit I've also created the input boxes like text_input, number_input, date_input.
  
  1. Keyword or Hashtag the user needed to search for **(hashtag)**
  2. Number of tweets the user wants to scrape **(tweets_count)**
  3. Tweets posted since date **(start_date)**
  4. Tweets posted until date **(end_date)**
  5. Date when the user is scraping the tweets **(today)**. Im getting this date with the help of **datetime** module 
  
	hashtag = st.sidebar.text_input("Enter the keyword or Hashtag you need to get : ")
	tweets_count = st.sidebar.number_input("Enter the number of Tweets to Scrape : ", min_value= 1, max_value= 1000, step= 1)
	start_date = st.sidebar.date_input("Start date (YYYY-MM-DD) : ")
	end_date = st.sidebar.date_input("End date (YYYY-MM-DD) : ")
	today = str(date.today())

### Step 3
  After getting user inputs. In the next step I've created an empty list **(tweets_list)** so that we are going to append the scraped tweets from the twitter. Then with the streamlit library I've created the checkbox **(Scrape Tweets)**. 
  
   With the help of for loop and enumerate function im getting the variety of information from twitter. The method I've used is **sntwitter.TwitterSearchScraper** which helps in getting informations like date, id, rawContent, username, replyCount, retweetCount, likeCount, language, source and etc.
   
   The loop will run till the iteration reaches the count provided b the user. Then these details are getting appended to the list called **(tweets_list)**.The tweets will only get scraped if the proper input is provided and also check box is checked.


	tweets_list = []
	# Enabling the Checkbox only when the hashtag is entered
	if hashtag:
	    st.sidebar.checkbox("**Scrape Tweets**")

	    # Using for loop, TwitterSearchScraper and enumerate function to scrape data and append tweets to list
	    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f"{hashtag} since:{start_date} until:{end_date}").get_items()):
		if i >= tweets_count:
		    break
		tweets_list.append([tweet.date,
				    tweet.id,
				    tweet.url,
				    tweet.rawContent,
				    tweet.user.username,
				    tweet.replyCount,
				    tweet.retweetCount,
				    tweet.likeCount,
				    tweet.lang,
				    tweet.source
				   ])
	else:
	    st.sidebar.checkbox("**Scrape Tweets**",disabled=True)

### Step 4
  1. The first function is used to create the **Pandas DataFrame** using the datas that was appended to **tweets_list = []**. Column names were provided as per my need.
  2. Second function is to convert the DataFrame object into a CSV file using **to_csv()** function.
  3. The last function is to convert the DataFrame object into a JSON file using **to_json()** function.
  
  
	# Creating DataFrame with the scraped tweets
	def data_frame(data):
	    return pd.DataFrame(data, columns= ['datetime', 'user_id', 'url', 'tweet_content', 'user_name',
						 'reply_count', 'retweet_count', 'like_count', 'language', 'source'])

	# Converting DataFrame to CSV file
	def convert_to_csv(c):
	    return c.to_csv().encode('utf-8')

	# Converting DataFrame to JSON file
	def convert_to_json(j):
	    return j.to_json(orient='index')

  Here is the object creation with different variable names of all the above three functions. This will act as the driver code for function execution.

	# Creating objects for dataframe and file conversion
	df = data_frame(tweets_list)
	csv = convert_to_csv(df)
	json = convert_to_json(df)
	    
### Step 5
  Bridging the connection between MongoDB and Python. For this we would need the **pymongo** library and the **.MongoClient** attribute. After successful connection I've created the database named **twitterscraping** and collection named **scraped_data**. We are going to store all the scraped datas in this collection.
  
  The **scr_data** is going to hold the basic informations like Scraped word, date scraped and scraped data. Then these details are uploded into the MongoDB collection.
  
  
	client = pymongo.MongoClient("mongodb+srv://jafarhussain:1996@cluster0.4gaz2ol.mongodb.net/?retryWrites=true&w=majority")
	db = client.twitterscraping
	col = db.scraped_data
	scr_data = {"Scraped_word" : hashtag,
		    "Scraped_date" : today,
		    "Scraped_data" : df.to_dict('records')
		   }
### Step 6
  Here comes the importance of streamlit in my project. I have created four buttons overall for this project.
  
  The first button is used to view the dataframe. Once the user clicks this button the df function is called and then dataframe will appear in the screen along with the success message as ✅DataFrame Fetched Successfully. 
  
	# BUTTON 1 - To view the DataFrame
	if st.button("View DataFrame"):
	    st.success("**:blue[DataFrame Fetched Successfully]**", icon="✅")
	    st.write(df)

  Once the **Upload the data to MongoDB** button is clicked by the user the **scr_data** which we have already created is getting uploaded to the MongoDB collection.
delete_many will delete the previous records from the collection and then the new records is getting inserted with the help of insert_one function. And finally the user will get the success message ✅Upload to MongoDB Successful! in their screen.

  If the user clicks this button without scraping the data the error message will be popped like **You cannot upload an empty dataset. Kindly enter the information in the leftside menu.**
  
	# BUTTON 2 - To upload the data to mongoDB database
	if st.button("Upload the data to MongoDB"):
	    try:
		col.delete_many({}) #Deleting old records from the collection
		col.insert_one(scr_data)
		st.success('Upload to MongoDB Successful!', icon="✅")
	    except:
		st.error('You cannot upload an empty dataset. Kindly enter the information in the leftside menu.', icon="🚨")

  The simple streamlit subheader that denotes the downloading options of the scraped data.
  
	# Header Diff Options to download the dataframe
	st.subheader("**:blue[To download the data use the below buttons :arrow_down:]**")

  These below two buttons are used to generate CSV or JSON files as per the user wish. In the backend the conver_to_csv or conver_to_json is called and executed. User will get the CSV file or JSON file downloaded to their downloads.
  
	# BUTTON 3 - To download data as CSV
	st.download_button(label= "Download data as CSV",
			   data= csv,
			   file_name= 'scraped_tweets_data.csv',
			   mime= 'text/csv'
			  )

	# BUTTON 4 - To download data as JSON
	st.download_button(label= "Download data as JSON",
			   data= json,
			   file_name= 'scraped_tweets_data.json',
			   mime= 'text/csv'
			  )
  
  
  To run this script go to the Terminal and type the below command, you will get a new window opened in your browser there we can interact with the streamlit user interface.
    
    	streamlit run Twitter_Scraping.py
  
  
  
  
  
  
