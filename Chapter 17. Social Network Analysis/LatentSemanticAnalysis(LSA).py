from matplotlib import cm
import lda
import pylab as plt
from collections import Counter
import bisect
import re
import pickle
import string

#Delete punctuation
def remove_punctuation(string_to_remove):
    transtable = {ord(c): None for c in string.punctuation}
    return string_to_remove.translate(transtable).lower()

def remove_stop_words(text,cached_stop):
    text = ' '.join([word for word in text.lower().split() if word not in cached_stop])
    return text

#Remove endings
def stem_string(string_to_stem,language="english"):
    from nltk.stem.snowball import SnowballStemmer
    stemmer = SnowballStemmer(language)
    return " ".join([stemmer.stem(word) for word in string_to_stem.split(" ")])

def bi_contains(lst, item):
    """ efficient `item in lst` for sorted lists """
    pos = bisect.bisect_left(lst, item)
    return [((item <= lst[-1]) and (lst[pos] == item)),pos]

def create_dictionary(lang,cached_stop):
    """
    top 5000 words, using labMTsimple
    """
    from labMTsimple.storyLab import emotionFileReader, emotion, stopper, emotionV
    labMT,labMTvector,labMTwordList = emotionFileReader(stopval=0.0,lang=lang,returnVector=True)
    vocab = sorted(list(set(labMTwordList) - set(cached_stop)))
    pickle.dump(vocab,open('./data/vocab.txt',"wb+"))
    
def create_corpus(all_articles,language="english"):
    """
    create the corpus (a numpy array (kind of a list of lists) with the number of times each word appear among all articles)
    """
    vocab = pickle.load(open('./data/vocab.txt',"rb+"))
    len_vocab = len(vocab)
    print("Number of articles: {0}".format(len(all_articles)))
    allMessages = np.zeros((len(all_articles),len_vocab))
    j = -1
    for mess in all_articles:
        mess = remove_stop_words(remove_punctuation(mess),cached_stop)
        j += 1
        # Kind-of efficient way to count words (better to use a dictionary)
        file = re.split(' |\n',mess)
        c = Counter(file)
        del c['']
        values = np.zeros(len_vocab)
        for word in c:
            pos = bi_contains(vocab, word)
            if pos[0]:
                values[pos[1]] = c[word]
        allMessages[j,:] += values
        
    allMessages = np.array(allMessages,dtype=int)
    pickle.dump(allMessages, open('./data/corpus.dat',"wb+"))

def lda_run(allMessages,vocab,topicNum=10,n_iter=1000):
    """
    run lda with allMessages and print topics
    """
    print(topicNum)
    model = lda.LDA(n_topics=topicNum, n_iter=n_iter, random_state=1)
    
    model.fit(allMessages)
    topic_word = model.topic_word_
    print(model.loglikelihood())
    np.savetxt("./data/ldaTopics"+str(topicNum)+".dat",np.asarray(topic_word))
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:]#-[:n_top_words:-1]
        freq_words = np.array(topic_dist)[np.argsort(topic_dist)][:]#-n_top_words:-1]

        print('Topic {}: {}'.format(i, ' '.join(topic_words[::-1][:5])))
        print('Topic {}: {}'.format(i, ' '.join([str(_) for _ in freq_words[::-1][:5]])))


    doc_topic = model.doc_topic_

    allDisSorted = []
    for i in range(allMessages.shape[0]):
        allDisSorted.append(doc_topic[i])

    allDisSorted = np.asarray(allDisSorted)
    np.savetxt("./data/allDistComb1Day"+str(topicNum)+".dat",allDisSorted)
    return model.loglikelihood()
    

def plotNumTopics(x,y,ax2,loglikelihood=False):
    """
    plot points and the smooth line. if KL divergence then divides the results by comb(x,2) to get the mean 
    """
    from statsmodels.nonparametric.smoothers_lowess import lowess
    import pylab as plt
    from scipy.misc import comb
    x = np.asarray(x)
    if loglikelihood:
        y = np.asarray(y)
    else:
        y = np.asarray(y)/comb(x,2)
            
    a = lowess(y,x,frac = 0.3)
    ax2.plot(x,y,'.',linewidth=2,markersize=7,color='orange')

    ax2.plot(x,a[:,1],color='orange',linewidth=2,label='Distance')
    ax2.set_xlabel('Number of Topics',fontsize=12)
    ax2.set_ylabel('Average distance between topic',fontsize=12)



def find_distances(tit="",retTopics = False):
    """
    Finds the distance between topics using:
    (1) the frequency at which each topic appears every day (topics that always appear in the same dates are probably related) 
    (2) the frequency of words appearing in the topics (topics with the same words are probably related)
    """
    from scipy.stats import pearsonr,spearmanr,kendalltau,entropy
    import pylab as plt
    from scipy.spatial.distance import pdist, squareform
    from scipy.cluster.hierarchy import linkage, dendrogram,leaders,fcluster


    def KL_H(u,v):
        return entropy(u,v)*entropy(v,u)/entropy(u)/entropy(v)


    varValues = np.transpose(np.loadtxt("./data/allDistComb1Day"+tit+".dat"))
    data_dist_a = pdist(varValues,lambda u,v: KL_H(u,v))

    varValues2 = (np.loadtxt("./data/ldaTopics"+tit+".dat"))
    data_dist_b = pdist(varValues2,lambda u,v: KL_H(u,v))

    return np.mean(data_dist_a),np.mean(data_dist_b)

def find_number_topics(range_lookup,n_iter=1000):
    """
    iterates through range_lookup and plots the distance between topics, to choose the best number
    
    """
    allMessages =  pickle.load(open('./data/corpus.dat',"rb+"))
    vocab = pickle.load(open('./data/vocab.txt',"rb+"))
        
    distances = []
    for i in range_lookup:
        loglikelihood = lda_run(allMessages,vocab,topicNum = i,n_iter=n_iter)  
        freq_distance, topic_distance = find_distances(tit=str(i),retTopics=True)
        distances.append([loglikelihood,freq_distance,topic_distance])
    
    fig = plt.figure(figsize = (15,5))
    loglikelihood,freq_distance,topic_distance = zip(*distances)
    ax = fig.add_subplot(1,3,1)
    plotNumTopics(range_lookup, loglikelihood,ax,loglikelihood=True)
    ax = fig.add_subplot(1,3,2)
    plotNumTopics(range_lookup, freq_distance,ax,loglikelihood=True)
    ax =fig.add_subplot(1,3,3)
    plotNumTopics(range_lookup, topic_distance,ax,loglikelihood=True)
    plt.show()
    


def correlationMerge(tit="",threshold=0.7):
    """
    Cluster topics that are close (in time and in frequency of words)
    """
    from scipy.stats import pearsonr,spearmanr,kendalltau,entropy
    import pylab as plt
    from scipy.spatial.distance import pdist, squareform
    from scipy.cluster.hierarchy import linkage, dendrogram,leaders,fcluster

    vocab = pickle.load(open('./data/vocab.txt',"rb+"))

    def KL_E(u,v):
        return entropy(u,v)*entropy(v,u)/entropy(u)/entropy(v)

    varValues = np.transpose(np.loadtxt("./data/allDistComb1Day"+str(tit)+".dat"))
    data_dist_a = pdist(varValues,lambda u,v: KL_E(u,v))

    varValues2 = (np.loadtxt("./data/ldaTopics"+str(tit)+".dat"))
    data_dist_b = pdist(varValues2,lambda u,v: KL_E(u,v))
    data_dist = data_dist_a*1 * data_dist_b*1

    #print(data_dist)
    fig = plt.figure(figsize=(8,8))

    # plot first dendrogram:
    ax1 = fig.add_axes([0.05,0.1,0.2,0.6])
    Y = linkage(data_dist, method='weighted') # method?

    t = max(Y[:, 2]) * threshold
    Z1 = dendrogram(Y, orientation='right',
                leaf_font_size=18,color_threshold=t) # adding/removing the axes
                #labels=["Profit","Decay","Profit \n(Ratio)","IMDB rating","Metascore","RottenT \nAudience","RottenT \nCritics","Profit \n(Deviation)"],
    ax1.set_xticks([]) # turn off xticks

    # plot second dendrogram:
    ax2 = fig.add_axes([0.32,0.71,0.58,0.2])
    Z2 = dendrogram(Y,color_threshold=t)
    ax2.set_xticks([])
    ax2.set_yticks([])

    clusters = fcluster(Y,t=t,criterion='distance')
    #print( clusters)
    lisTop = np.asarray(range(len(clusters)))

    #print(np.unique(clusters))
    prov = 0
    for g in np.unique(clusters):
        group = lisTop[clusters==g]
        for i2 in group:
            topic_words = np.array(vocab)[np.argsort(varValues2[i2,:])][:]#-[:n_top_words:-1]
            freq_words = np.array(varValues2[i2,:])[np.argsort(varValues2[i2,:])][:]#-n_top_words:-1]
            prov += np.sum(freq_words[::-1][:10])


    # get the distance matrix:
    D = squareform(data_dist)

    # reorder rows/cols of D to match dendrograms
    idx1 = Z1['leaves']
    idx2 = Z2['leaves']
    D = D[idx1,:]
    D = D[:,idx2]
    # add matrix
    axmatrix = fig.add_axes([0.32,0.1,0.58,0.6])
    im = axmatrix.matshow(D, aspect='auto', origin='lower', cmap=plt.cm.YlGnBu)
    axmatrix.set_xticks([])
    axmatrix.set_yticks([])

    # Plot colorbar.
    axcolor = fig.add_axes([0.91,0.1,0.02,0.6])
    plt.colorbar(im, cax=axcolor)
    #plt.savefig("./data/"+'MatrixPrediction'+tit+'.pdf', bbox_inches='tight' ,dpi=100)
    #plt.savefig("./data/"+'MatrixPrediction'+tit+'.png', bbox_inches='tight' ,dpi=100)
    plt.show()
    return clusters,vocab,varValues2

def automatic_annotate(clusters,vocab,varValues2):
    """
    Finds the wods that characterize each cluster (prints them) and by topic (saves them to ./data/topics.csv)
    """
    sumValues = np.sum(varValues2,0)
    lisTop = np.asarray(range(len(clusters)))
    cols = ['g','r','c','b','m','y','k','g','b']
    print(clusters)
    
    for g in np.unique(clusters):
        group = lisTop[clusters==g]
        #print(group)
        prov = np.zeros(len(sumValues))
        for i2 in group:
            topic_words = np.array(vocab)[np.argsort(varValues2[i2,:])][:]#-[:n_top_words:-1]
            freq_words = np.array(varValues2[i2,:])[np.argsort(varValues2[i2,:])][:]#-n_top_words:-1]
            prov += varValues2[i2,:]

            sumValues1 = np.sum(varValues2,0)
  
            topic_words1 = np.array(vocab)[np.argsort(varValues2[i2,:]/sumValues1)][:]#-[:n_top_words:-1]
            sumValues2 = np.ones(len(np.sum(varValues2,0)))
            topic_words2 = np.array(vocab)[np.argsort(varValues2[i2,:])][:]#-[:n_top_words:-1]           
            x = []
            indX = 0
            while len(x) < 20:
                x += list(topic_words1[::-1][indX:indX+1])
                x += list(topic_words2[::-1][indX:indX+1])
                indX += 1
            

            print(i2,' '.join(x))
            #print('Topic {}: {}'.format(i2, ' '.join(topic_words[::-1][:50])))
            #print('Topic {}: {}'.format(i2, ' '.join([str(_) for _ in freq_words[::-1][:50]])))
        sumValues1 = np.sum(varValues2,0)
        topic_words1 = np.array(vocab)[np.argsort(prov/sumValues)][:]#-[:n_top_words:-1]
        sumValues2 = np.ones(len(np.sum(varValues2,0)))
        topic_words2 = np.array(vocab)[np.argsort(prov/sumValues)][:]#-[:n_top_words:-1]
        x = []
        indX = 0
        while len(x) < 20:
            x += list(topic_words1[::-1][indX:indX+1])
            if topic_words2[::-1][indX:indX+1] not in x:
                x += list(topic_words2[::-1][indX:indX+1])
            indX += 1
        
        print("All cluster: ",' '.join(x))
        print("-"*30)
   

    with open("./data/topics.csv","w+") as f:
        for i2 in range(len(clusters)):
        
            topic_words = np.array(vocab)[np.argsort(varValues2[i2,:])][:]#-[:n_top_words:-1]
            freq_words = np.array(varValues2[i2,:])[np.argsort(varValues2[i2,:])][:]#-n_top_words:-1]
         
            sumValues1 = np.sum(varValues2,0)
            topic_words1 = np.array(vocab)[np.argsort(varValues2[i2,:]/sumValues1)][:]#-[:n_top_words:-1]
            sumValues2 = np.ones(len(np.sum(varValues2,0)))
            topic_words2 = np.array(vocab)[np.argsort(varValues2[i2,:]/sumValues2)][:]#-[:n_top_words:-1]
            x = []
            indX = 0
            while len(x) < 30:
                x += list(topic_words1[::-1][indX:indX+1])
                x += list(topic_words2[::-1][indX:indX+1])
                
                indX += 1


            f.write("- {0}\t{1}\n".format(i2,' '.join(x)))

def weightWord(tit="",word='hoi'):
    """
    returns how much weight a word has in every article (based on its topic)
    """
    vocab = pickle.load(open('./data/vocab.txt',"rb"))

    #By day
    varValues = np.transpose(np.loadtxt("./data/allDistComb1Day"+str(tit)+".dat"))
    #By freq
    varValues2 = (np.loadtxt("./data/ldaTopics"+str(tit)+".dat"))

    weigthTopics = np.ones(int(tit))
    
    len_vocab = len(vocab)
    # Kind-of efficient way to count words (better to use a dictionary)
    file = re.split(' |\n',word)
    c = Counter(file)
    del c['']
    values = np.zeros(len_vocab)
    count = 0 
    for word in c:
        pos = bi_contains(vocab, word)
        if pos[0]:
            weigthTopics += np.log10(varValues2[:,pos[1]]/np.sum(varValues2[:,pos[1]])*c[word])
            

    weigthTopics = (weigthTopics - np.min(weigthTopics))
    weigthTopics /= np.sum(weigthTopics)
    
    return weigthTopics

    
def plot_imshows(all_topics,filenames,num_topics):
    """
    given all_topics = 2D array, one dimension = topics, the other = different queries we are comparing
    """
    all_topics[all_topics==0] = np.NaN

    plt.figure(figsize = (15,10))
    plt.subplot(2,1,1)
    plt.imshow(all_topics*10,interpolation="none",aspect="auto",cmap=plt.cm.YlGnBu)
    plt.yticks(range(len(filenames)),[_[_.find("a/")+2:_.find(".csv")] for _ in filenames])
    plt.xticks(range(num_topics),[str(_) for _ in range(num_topics)])
    plt.grid(False)
    plt.colorbar()
    plt.title("Not normalized")
    for topic_number in range(num_topics):
        all_topics[:,topic_number] = (all_topics[:,topic_number] - np.mean(all_topics[:,topic_number]))/np.std(all_topics[:,topic_number])

    plt.subplot(2,1,2)
    plt.title("Normalized")
    plt.imshow(all_topics,interpolation="none",aspect="auto", cmap=plt.cm.YlGnBu)
    plt.yticks(range(len(filenames)),[_[_.find("a/")+2:_.find(".csv")] for _ in filenames])
    plt.xticks(range(num_topics),[str(_) for _ in range(num_topics)])
    plt.grid(False)
    plt.colorbar()
    plt.show()