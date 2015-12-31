'''
to extract 100K samples of each class(to handle skewed classes)

@author: vaibhav
'''

import json
import csv

jsonInFile="../../../../data/yelp_academic_dataset_review.json"
outfile="../../../../data/csv/"
fieldnames = ['stars', 'text']

starCount = {1:0, 2:0, 3:0, 4:0, 5:0}
LIMIT = 100000

print('---------------------------');
with open(jsonInFile) as infile:
    count = 1;
    fileNo = 1;
    outFileName = outfile + str(fileNo) + ".csv"

    outF = open(outFileName, 'w', newline='\n', encoding='utf-8');
    outCsvWriter = csv.DictWriter(outF, fieldnames=fieldnames);
    outCsvWriter.writeheader();

    for idx, line in enumerate(infile):
        j = json.loads(line);
        j["text"] = "".join(j["text"].split("\n"))

        if(starCount[j['stars']] < LIMIT):
            starCount[j['stars']] += 1
            outCsvWriter.writerow({'stars': j['stars'], 'text':j['text']});
            count+=1;

            if count % 1000 == 0:
                print(count);
    print("-------------------------\nTotal Reviews: ", count, "\n Star Count: ", starCount, sep="");
