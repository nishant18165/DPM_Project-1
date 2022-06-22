# Twitter Data Sentiment Analysis
## Introduction
In this project we have made a web based platform to find the sentiment of people on social media(Twitter) towards a particular subject.

## Motivation
In our generation the social media is a place where most people spend large amounts of time, so to get the mood/feeling of the people towards a particular topic it is useful to have a system by using which we can get the sentiment of the masses about topics.  

## Uses of sentiment analysis:
- Used in Decision Making for an organisation to analyse the market
- Brand Reputation Management 
- To find Voice of Voters 
- Used in Online Commerce 
- Can be used in efficient Governance 

## Details
  ### Data
  To get Twitter data we have used python Tweepy Api library. Tweepy is an open-sourced, easy-to-use Python library for accessing the Twitter API. It gives you an interface to access the API from your Python application.
  ### Data Processing 
  After getting data using Tweepy interface we have removed all the special characters and stopwords with the help of nltk library and then make dataframes of the tweets so that it can be easily and fastly accessed.
  ### Sentiments Prediction 
  Now we have got the preprocessed data so we applied TextBlob(
Image result for textblob
TextBlob is a Python (2 and 3) library for processing textual data. It provides a simple API for diving into common natural language processing (NLP) tasks such as part-of-speech tagging, noun phrase extraction, sentiment analysis, classification, translation, and more) to get the sentiment of the tweet data


## Web Based Platform 
To provide a interface to easily use this sentiment analysis thing we have made a flask based website for backend and for front end we have use HTML and CSS.

## Link of Website
[Sentiment Analysis Tool](https://dpm-sentiment-analysis.herokuapp.com/)
