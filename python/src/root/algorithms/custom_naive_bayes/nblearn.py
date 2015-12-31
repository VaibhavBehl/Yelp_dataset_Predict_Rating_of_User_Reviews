# This is the LEARNING phase of Naive Bayes which will generate a Model file from training data passed to it.
# Need to specify names of Training data and Model file in command line arguments.
#
# command line args: <training_data> <model_file>
# stdout: #none

import sys;

trainFile = sys.argv[1];
modelFile = sys.argv[2];

trainF = open(trainFile, 'r');
modelF = open(modelFile, 'w');

vocab = set(); # set to keep track of unique vocab words
classes = {}; # count of all classes for calculating P(Class), stored like this- {'NEGATIVE': 15, 'POSITIVE': 10}
classWordDict = {}; # will store count of class-word pair like this- {'NEGATIVE': {'none': 18, 'all': 101}, 'POSITIVE': {'me': 18, 'the': 10}}

for line in trainF:
	lineTokenArray = line.split();
	
	for i in range(0, len(lineTokenArray)):	#iterate over all tokens in line
		if i == 0: # first token is always a Class
			tokenClass = lineTokenArray[i];
			if tokenClass not in classes: # count of all Classes
				classes[tokenClass]=1;
			else:
				classes[tokenClass]=classes[tokenClass]+1;
				
			#init the token in classWordDict if not found
			if tokenClass not in classWordDict:
				classWordDict[tokenClass]={}; # this dictionary will store word count pairs
		else:
			wordCountDict = classWordDict[tokenClass];
			featureI = lineTokenArray[i];
			splitFeatureI = featureI.split(':');
			featureName = splitFeatureI[0];
			featureValue = int(splitFeatureI[1]);
			vocab.add(featureName); # add to unique feature(word) set
			
			if featureName not in wordCountDict:
				wordCountDict[featureName] = featureValue;
			else:
				wordCountDict[featureName] = wordCountDict[featureName] + featureValue;

# -- Writing Model File
#First line of model file is 'Vocabulary Size'
modelF.write(str(len(vocab))+'\n');
#then count of classes present
modelF.write(str(len(classes)));
#now we print all classnames with count (one each line)
for ck in classes:
	modelF.write('\n' + ck + ' ' + str(classes[ck]));
#After that all lines will be space delimited values having Class,Feature_Name,Feature_Count like:NEGATIVE none 18
for classKey in classWordDict:
	for wordKey in classWordDict[classKey]:
		modelF.write('\n');
		modelF.write(classKey);
		modelF.write(' ');
		modelF.write(wordKey);
		modelF.write(' ');
		modelF.write(str(classWordDict[classKey][wordKey]));

#cleanup
trainF.close();
modelF.close();
