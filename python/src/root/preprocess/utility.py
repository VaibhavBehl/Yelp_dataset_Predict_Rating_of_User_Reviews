'''
Created on Nov 27, 2015

@author: vaibhav
'''
import sys
import math
from sklearn.externals.joblib import Memory
from sklearn.datasets import load_svmlight_file
import numpy as np

# don't change this value in between testing diff algos. This value determines how the StratifiedKFold cuts All Data into Tr and Te
app_random_state_value = 1
classes = [1,2,3,4,5]

def formatAndPrintMetrics(mseSum, maeSum, scoreSumMatrix, maxIterations):
    scoreSumMatrix = scoreSumMatrix/maxIterations
    scoreSumMatrix = scoreSumMatrix*100
    scoreSumMatrix = np.around(scoreSumMatrix.astype(np.double),4)
    print('average MSE=' + str(round(mseSum/maxIterations,4)))
    print('average MAE=' + str(round(maeSum/maxIterations,4)))
    print('average P=' + str(scoreSumMatrix[0]))
    print('average R=' + str(scoreSumMatrix[1]))
    print('average F=' + str(scoreSumMatrix[2]))

#this is only to generate for a single pair of (orig,pred), use formatAndPrintMetrics for others
def printMetrics(origY, predY):
    
    if(len(origY) != len(predY)):
        sys.exit('Custom error msg: length of orig and pred Y not equal')
    
    belongInClass = [0,0,0,0,0]
    classifiedAsClass = [0,0,0,0,0]
    correctlyClassifiedAsClass = [0,0,0,0,0]
    
    mseSum = 0
    abSum = 0
    mseCount = 0
    for oy, py in zip(origY, predY):
        mseSum = mseSum + math.pow(oy-py,2)
        abSum = abSum + abs(oy-py)
        mseCount += 1
        for i,cc in enumerate(classes):
            if oy == cc:
                belongInClass[i] += 1
            if py == cc:
                classifiedAsClass[i] += 1
            if oy == py:
                if oy == cc:
                    correctlyClassifiedAsClass[i] += 1
    
    print('MSE=' + str(mseSum/mseCount))
    print('MAE=' + str(abSum/mseCount))
    for i,cc in enumerate(classes):
        pClass = round(100*correctlyClassifiedAsClass[i]/classifiedAsClass[i],4);
        rClass = round(100*correctlyClassifiedAsClass[i]/belongInClass[i],4);
        fClass = round(2*pClass*rClass/(pClass + rClass),4);
        print('class ' + str(cc) + ' P=' + str(pClass) + ' R=' + str(rClass) + ' F=' + str(fClass))

mem = Memory("./mycache_can_delete")
@mem.cache
def get_data(dataFile):
    data = load_svmlight_file(dataFile)
    return data[0], data[1]