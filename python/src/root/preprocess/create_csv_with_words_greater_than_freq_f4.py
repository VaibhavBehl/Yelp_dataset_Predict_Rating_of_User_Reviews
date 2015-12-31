'''
THIS IS FOR FEATURE 4, ADVANCED FEATURE !!(after removing low freq. words, we add advance features)-> bigrams of positive and negative words, 
and (somehow) count of positive/negative words for each tr. example
..
This file needs a RAW FEAT file and its corresponding DICT file.
It will then remove 'words' which occour less than a certain times in DICT file and create a new FEAT file

Created on Nov 26, 2015

@author: vaibhav
'''
import csv
import collections
from check_positive_or_negative import get_positive_words_from
from check_positive_or_negative import get_negative_words_from
from check_positive_or_negative import POSITIVE_WORDS_FILE
from check_positive_or_negative import NEGATIVE_WORDS_FILE
from nltk.stem.porter import PorterStemmer

REST_MODE = '_REST'
MIXED_MODE = '_MIXED'

MODE = REST_MODE

rawFile = 'files/featRawStem'+MODE+'.csv'#sys.argv[1]; #Raw stem feat file
rawDictFile = 'files/rawStemGlobalTokenDict'+MODE+'.csv'#sys.argv[2]; #Dictionary file
newFeatFile = 'files/new_feat'+MODE+'.csv'
newRawDictFile = 'files/new_rawStemGlobalTokenDict'+MODE+'.csv'
THRESHOLD = 2e-06

rawF = open(rawFile, 'r')
rawDictF = open(rawDictFile, 'r')
newFeatF = open(newFeatFile, 'w', newline='')
newRawDictF = open(newRawDictFile, 'w', newline='')

rawDict = collections.OrderedDict()
rawDictfReader = csv.reader(rawDictF)
totalWordCount = 0
for row in rawDictfReader:
    rawDict[row[0]] = int(row[1])
    totalWordCount += int(row[1])

positiveSet = get_positive_words_from(POSITIVE_WORDS_FILE)
posSetStem = set()
negativeSet = get_negative_words_from(NEGATIVE_WORDS_FILE)
negSetStem = set()
ps = PorterStemmer()
for p in positiveSet:
    posSetStem.add(ps.stem(p))
for n in negativeSet:
    negSetStem.add(ps.stem(n))

for pss in posSetStem:
    if pss in negSetStem:
        print('match found-'+pss)

rawDict['POSITIVE_COUNT'] = 0
staticPositiveFeatIndex = list(rawDict.keys()).index('POSITIVE_COUNT')
rawDict['NEGATIVE_COUNT'] = 0
staticNegativeFeatIndex = list(rawDict.keys()).index('NEGATIVE_COUNT')
rawDictList = list(rawDict.keys())
newBigramsIndexDict = {} # don't want to do a list(rawDict.keys()) each time rawDict is updated
rawDictNextIndex = staticNegativeFeatIndex+1

newFeatWriter = csv.writer(newFeatF)
# for each line of rawF write to newFeatFile those features that have frequency in rawDictList>(threshold) and also convert to SVM light Format
rawFReader = csv.reader(rawF)
for idx,row in enumerate(rawFReader):
    if idx > 10:
        break
    if idx%100==0:
        print(idx+1)
    rowTarget = row[0]
    rowValue = row[1]
    if rowValue:
        vTokens = rowValue.split('\t')
        vtokDict = {}
        positiveCount = 0
        negativeCount = 0
        for vTok in vTokens:
            if rawDict[vTok]/totalWordCount > THRESHOLD:
                found=False
                if vTok in posSetStem:
                    positiveCount+=1
                    found=True
                if vTok in negSetStem:
                    negativeCount+=1
                    found=True
                if found:
                    # add two bigrams for each word.. first add to main dict and/or find index from it
                    wordIndex = vTokens.index(vTok)
                    if wordIndex >0:
                        leftBigram = vTokens[wordIndex-1]+vTokens[wordIndex]
                        if leftBigram in rawDict:
                            rawDict[leftBigram] +=1
                        else:
                            rawDict[leftBigram] =1
                            newBigramsIndexDict[leftBigram] = rawDictNextIndex
                            rawDictNextIndex +=1
                        if leftBigram in rawDictList:
                            idx = rawDictList.index(leftBigram)
                        else:
                            idx = newBigramsIndexDict[leftBigram] # add this idx to the vtokDict(for this row)
                        if idx in vtokDict:
                            vtokDict[idx]+=1
                        else:
                            vtokDict[idx]=1
                    if wordIndex < len(vTokens)-1:
                        rightBigram = vTokens[wordIndex]+vTokens[wordIndex+1]
                        if rightBigram in rawDict:
                            rawDict[rightBigram] +=1
                        else:
                            rawDict[rightBigram] = 1
                            newBigramsIndexDict[rightBigram] = rawDictNextIndex
                            rawDictNextIndex +=1
                        if rightBigram in rawDictList:
                            idx = rawDictList.index(rightBigram)
                        else:
                            idx = newBigramsIndexDict[rightBigram] # add this idx to the vtokDict(for this row)
                        if idx in vtokDict:
                            vtokDict[idx]+=1
                        else:
                            vtokDict[idx]=1
                    
                fLabel = rawDictList.index(vTok) + 1 # this is 0 based index, but we need a plus 1
                if fLabel in vtokDict:
                    vtokDict[fLabel]+=1
                else:
                    vtokDict[fLabel]=1
        # sort vtokDict by keys(fLabel)
        vtokDict[staticPositiveFeatIndex] = positiveCount/len(vTokens)
        vtokDict[staticNegativeFeatIndex] = negativeCount/len(vTokens)
        
        value = ['']
        odFeatValueDict = collections.OrderedDict(sorted(vtokDict.items()))
        for kk, vv in odFeatValueDict.items():
            value.append(' %s:%s' % (str(kk), str(vv)))
        newFeatWriter.writerow([rowTarget,''.join(value)])
        
# need to wrtie out the new raw dict, which will have indexes for bigrams
newRawDictWriter = csv.writer(newRawDictF)
for key, value in rawDict.items():
    newRawDictWriter.writerow([key,value])