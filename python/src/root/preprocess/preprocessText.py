__author__ = 'FarhanKhwaja'

import re
import nltk

def preprocess(text, pStemmer, textCleanUp=True, stopwordsCheck=False, stemWords=False):
    #nltk.download()
    #stopwords = ["(", ")", "#", '!', ':', '.','-', ",", '"', "'", "+", ';', '/', '\\','?']
    unigram = []
    if text != '':

        if textCleanUp:

            text = text.lower()
            text = re.sub("[^a-z]+", " ", text)
            
            # remove weird non english characters
            #text = re.sub("[^\\x00-\\x7f]", "", text)

            # remove urls
            #text = re.sub("(\w+:\/\/\S+)", " ", text)

            #for replacementWord in stopwords:
            #   text = text.replace(replacementWord, " ")


        #pStemmer = PorterStemmer()
        tokens = text.split()
        
        # nltk.corpus.stopwords.words('english') -- not good, since it will remove words like very!!
        if stemWords and stopwordsCheck:
            unigram = [pStemmer.stem(w) for w in tokens if w not in nltk.corpus.stopwords.words('english') and w.isalpha()]
        elif stemWords:
            unigram = [pStemmer.stem(w) for w in tokens]
        elif stopwordsCheck:
            unigram = [w for w in tokens if w not in nltk.corpus.stopwords.words('english') and w.isalpha()]
        else:
            #lowercase and tokenize
            unigram = [w for w in tokens]

    return unigram