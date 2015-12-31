'''
this will read from feat and dict, and will generate new dict and new feat.. after removing low freq words
..
This file needs a RAW FEAT file and its corresponding DICT file.
It will then remove 'words' which occour less than a certain times in DICT file and create a new FEAT file

Created on Nov 26, 2015

@author: vaibhav
'''
import csv
import collections 
import sys

REST_MODE = '_REST'
MIXED_MODE = '_MIXED'

MODE = REST_MODE

THRESHOLD = 2e-06

rawF = open('files/new_feat'+MODE+'.csv', 'r')
rawDictF = open('files/new_rawStemGlobalTokenDict'+MODE+'.csv', 'r')
newFeatF = open('files/new_new_feat'+MODE+'.csv', 'w', newline='')
newDictF = open('files/new_new_featDict'+MODE+'.csv', 'w', newline='')

rawDict = collections.OrderedDict()
rawDictfReader = csv.reader(rawDictF)
totalWordCount = 0
for row in rawDictfReader:
    rawDict[row[0]] = int(row[1])
    totalWordCount += int(row[1])

#new ordered dict with freq<10 words removed
tempOrderedDict = collections.OrderedDict()
for key,value in rawDict.items():
    if key=='POSITIVE_COUNT' or key=='NEGATIVE_COUNT' or (value>=10 and value<=100000):
        tempOrderedDict[key] = value
newOrderedDict = collections.OrderedDict(sorted(tempOrderedDict.items(), key=lambda x:x[1], reverse=True))

##
rawDictList = list(rawDict.keys()) # indexes for old(existing)
newOrderedDictList = list(newOrderedDict.keys()) # indexes for new 

newFeatWriter = csv.writer(newFeatF)
# for each line of rawF write to newFeatFile those features that have frequency in rawDictList>(threshold) and also convert to SVM light Format
rawFReader = csv.reader(rawF)
for idx,row in enumerate(rawFReader):
    if idx%100==0:
        print(idx+1)
    rowTarget = row[0]
    rowValue = row[1]
    if rowValue:
        vTokens = rowValue.split()
        vtokDict = {}
        for vTok in vTokens: # iterating over orig token file (int-index in orig dict:int-feature val)
            vTokSplit = vTok.split(':')
            fi = vTokSplit[0] # find index of this in orig, than find 'text' from it, find that 'text' index in new dict, replace it
            fv = vTokSplit[1]
            
            #check if fi's 'text' is in new dict
            fiTextRawDict = rawDictList[int(fi)-1]
            if fiTextRawDict == 'POSITIVE_COUNT':
                fv = float(fv)*50
            elif fiTextRawDict == 'NEGATIVE_COUNT':
                fv = float(fv)*100
            if fiTextRawDict in newOrderedDictList:
                newFI = newOrderedDictList.index(fiTextRawDict) + 1
                if newFI in vtokDict:
                    sys.exit('duplicate found, should not happen')
                else:
                    vtokDict[newFI]=fv
        # sort vtokDict by keys(fLabel)
        
        value = ['']
        odFeatValueDict = collections.OrderedDict(sorted(vtokDict.items()))
        for kk, vv in odFeatValueDict.items():
            value.append(' %s:%s' % (str(kk), str(vv)))
        newFeatWriter.writerow([rowTarget,''.join(value)])

# need to wrtie out the new raw dict, which will have indexes for bigrams
newRawDictWriter = csv.writer(newDictF)
for key, value in newOrderedDict.items():
    newRawDictWriter.writerow([key,value])