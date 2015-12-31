'''
Created on Nov 26, 2015

@author: vaibhav
'''

from sklearn.naive_bayes import MultinomialNB
from sklearn.cross_validation import StratifiedKFold
from utility import get_data
from utility import app_random_state_value
from sklearn.feature_extraction.text import TfidfTransformer
from utility import classes
from utility import formatAndPrintMetrics
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
import numpy as np


fullTrainFile = '../files/train_low_freq_removed_500k.txt'
maxIterations = 5 # number of CV results you want to see, value between 1 to 5
printPredictionToFile = False # deprecated.. should not use since we are doing CV, keep it false
algoVerbose = False
predFile = 'files/nb.mn.25.75.predictions'#sys.argv[2];
useTfIdf = True # this becomes feature 3! # True REDUCES MAE(good)
#Hyperparameters list

##


X, Y = get_data(fullTrainFile)
if(useTfIdf):
    transformer = TfidfTransformer()
    X = transformer.fit_transform(X,Y)
skf = StratifiedKFold(Y, n_folds=5, random_state=app_random_state_value)

scoreSumMatrix = np.zeros((4,len(classes)))
mseSum = 0
maeSum = 0
count=1
for train_index, test_index in skf:
    xTr, xTe = X[train_index], X[test_index]
    yTr, yTe = Y[train_index], Y[test_index]
    
    clf = MultinomialNB()
    yhTe = clf.fit(xTr, yTr).predict(xTe)
    
    #printMetrics(yTe,yhTe) #deprecated
    mseSum = mseSum + mean_squared_error(yTe,yhTe)
    maeSum = maeSum + mean_absolute_error(yTe,yhTe)
    score = precision_recall_fscore_support(yTe, yhTe, average=None, labels=classes)
    scoreSumMatrix = scoreSumMatrix + score
    if(printPredictionToFile): # deprecated.. should not use
        # write yhTe to predictions file
        with open(predFile+str(count), 'w') as outRf:
            for yhVal in yhTe:
                outRf.write(str(int(yhVal))+'\n')
    count+=1
    if(count>maxIterations):
        formatAndPrintMetrics(mseSum, maeSum, scoreSumMatrix, maxIterations)
        break