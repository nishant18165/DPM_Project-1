from contextlib import redirect_stderr
from bokeh.io import output_notebook, output_file, show
import imdb
from bokeh.plotting import figure,show
from bokeh.embed import components
from bokeh.palettes import Spectral6
from bokeh.models import ColumnDataSource, map_plots
from flask import Flask, render_template
from flask import request, redirect
import tweepy
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from wordcloud import WordCloud, STOPWORDS
from textblob import TextBlob, Word, Blobber
import pandas as pd
import numpy as np
import os
from math import pi
from bokeh.transform import cumsum
import re  # regular expressions
from flask import Flask, render_template, request, send_file, make_response, url_for, Response
import matplotlib.pyplot as plt
import matplotlib



matplotlib.use('Agg')
nltk.download('stopwords')
app = Flask(__name__)

API_Key = "KKkTazbDImIGKH2vSjqdsIKO9"
API_Key_Secret = "aF4URfFXK0t93omcBSUZNXN9qyC36wD3Yy7qG4nLOS3qyi1xst"
Access_Token = "1448641204367683587-lBd07TNTQQFPu7HCbsxY02u3Kc1Q72"
Access_Token_Secret = "3XXClv7oXBEf2kQpiT0CRdgrBN4Lzjxkfi1UW6DdidikX"
auth = tweepy.OAuthHandler(API_Key, API_Key_Secret)
auth.set_access_token(Access_Token, Access_Token_Secret)
api = tweepy.API(auth)

##########################################################
###############################################

def get_tweetsdf(topic,typ):
    tweetList = []
    userList = []
    likesList = []
    datetimeList = []
    locationList = []

    if(typ == 'person'):
        cursor = api.user_timeline(screen_name= topic, 
                           count=200,
                           include_rts = False,
                           tweet_mode = 'extended'
                           )
    else:

        Query = topic + "-filter:retweets"
        cursor = tweepy.Cursor(api.search_tweets, q=Query, lang="en",
                            tweet_mode="extended", exclude="retweets").items(200)
    for t in cursor:
        tweetList.append(t.full_text)
        userList.append(t.user.name)
        likesList.append(t.favorite_count)
        locationList.append(t.user.location)
        datetimeList.append(t.created_at)

    df = pd.DataFrame({"User Name": userList, "Tweets": tweetList, "Likes": likesList,
                       "Date Time": datetimeList, "Location": locationList})
    return df

##########################################################
"""
def getpersonal(userid):
    tweetList = []
    userList = []
    likesList = []
    datetimeList = []
    locationList = []
    #Query = userid +  "-filter:retweets"
    tweets = api.user_timeline(screen_name= userid, 
                           # 200 is the maximum allowed count
                           count=200,
                           include_rts = False,
                           # Necessary to keep full_text 
                           # otherwise only the first 140 words are extracted
                           tweet_mode = 'extended'
                           )
    for t in tweets:
        tweetList.append(t.full_text)
        userList.append(t.user.name)
        likesList.append(t.favorite_count)
        locationList.append(t.user.location)
        datetimeList.append(t.created_at)
        
    df =  pd.DataFrame({"User Name":userList,"Tweets":tweetList,"Likes":likesList,
                            "Date Time":datetimeList,"Location":locationList })
    return df
"""
###################################################

def get_polarity_dataframe(df):
    # Section 1
    tempdf = df
    x = tempdf["Tweets"]

    # to remove stop words(a,an the)

    # to get stem of verb(playing->play)
    stop_words = stopwords.words('english')
    stemmer = PorterStemmer()

    cleaned_text = []
    for i in range(len(x)):
        # substitute empty string where char is not a-zA-Z
        tweet = re.sub('[^a-zA-Z]', ' ', x.iloc[i])
        tweet = tweet.lower().split()

        tweet = [stemmer.stem(word) for word in tweet if (
            word not in stop_words)]  # stemming and remove stop words
        tweet = ' '.join(tweet)
        cleaned_text.append(tweet)

    tempdf["Clean Tweets"] = cleaned_text

    def sentiment_analysis(df):
        def getSubjectivity(text):
            # subjectivity  =1 (personal opinion) =0(factual point)
            return TextBlob(text).sentiment.subjectivity

        # Create a function to get the polarity
        def getPolarity(text):
            return TextBlob(text).sentiment.polarity  # polarity lies [-1,1]

        # Create two new columns ‘Subjectivity’ & ‘Polarity’
        df["Subjectivity"] = df["Clean Tweets"].apply(getSubjectivity)
        df["Polarity"] = df["Clean Tweets"].apply(getPolarity)

        def getAnalysis(score):
            if score <= -0.1:
                return "negative"
            elif score > -0.1 and score < 0.1:
                return "neutral"
            else:
                return "positive"
        df["Polarity_Analysis"] = df["Polarity"].apply(getAnalysis)
        return df

        # Section2
    newdf = sentiment_analysis(tempdf)
    return newdf

###################################################


def get_polarity_plot(topic, p_type, typ='movies'):
    # get dataframe from topic
    
    print(typ)
    df1 = get_tweetsdf(topic=topic,typ = typ)
   
        # get dataframe with polarity columns
    newdf = get_polarity_dataframe(df1)

    posNumber = newdf[newdf["Polarity_Analysis"] == "positive"].shape[0]
    negNumber = newdf[newdf["Polarity_Analysis"] == "negative"].shape[0]
    neuNumber = newdf[newdf["Polarity_Analysis"] == "neutral"].shape[0]

    sentiments = ["Positive", "Negative", "Neutral"]
    total = posNumber + negNumber + neuNumber
    counts = [posNumber, negNumber, neuNumber]
    
    if p_type == "Pie Chart":
        x = {
            'Positive': posNumber,
            'Negative': negNumber,
            'Neutral': neuNumber,
        }
        data = pd.Series(x).reset_index(name='value').rename(
            columns={'index': 'country'})
        data['angle'] = data['value']/data['value'].sum() * 2*pi
        data['color'] = ["seagreen", "#ffa600", "#58508d"]
        # print(data)

        output_file("plot.html")
        p = figure(height=400,width=700, title=f"Pie Chart for sentiments analysis  of latest {total} tweets", toolbar_location=None,
                   tools="hover", tooltips="@country: @value", x_range=(-0.5, 1.0))
        p.wedge(x=0, y=1, radius=0.4,
                start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                line_color="white", fill_color='color', legend_field='country', source=data)
        p.axis.axis_label = None
        p.axis.visible = False
        p.grid.grid_line_color = None
        p.title.align = "center"
        return p
    elif p_type == "Bar Graph":
        source = ColumnDataSource(data=dict(sentiments=sentiments, counts=counts, color=Spectral6))
        p = figure(height=500,width=800,x_range=sentiments, title=f"Bar Graph for sentiments analysis  of latest {total} tweets",
                   toolbar_location=None, tools="hover",tooltips="@sentiments: @counts", x_axis_label="Sentiments", y_axis_label="Tweets Count")
        p.vbar(x='sentiments', top='counts', width=0.8,
               color='color',  source=source)
        p.xgrid.grid_line_color = None
        p.title.align = "center"
        return p


#####################################################
def helper(pold):
    # Wordclod for mixed tweets
    all_tweets = []
    for i in range(len(pold)):
        all_tweets.append(pold.loc[i].Tweets)
    text_all = ' '.join(all_tweets)

    proc1 = re.compile('<.*?>')

    def proc(text_in):
        # Removes HTML Tags and other symbols under proc1
        text_o = re.sub(proc1, '', text_in)
        output = re.sub(r'[^\w\s]', '', text_o)  # Removes URLs from the text
        return output.lower()  # Returns the processed text in lower case

    word_cloud_p_processed = WordCloud(collocations=False, background_color='white').generate(
        proc(text_all))  # Stopwords are removed in this line by 3rd argument
    plt.imshow(word_cloud_p_processed, interpolation='bilinear')
    plt.axis("off")

    # Seperation of +ve and negative tweets
    pos = []
    neg = []
    for i in range(len(pold)):
        if pold.loc[i].Polarity_Analysis == "positive":
            pos.append(pold.loc[i].Tweets)
        elif pold.loc[i].Polarity_Analysis == "negative":
            neg.append(pold.loc[i].Tweets)

    path_static = os.path.join(os.getcwd(), "static/")

    # Wordcloud for +ve Tweets
    text_pp = ' '.join(pos)
    word_cloud_p_processed = WordCloud(collocations=False, background_color='white').generate(
        proc(text_pp))  # Stopwords are removed in this line by 3rd argument
    plt.imshow(word_cloud_p_processed, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0.1)
    plt.savefig(path_static+"wordcld_p.png")

    # Wordcloud for Negative Tweets
    text_nn = ' '.join(neg)
    word_cloud_p_processed = WordCloud(collocations=False, background_color='white').generate(
        proc(text_nn))  # Stopwords are removed in this line by 3rd argument
    plt.imshow(word_cloud_p_processed, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0.1)
    plt.savefig(path_static+"wordcld_n.png")

    # Top 10 +ve tweet dataframe
    top_pos_10 = []
    for i in range(len(pold)):
        if pold.loc[i].Polarity_Analysis == "positive":
            top_pos_10.append(pold.loc[i])
    t10_p = pd.DataFrame(top_pos_10)
    rslt_df_p = t10_p.sort_values(by='Polarity',ascending=False)
    final_p = rslt_df_p.head(10).drop(
        ["Location", "Clean Tweets", "Subjectivity","Likes","Polarity_Analysis"], axis=1)

    # Top 10 -ve tweet dataframe
    top_neg_10 = []
    for i in range(len(pold)):
        if pold.loc[i].Polarity_Analysis == "negative":
            top_neg_10.append(pold.loc[i])
    t10_n = pd.DataFrame(top_neg_10)
    rslt_df_n = t10_n.sort_values(by='Polarity')
    final_n = rslt_df_n.head(10).drop(
        ["Location", "Clean Tweets", "Subjectivity", "Likes","Polarity_Analysis"], axis=1)

    return (final_p, final_n)


#################################################

def remove(string):
    return ("".join(string.split())).lower()


def valid_movie(movie_name):
    # creating instance of IMDb
    ia = imdb.IMDb()
    # searchning the movie
    search = ia.search_movie(movie_name)
    movie_fname = "none"
    # printing the result
    for movie in search:
        if(remove(movie['title']) == remove(movie_name)):
            movie_fname = movie_name
            return (True, movie['title'])
    return (False, "")


################################################

@app.route("/error")
def error():
    return render_template('error.html')



direct = 'none'
@app.route("/", methods=['GET', 'POST'])
def main():
    global direct
    if(request.method == 'POST'):
        print("clicked")
        try:
            direct = request.form['sel']
            if(direct == "movie"):
                return redirect('/movie')
            elif(direct == "subject"):
                return redirect('/subject')
            elif(direct == "person"):
                return redirect('/person')
            else:
                return redirect('/')
        except:
            return render_template('error.html')
    else:
        print("not clicked")
        return render_template('index.html')



###############################################
##sentiment analysis towards a topic/subject
###############################################
final_n=""
final_p=""
@app.route('/subject', methods=['GET', 'POST'])
def subject():
    if(request.method == 'POST'):
        try:
            subject_name = request.form['subject@name']
            # no_tweet=request.form['no@tweet']
            p_type = request.form['p_type']
            pold = get_polarity_dataframe(get_tweetsdf(subject_name,'subject'))
            global final_n,final_p
            final_p,final_n = helper(pold)
            p1 = get_polarity_plot(str(subject_name), str(p_type),'subject')
            demo_script_code, chart_code = components(p1)
            return render_template('result.html', chart_code=chart_code, demo_script_code=demo_script_code,
                               table1=[final_p.to_html(
                                   classes='data1', index=False)],
                               table2=[final_n.to_html(classes='data2', index=False)], titles=final_p.columns.values)
        except:
            return render_template('error.html')

    else:
            print('not clicked subject')
            return render_template('subject.html')

###############################################
##personal tweet sentiment analysis
###############################################

@app.route('/person', methods=['GET', 'POST'])
def personal():
    #name_list=['Narendra Modi','Donald Trump','Joe Biden','Rahul Gandhi','Boris Johnson','Justin Treudo','Scott Morison','Angela Markel','Jacinda Ardern','Cyril Ramaphosa']
    if(request.method == 'POST'):
        try:
            person_id = request.form['user_id']
            result_type = request.form['p_type']
            pold = get_polarity_dataframe(get_tweetsdf(person_id,'person'))
            global final_n,final_p
            final_p, final_n = helper(pold)
            p1 = get_polarity_plot(str(person_id), str(result_type), 'person')
            demo_script_code, chart_code = components(p1)
            return render_template('result.html', chart_code=chart_code, demo_script_code=demo_script_code, titles=final_p.columns.values)
        except:
            return render_template('error.html')

    else:
        print('not clicked personal')
        return render_template('person.html')


##########################################################
# Code for movie sentiment analysis
##########################################################
@app.route('/movie', methods=['GET', 'POST'])
def movie():
    if(request.method == 'POST'):
        try:
            print('clicked movie')
            movie_name = request.form['movie_name']
            result_type = request.form['p_type']
            print(movie_name, result_type)
            tmp = valid_movie(movie_name)
            print(tmp[1])
            if(tmp[0] == True):
                pold = get_polarity_dataframe(get_tweetsdf(tmp[1],'movie'))
                global final_n,final_p
                final_p, final_n = helper(pold)
                p1 = get_polarity_plot(str(tmp[1]), str(result_type),'movie')
                demo_script_code, chart_code = components(p1)
                return render_template('result.html', chart_code=chart_code, demo_script_code=demo_script_code,
                                       table1=[final_p.to_html(
                                           classes='data1', index=False)],
                                       table2=[final_n.to_html(classes='data2', index=False)], titles=final_p.columns.values)
            else:
                return render_template('error.html')
        except:
            return render_template('error.html')
    else:
        print('not clicked movie')
        return render_template('movie.html')

@app.route('/neg')
def negative():
    return render_template('negative.html',table1=[final_n.to_html(
                                   classes='data1', index=False)],titles=final_n.columns.values)


@app.route('/pos')
def positive():
    return render_template('positive.html',table2=[final_p.to_html(classes='data2', index=False)], titles=final_p.columns.values)
if __name__ == "__main__":
    app.run(debug=True)
