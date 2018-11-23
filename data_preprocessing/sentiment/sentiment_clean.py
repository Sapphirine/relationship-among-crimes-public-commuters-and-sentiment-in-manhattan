import pandas as pd #import pandas
import numpy as numpy #import numpy
from sklearn.utils import shuffle # to shuffle the data 
import random # import random
import sklearn # import sklearn
import nltk # import nltk
from nltk.corpus import stopwords #import stop words
import re # import regular expression
from nltk.tokenize import word_tokenize # import word_tokenize
import matplotlib
import matplotlib.pyplot as plt #import matplotlib.pyplot 

def data_clean_up():
    df = pd.read_csv("./training.1600000.processed.noemoticon.csv", encoding='latin-1', header=None) #read csv file without header as dataframe
    from sklearn.feature_extraction.text import TfidfVectorizer #  import TF-idf vectorizer

    df.columns = ["sentiment", "id", "date", "query", "user", "text"]
    df = df.drop(["sentiment", "id", "query", "user"], axis = 1)

    import re
    from bs4 import BeautifulSoup
    from nltk.tokenize import WordPunctTokenizer
    tok = WordPunctTokenizer()

    pat1 = r'@[A-Za-z0-9_]+'        # remove @ mentions fron tweets
    pat2 = r'https?://[^ ]+'        # remove URL's from tweets
    combined_pat = r'|'.join((pat1, pat2)) #addition of pat1 and pat2
    www_pat = r'www.[^ ]+'         # remove URL's from tweets
    negations_dic = {"isn't":"is not", "aren't":"are not", "wasn't":"was not", "weren't":"were not",   # converting words like isn't to is not
                    "haven't":"have not","hasn't":"has not","hadn't":"had not","won't":"will not",
                    "wouldn't":"would not", "don't":"do not", "doesn't":"does not","didn't":"did not",
                    "can't":"can not","couldn't":"could not","shouldn't":"should not","mightn't":"might not",
                    "mustn't":"must not"}
    neg_pattern = re.compile(r'\b(' + '|'.join(negations_dic.keys()) + r')\b')

    def tweet_cleaner(text):  # define tweet_cleaner function to clean the tweets
        soup = BeautifulSoup(text, 'lxml')    # call beautiful object
        souped = soup.get_text()   # get only text from the tweets 
        try:
            bom_removed = souped.decode("utf-8-sig").replace(u"\ufffd", "?")    # remove utf-8-sig codeing
        except:
            bom_removed = souped
        stripped = re.sub(combined_pat, '', bom_removed) # calling combined_pat
        stripped = re.sub(www_pat, '', stripped) #remove URL's
        lower_case = stripped.lower()      # converting all into lower case
        neg_handled = neg_pattern.sub(lambda x: negations_dic[x.group()], lower_case) # converting word's like isn't to is not
        letters_only = re.sub("[^a-zA-Z]", " ", neg_handled)       # will replace # by space
        words = [x for x  in tok.tokenize(letters_only) if len(x) > 1] # Word Punct Tokenize and only consider words whose length is greater than 1
        return (" ".join(words)).strip() # join the words

    nums = [0,400000,800000,1200000,1600000] # used for batch processing tweets
    clean_tweet_texts = [] # initialize list
    for i in range(nums[0],nums[4]): # batch process 1.6 million tweets                                                               
        clean_tweet_texts.append(tweet_cleaner(df['text'][i]))  # call tweet_cleaner function and pass parameter as all the tweets to clean the tweets and append cleaned tweets into clean_tweet_texts list'

    clean_text = pd.Series(clean_tweet_texts)
    df['clean_text'] = clean_text.values
    df = df.drop(["text"], axis=1)
    df.to_csv("clean_twitter.csv", index=False)


def convert_datetime():
    import datetime
    df = pd.read_csv("clean_twitter.csv")
    nums = [0,400000,800000,1200000,1600000] # used for batch processing tweets
    day = [] # initialize list
    hour = []
    for i in range(nums[0],nums[4]): # batch process 1.6 million tweets
        dt = datetime.datetime.strptime(df["date"][i].split('PDT')[0].strip(), "%a %b %d %H:%M:%S")
        day.append(dt.weekday())
        hour.append(dt.hour)

    day_se = pd.Series(day)
    hour_se = pd.Series(hour)

    df["day"] = day_se.values
    df["hour"] = hour_se.values

    df = df.drop("date", axis=1)
    df = df[["day", "hour", "clean_text"]]
    df.to_csv("clean_twitter_day_hour.csv", index=False)

def calculate_sentiment():
    from textblob import TextBlob
    df = pd.read_csv("clean_twitter_day_hour.csv")
    df = df.dropna()
    df = df.reset_index(drop=True)
    sentiment = [] # initialize list
    for i in range(len(df)): # batch process 1.6 million tweets
        text = df["clean_text"][i]
        blob = TextBlob(text)
        sentiment.append(blob.polarity)
    
    sentiment_se = pd.Series(sentiment)
    df["sentiment"] = sentiment_se
    df = df.drop("clean_text", axis=1)
    df.to_csv("clean_twitter_day_hour_senitment.csv", index=False)

def aggregate_sentiment():
    df = pd.read_csv("clean_twitter_day_hour_senitment.csv")
    new_dict = {}

    idx = 0 
    for dd in range(7):
        for hh in range(24):
            new_dict[idx] = {}
            new_dict[idx]["day"] = dd
            new_dict[idx]["hour"] = hh
            new_dict[idx]["negative"] = len(df[(df["day"] == dd) & (df["hour"] == hh) & (df["sentiment"] < -0.25)])
            new_dict[idx]["neutral"] = len(df[(df["day"] == dd) & (df["hour"] == hh) & (df["sentiment"] >= -0.25) & (df["sentiment"] <= 0.25)])
            new_dict[idx]["positive"] = len(df[(df["day"] == dd) & (df["hour"] == hh) & (df["sentiment"] > 0.25)])

            idx += 1

    new_df = pd.DataFrame.from_dict(new_dict)
    new_df = new_df.T
    new_df.to_csv("sentiment_number.csv", index=False)
    

def aggregate_sentiment_percentage():
    df = pd.read_csv("sentiment_number.csv")

    negative_per = []
    neutral_per = []
    positive_per = []
    for i in range(len(df)):
        total = df["negative"][i] + df["neutral"][i] + df["positive"][i]
        negative_per.append(df["negative"][i] / total)
        neutral_per.append(df["neutral"][i] / total)
        positive_per.append(df["positive"][i] / total)

    negative_per_se = pd.Series(negative_per)
    neutral_per_se = pd.Series(neutral_per)
    positive_per_se = pd.Series(positive_per)

    df = df.drop(["negative", "neutral", "positive"], axis=1)
    df["negative"] = negative_per_se
    df["neutral"] = neutral_per_se
    df["positive"] = positive_per_se

    df.to_csv("sentiment.csv", index=False)

if __name__ == "__main__":
    # data_clean_up()
    # convert_datetime()
    # calculate_sentiment()
    # aggregate_sentiment()
    aggregate_sentiment_percentage()
