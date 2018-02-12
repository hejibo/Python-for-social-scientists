# -*- coding: utf-8 -*-
# based on paper "Human language reveals a universal positivity bias"



from nltk.corpus import stopwords
import pandas as pd
import numpy as np
import pylab as plt
from nltk.stem.snowball import SnowballStemmer
from labMTsimple.storyLab import emotionFileReader, emotion, stopper, emotionV
import string
from dateutil.parser import parse

#Download corpora if you haven't downloaded before (otherwise comment lines below)
import nltk
nltk.download()

def get_happiness_raw(string_study,lang="english"):
    """
    Available languages: german      portuguese arabic   hindi   russian chinese  indonesian  spanish english  korean      urdu french   pashto
    """

    from labMTsimple.storyLab import emotionFileReader, emotion, stopper, emotionV
    labMT,labMTvector,labMTwordList = emotionFileReader(stopval=0.0,lang=lang,returnVector=True)

    #Then we can score the text and get the word vector at the same time:
    Valence,Fvec = emotion(string_study,labMT,shift=True,happsList=labMTvector)
   
    return Valence

def get_happiness_delete_neutral(string_study,lang="english"):
    """
    Available languages: german      portuguese arabic   hindi   russian chinese  indonesian  spanish english  korean      urdu french   pashto
    """

    from labMTsimple.storyLab import emotionFileReader, emotion, stopper, emotionV
    labMT,labMTvector,labMTwordList = emotionFileReader(stopval=0.0,lang=lang,returnVector=True)

    #Then we can score the text and get the word vector at the same time:
    Valence,Fvec = emotion(string_study,labMT,shift=True,happsList=labMTvector)
    StoppedVec = stopper(Fvec,labMTvector,labMTwordList,stopVal=1.0)
    Valence = emotionV(StoppedVec,labMTvector)
    
    return Valence
#Delete punctuation
def remove_punctuation(string_to_remove):
    transtable = {ord(c): None for c in string.punctuation}
    return string_to_remove.translate(transtable).lower()

def remove_stop_words(text):
    text = ' '.join([word for word in text.split() if word not in cached_stop])
    return text

def stem_string(string_to_stem,language="english"):
    from nltk.stem.snowball import SnowballStemmer
    stemmer = SnowballStemmer(language)
    return " ".join([stemmer.stem(word) for word in string_to_stem.split(" ")])


def dates_vs_yvalues(df,column_ys,column_dates,groupbyday = True,filter_zeros=True,color="",smoothing=2/3,print_points=True,label=""):
    from statsmodels.nonparametric.smoothers_lowess import lowess
    try: df[column_dates] = df[column_dates].apply(lambda x: parse(x,yearfirst=True,dayfirst=dayfirst))
    except: pass

    
    if filter_zeros:
        df = df.loc[df[column_ys]>0,:]
    
    if groupbyday:
        df = df.groupby(column_dates).mean().reset_index()
        
    y = lowess(df[column_ys],df[column_dates],frac=smoothing,return_sorted=False)
    
    if color:
        plt.plot(df[column_dates],y,color=color,label=label)
        if print_points:
            plt.plot(df[column_dates],df[column_ys],"o",color=color)
    else:
        plt.plot(df[column_dates],y,label=label)
        if print_points:
            plt.plot(df[column_dates],df[column_ys],"o")    


## Sentiment analysis
"""
Available languages: 
german       portuguese 
arabic       hindi   
russian      chinese  
indonesian   spanish 
english      korean      
urdu         french   
pashto  """
    
language = "spanish"
filenames = ["./data/Pedro_Sanchez_PSOE.csv","./data/Pablo_Iglesias_Podemos.csv","./data/Albert_Rivera_Ciudadanos.csv","./data/Mariano_Rajoy_PP.csv"]

separator_csv = "\t" #tab
header = None
index_col = None 
columns_csv = ["Date","Newspaper","Article"]
column_text = "Article" #leave empty to not get the valence
column_date = "Date" #leave empty to not parse the date
dayfirst = False
extra_stop_words = [_.lower() for _ in ["Podemos","Pablo","Iglesias","Ciudadanos","Albert","Rivera","Pedro","Sánchez","PSOE","Mariano","Rajoy","PP"]]

cached_stop = set(stopwords.words(language) + extra_stop_words)
    
## Fill up
for filename in filenames:
    print(filename)
    df = pd.read_csv(filename,sep=separator_csv,header=header,index_col=index_col)
    df.columns = columns_csv
    df = df.drop_duplicates(subset=[column_text])
    
    if column_text:
        valences_articles = []
        for article in df[column_text]:
            try:
                t_article = remove_punctuation(article)
                t_article = remove_stop_words(t_article)
                #t_article = stem_string(t_article)
                valence = get_happiness_delete_neutral(t_article,language)
            except: 
                valence = np.NaN
            valences_articles.append(valence)
        df["Valence"] = valences_articles

    if column_date:
        dates = []
        for date in df[column_date]:
            try:
                date = parse(date,fuzzy=True,dayfirst=dayfirst)
            except: 
                date = pd.NaT
            dates.append(date)
        df["Date_parsed"] = dates

    df.to_csv(filename[:-4]+"_formatted.csv",sep=separator_csv,index=index_col)

