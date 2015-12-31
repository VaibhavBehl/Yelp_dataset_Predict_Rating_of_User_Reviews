'''
Created on Nov 18, 2015

@author: vaibhav
'''
import json
import csv
import collections
import time
from preprocessText import preprocess
from nltk.stem.porter import PorterStemmer

jsonInFile="../../../../data/yelp_academic_dataset_review.json"
businessJsonInFile="../../../../data/yelp_academic_dataset_business.json"

restBizSet = set()
with open(businessJsonInFile) as bizInfile:
    for idx,line in enumerate(bizInfile):
        j = json.loads(line);
        bizId = j['business_id']
        bizCats = j['categories']
        if 'Restaurants' in bizCats:
            restBizSet.add(bizId)

#outfile="../../../../data/review_json.csv"
#outF = open(outfile, 'w', newline='\n', encoding='utf-8');
#outCsvWriter = csv.writer(outF, delimiter=',');
#fieldnames = ['id', 'stars', 'text']
#outCsvWriter = csv.DictWriter(outF, fieldnames=fieldnames);
#outCsvWriter.writeheader();

REST_MODE = '_REST'
MIXED_MODE = '_MIXED'

MODE = MIXED_MODE
featWriter = csv.writer(open('feat'+ MODE+'.csv', 'w', newline=''))
featRawWriter = csv.writer(open('featRaw'+ MODE+'.csv', 'w', newline=''))
featRawStemWriter = csv.writer(open('featRawStem'+ MODE+'.csv', 'w', newline=''))

start_time = time.time()
textLenDict={}
classCountDict = {1:0,2:0,3:0,4:0,5:0}
odGlobalTokenDict=collections.OrderedDict()
rawGlobalTokenDict = {}
rawStemGlobalTokenDict = {}
pStemmer = PorterStemmer()
print('---------------------------');
if MODE == REST_MODE:
    RECORD_LIMIT = 25
elif MODE == MIXED_MODE:
    RECORD_LIMIT = 50
 
with open(jsonInFile) as infile:
    count = 0;
    for idx,line in enumerate(infile):
        #print(idx+1);
        j = json.loads(line);
#       outCsvWriter.writerow({'id': idx+1, 'stars': j['stars'], 'text':j['text']});
        sClass = j['stars']
        jText = j['text']
        jBizRevId = j['business_id']
        jTextLen = len(jText)
        # RAW
        proRaw = preprocess(jText,pStemmer,True,False,False)
        proRaw = [i for i in proRaw if len(i) > 2]
        # upper bound on each classes exmpales
        if classCountDict[sClass] <round(RECORD_LIMIT/5) and len(proRaw)>=15 and len(proRaw)<600:
            if MODE == MIXED_MODE or (MODE == REST_MODE and jBizRevId in restBizSet):
                classCountDict[sClass]+=1
    
                for tok in proRaw:
                    if tok in rawGlobalTokenDict:
                        rawGlobalTokenDict[tok]+=1
                    else:
                        rawGlobalTokenDict[tok]=1
                featRawWriter.writerow([sClass,'\t'.join(proRaw)])
                
                processed = preprocess(jText,pStemmer,True,False,True)
                processed = [i for i in processed if len(i) > 2]
                
                # RAW STEM(porter)
                proRawStem = processed
                for tok in proRawStem:
                    if tok in rawStemGlobalTokenDict:
                        rawStemGlobalTokenDict[tok]+=1
                    else:
                        rawStemGlobalTokenDict[tok]=1
                featRawStemWriter.writerow([sClass,'\t'.join(proRawStem)])
                #print('^v^v^v^v^v^')
                #print('-jText-'+jText)
                #print('-processed-'+str(processed))
                # store this 'processed' tokens(unigrams) in the textLenDict and same time get index and write in CSV file
                localTokenDict = {} # per example
                #storing in odGlobalTokenDict and also getting current index to use as replacement
                for tok in processed:
                    if tok in odGlobalTokenDict:
                        odGlobalTokenDict[tok]+=1
                    else:
                        odGlobalTokenDict[tok]=1
                    if tok in localTokenDict:
                        localTokenDict[tok]+=1
                    else:
                        localTokenDict[tok]=1
                odGlobalTokenDictList = list(odGlobalTokenDict.keys())
    
                #print('-localTokenDict-'+str(localTokenDict))
                #print('len(localTokenDict)='+str(len(localTokenDict)))
                #print('-odGlobalTokenDict-'+str(odGlobalTokenDict))
                featValueDict = {} # dict to store the feat:weight as key:value so later sort by KEY!!
                for lTok in localTokenDict.keys():
                    featValueDict[odGlobalTokenDictList.index(lTok)+1] = localTokenDict[lTok]
                
                value = ['']
                odFeatValueDict = collections.OrderedDict(sorted(featValueDict.items()))
                for kk, vv in odFeatValueDict.items():
                    value.append(' %s:%s' % (str(kk), str(vv)))
                featWriter.writerow([sClass, ''.join(value)])
                
                #text length dict, just for checking purpose
                if jTextLen in textLenDict:
                    textLenDict[jTextLen] +=1
                else:
                    textLenDict[jTextLen]= 1
                    
                if count % 100 == 0:
                    print(count);
                count+=1;
                if count>=RECORD_LIMIT:
                    break;
            
    
    print("--- %s seconds ---" % (time.time() - start_time))
    print('----------textLenDict-----------------');
    ##print(len(textLenDict))
    #od = collections.OrderedDict(sorted(textLenDict.items()))
    #print(od)
    sorted_textLenDict = collections.OrderedDict(sorted(textLenDict.items(), key=lambda x:x[1], reverse=True))
    #print(sorted_textLenDict)
    textLenDictWriter = csv.writer(open('textLenDict'+MODE+'.csv', 'w', newline=''))
    for key, value in sorted_textLenDict.items():
        textLenDictWriter.writerow([key,value])
    
    print('------------token dict---------------');
    sorted_tokenDict = collections.OrderedDict(sorted(odGlobalTokenDict.items(), key=lambda x:x[1], reverse=True))
    #print(sorted_tokenDict)
    tokenDictWriter = csv.writer(open('odGlobalTokenDict'+MODE+'.csv', 'w', newline=''))
    for key, value in sorted_tokenDict.items():
        tokenDictWriter.writerow([key,value])
        
    print('------------raw token dict---------------');
    sorted_tokenDict = collections.OrderedDict(sorted(rawGlobalTokenDict.items(), key=lambda x:x[1], reverse=True))
    tokenDictWriter = csv.writer(open('rawGlobalTokenDict'+MODE+'.csv', 'w', newline=''))
    for key, value in sorted_tokenDict.items():
        tokenDictWriter.writerow([key,value])
    
    print('------------raw stem token dict---------------');
    sorted_tokenDict = collections.OrderedDict(sorted(rawStemGlobalTokenDict.items(), key=lambda x:x[1], reverse=True))
    tokenDictWriter = csv.writer(open('rawStemGlobalTokenDict'+MODE+'.csv', 'w', newline=''))
    for key, value in sorted_tokenDict.items():
        tokenDictWriter.writerow([key,value])
    
    print('*******FINISHED :)*******')