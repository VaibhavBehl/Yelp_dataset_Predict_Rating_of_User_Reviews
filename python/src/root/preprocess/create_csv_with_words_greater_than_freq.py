'''
THIS IS FOR FEATURE 2 !!(removing low freq. words)
..
This file needs a RAW FEAT file and its corresponding DICT file.
It will then remove 'words' which occour less than a certain times in DICT file and create a new FEAT file

Created on Nov 26, 2015

@author: vaibhav
'''
import csv
import collections 

REST_MODE = '_REST'
MIXED_MODE = '_MIXED'

MODE = MIXED_MODE

rawFile = 'files/featRawStem'+MODE+'.csv'#sys.argv[1]; #Raw stem feat file
rawDictFile = 'files/rawStemGlobalTokenDict'+MODE+'.csv'#sys.argv[2]; #Dictionary file
newFeatFile = 'files/new_feat'+MODE+'.csv'
THRESHOLD = 2e-06

rawF = open(rawFile, 'r')
rawDictF = open(rawDictFile, 'r')
newFeatF = open(newFeatFile, 'w', newline='')

rawDict = collections.OrderedDict()
rawDictfReader = csv.reader(rawDictF)
totalWordCount = 0
for row in rawDictfReader:
    rawDict[row[0]] = int(row[1])
    totalWordCount += int(row[1])

rawDictList = list(rawDict.keys())
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
        for vTok in vTokens:
            if rawDict[vTok]/totalWordCount > THRESHOLD:
                fLabel = rawDictList.index(vTok) + 1 # this is 0 based index, but we need a plus 1
                if fLabel in vtokDict:
                    vtokDict[fLabel]+=1
                else:
                    vtokDict[fLabel]=1
        # sort vtokDict by keys(fLabel)
        
        value = ['']
        odFeatValueDict = collections.OrderedDict(sorted(vtokDict.items()))
        for kk, vv in odFeatValueDict.items():
            value.append(' %s:%s' % (str(kk), str(vv)))
        newFeatWriter.writerow([rowTarget,''.join(value)])