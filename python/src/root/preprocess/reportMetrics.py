# Prints various scores/metrics(precision, recall, F1) to the STDOUT. Needs two files containing SAME number of lines and having same classes.
# Also pass in the classes on which to report the metric.
#
# command line args: <original_file> <predicted_file> <Class1> <Class2>
# stdout: <scores>

import math

originalFile = 'files/te_25'#sys.argv[1];
predictedFile = 'files/nb.mn.25.75.predictions5'#sys.argv[2];

originalF = open(originalFile, 'r');
predictedF = open(predictedFile, 'r');

classes = ['1','2','3','4','5']
belongInClass = [0,0,0,0,0]
classifiedAsClass = [0,0,0,0,0]
correctlyClassifiedAsClass = [0,0,0,0,0]

predictedFArray = predictedF.readlines();
mseSum = 0
abSum = 0
mseCount = 0
for lineIdx, originalL in enumerate(originalF, start=0):
	origLineT = originalL.split()
	originalLine = origLineT[0].rstrip('\n');
	pfaT = predictedFArray[lineIdx].split();
	predictedLine = pfaT[0].rstrip('\n');
	mseSum = mseSum + math.pow(int(originalLine)-int(predictedLine),2)
	abSum = abSum + abs(int(originalLine)-int(predictedLine))
	mseCount += 1
	for i,cc in enumerate(classes):
		if originalLine == cc:
			belongInClass[i] += 1
		if predictedLine == cc:
			classifiedAsClass[i] += 1
		if originalLine == predictedLine:
			if originalLine == cc:
				correctlyClassifiedAsClass[i] += 1

print('MSE=' + str(mseSum/mseCount))
print('MAE=' + str(abSum/mseCount))
for i,cc in enumerate(classes):
	pClass = round(100*correctlyClassifiedAsClass[i]/classifiedAsClass[i],4);
	rClass = round(100*correctlyClassifiedAsClass[i]/belongInClass[i],4);
	fClass = round(2*pClass*rClass/(pClass + rClass),4);
	print('class ' + str(cc) + ' P=' + str(pClass) + ' R=' + str(rClass) + ' F=' + str(fClass))
#cleanup
originalF.close();
predictedF.close();
