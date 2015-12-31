# This is the CLASSIFICATION phase of Naive Bayes which will generate a Prediction to stdout from a ModelFile and TestFile passed as cmd arguement.
# Need to specify names of MODELFILE and TESTFILE in command line arguments.
#
# command line args: <model_file> <test_file> <predictions_file>
# stdout:  NA

import sys;
import math;
import warnings;

modelFile = sys.argv[1];
testFile = sys.argv[2];
predFile = sys.argv[3];

modelF = open(modelFile, 'r');
testF = open(testFile, 'r');
sys.stdout = open(predFile, 'w');

vocabTotal = 0; # total vocabulary size of training data, will init this from model file
classes = {}; # dictionary of count of all classes for calculating P(Class), eg-{'NEGATIVE': 12500, 'POSITIVE': 12500}, init from model file
totalClassCount = 0; # this will be total number of documents
totalWordsPerClass = {}; # dictionary to store total words per class, eg-{'NEGATIVE': 999, 'POSITIVE': 999}, init from model file
classWordDict = {}; # count of words for a class, will init this from model file

# -- Initialising local data structures from MODEL FILE --
# Read the first line 
line = modelF.readline();
vocabTotal = int(line.rstrip('\n'));
line = modelF.readline();
countClasses = int(line.rstrip('\n'));
for i in range(0, countClasses): #iterate for all classes(line-by-line)
	line = modelF.readline();
	lineTokenArray = line.split();
	className = lineTokenArray[0];
	classCount = int(lineTokenArray[1]);
	classes[className]=classCount;
	totalClassCount = totalClassCount + classCount;
# iterating over rest of the lines to init the classWordDict object
line = modelF.readline();
while line:
	lineTokenArray = line.split();
	tokenClass = lineTokenArray[0];
	featureWord = lineTokenArray[1];
	featureCount = int(lineTokenArray[2]);
	#init totalWordsPerClass
	if tokenClass not in totalWordsPerClass:
		totalWordsPerClass[tokenClass]=featureCount;
	else:
		totalWordsPerClass[tokenClass] = totalWordsPerClass[tokenClass] + featureCount;
	#init classWordDict
	if tokenClass not in classWordDict:
			classWordDict[tokenClass]={};
	if featureWord not in classWordDict[tokenClass]: # no else needed here, since no duplicate words will be there for a class
			classWordDict[tokenClass][featureWord] = featureCount;
	line = modelF.readline();



# -- Generating Predictions --
#now iterate over all lines in test file and print the predicted output to STDOUT per line
eqProbCount = 0
for lineIdx, line in enumerate(testF, start=0):
	if lineIdx != 0:
		sys.stdout.write('\n');

	#iterate over all classes from classWordDict
	prob1=float('-inf');
	prob2=float('-inf');
	currentMaxProb=float('-inf');
	currentMaxProbClass='';
	for classLabel in classWordDict:
		logProbSum = math.log(classes[classLabel]/totalClassCount); # probability of a class, log[p(class)]
		lineTokenArray = line.split();
		## >> changed range init from 0 to 1, because test file is in SVMLight format
		for i in range(1, len(lineTokenArray)):	#iterate over all tokens(word:frequency), frequency*log[P(word|class)]
			featureI = lineTokenArray[i];
			splitFeatureI = featureI.split(':');
			featureWord = splitFeatureI[0];
			featureFrequency = int(splitFeatureI[1]);
			if featureWord in classWordDict[classLabel]: # ignore not present features
				logProbSum = logProbSum + featureFrequency * math.log((classWordDict[classLabel][featureWord] + 1)/(totalWordsPerClass[classLabel] + vocabTotal));
			else:
				logProbSum = logProbSum + featureFrequency * math.log((0 + 1)/(totalWordsPerClass[classLabel] + vocabTotal));
				#sys.stdout.write('\n##'+featureWord + '##');
		if prob1 == float('-inf'):
			prob1 = logProbSum;
		elif prob2 == float('-inf'):
			prob2 = logProbSum;
		if logProbSum>currentMaxProb:
			currentMaxProb = logProbSum;
			currentMaxProbClass = classLabel;
		elif logProbSum == currentMaxProb:
			eqProbCount += 1
	sys.stdout.write(currentMaxProbClass);# + ' ' + str(prob1) + ' ' + str(prob2));

#cleanup
modelF.close();
testF.close();

if eqProbCount>0:
	warnings.warn('equal probability found'+str(eqProbCount))