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
#import nltk
#nltk.download()

def make_line_hist(x,minValue,maxValue,nbins=10,logscale=False):
    """
    make a line histogram (instead of bars, just the top line)
    """
    if logscale:
        freqs,bins = np.histogram(x,bins=np.logspace(np.log10(minValue),np.log10(maxValue),nbins),normed=True) 
    else:
        freqs,bins = np.histogram(x,bins=np.linspace(minValue,maxValue,nbins),normed=True)
        
    
    plt.plot((bins[:-1]+bins[1:])/2,freqs)
    return freqs

def correlation(x,y,typeCorr="pearson"):
    from scipy.stats import pearsonr, spearmanr
    if typeCorr == "pearson":
        corr,p_value = pearsonr(x,y)
    else:
        corr,p_value = spearmanr(x,y)
    
    print("Correlation: {0:2.2g}. P-value: {1:2.5f}".format(corr,p_value))
    return corr,p_value
    
def cross_correlation(x,y,time):
    """
    Calculates the normalized cross-correlation and plots it
    """
    import numpy as np
    modeC = "same"
    x = (x - np.mean(x))/np.std(x)
    y =  (y - np.mean(y))/np.std(y)

    timeInt = np.diff(time).mean().days
    numPoints = len(x)
    fig = plt.figure(figsize=(6,3.5))        
    d = np.correlate(y,x,modeC)

    plt.plot([0,0],[-0.5,1],color="grey")
    plt.xlabel("Lag")
    plt.ylabel("Correlation")
    plt.plot(np.linspace(len(x)/2*timeInt,-len(x)/2*timeInt,len(x)),d/numPoints)
    plt.show()

def compare_samples(populations,parametric=False):
    """
    check if the samples come from the same population or not
    """
    from scipy.stats import mannwhitneyu, ttest_ind, f_oneway, kruskal, ranksums
    from statsmodels.stats.multicomp import pairwise_tukeyhsd
    populations = [np.array(pop) for pop in populations] #obscure line to take out missing values
    populations = [pop[~np.isnan(pop)]  for pop in populations]

    if len(populations) == 2:
        if parametric:
            stat, p_value = ttest_ind(*populations)
            print("P-value t-test: {0:2.10f}".format(p_value))
        else:
            stat, p_value1 = mannwhitneyu(*populations)
            print("P-value MWW: {0:2.10f}".format(p_value))
            stat, p_value2 = ranksums(*populations)
            print("P-value Ranksum: {0:2.10f}".format(p_value))
    
    if len(populations) > 2:
        if parametric:
            stat, p_value = f_oneway(*populations)
            print("P-value anova: {0:2.10f}".format(p_value))
        else:
            stat, p_value = kruskal(*populations)  
            print("P-value kruskal: {0:2.10f}".format(p_value))
            
        if p_value < 0.05:
            flatten_pop = []
            label_pop = []
            for i,pop in enumerate(populations):
                flatten_pop += list(pop)
                label_pop += ["pop{0}".format(i)]*len(pop)
                    
            res2 = pairwise_tukeyhsd(np.asarray(flatten_pop),label_pop)
            print("Printing pair comparisons using Tukey HSD")
            print(res2)
            res2.plot_simultaneous(comparison_name=None,xlabel='diffs',ylabel='grups')
            
    print(("Means: " + ", {}"*len(populations)).format(*[np.mean(_) for _ in populations]))
    print(("STDs: " + ", {}"*len(populations)).format(*[np.std(_) for _ in populations]))
    
    
    return p_value

def linear_regression(vectors_X,vector_y,variables_names="ABCDEFG",formula="Y ~ A * B"):
    """
    linear_regression
    vectors_X: list of the vectors X
    vector_y: independent variable
    variables_names: whatever you want to name the variables in X 
    formula: formulat to use
    """
    #linear regression
    import pandas as pd
    import statsmodels.formula.api as sm
    d = dict(zip(variables_names,vectors_X))
    d["Y"] = vector_y
             
    df = pd.DataFrame(d)
    result = sm.ols(formula=formula, data=df).fit()
    print(result.summary())
    
    return result.params
    
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
filenames = [r"D:\Python-for-social-scientists\Chapter 17. Social Network Analysis\text_analysis_python-master\\data\Pedro_Sanchez_PSOE.csv",
r"D:\Python-for-social-scientists\Chapter 17. Social Network Analysis\text_analysis_python-master\\data\\Pablo_Iglesias_Podemos.csv",
r"D:\Python-for-social-scientists\Chapter 17. Social Network Analysis\text_analysis_python-master\\data\\Albert_Rivera_Ciudadanos.csv",
r"D:\Python-for-social-scientists\Chapter 17. Social Network Analysis\text_analysis_python-master\\data\\Mariano_Rajoy_PP.csv"]

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

## Plot happiness

print_points = False
smoothing = 0.2
colors = ["#912CEE","orange","#00BFFF","red"] #Watch out, have 
labels = ["Podemos","Ciudadanos","PP","PSOE"]
plt.figure(figsize=(15,5))
column_ys = "Valence"
column_date = "Date_parsed"

valences  = []
for i,filename in enumerate(filenames): #enumerate gives you the index adn the content of the elements in the list   
    df = pd.read_csv(filename[:-4]+"_formatted.csv",sep=separator_csv,index_col=index_col)
    valences.append(df[column_ys].values)
    if (len(colors) >= len(filenames)) and (len(labels) >= len(filenames) ):
        dates_vs_yvalues(df,column_ys,column_date,groupbyday = True,filter_zeros=True,color=colors[i],smoothing=smoothing,print_points=print_points,label=labels[i])
    else:
        dates_vs_yvalues(df,column_ys,column_date,groupbyday = True,filter_zeros=True,smoothing=smoothing,print_points=print_points)        

compare_samples(valences,parametric=True)
elections = parse("Dec 20, 2015")
plt.plot([elections,elections],[6.1,6.3],color="grey")
plt.legend()
plt.show()