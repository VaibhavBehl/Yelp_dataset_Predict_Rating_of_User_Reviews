'''
Created on Nov 18, 2015

@author: vaibhav
'''
import json
import csv
#from pprint import pprint

jsonInFile="../../../../data/yelp_academic_dataset_review.json"
outfile="../../../../data/csv/"
fieldnames = ['id', 'stars', 'text']

print('---------------------------');
with open(jsonInFile) as infile:
    count = 1;
    fileNo = 1;
    outFileName = outfile + str(fileNo) + ".csv"

    outF = open(outFileName, 'w', newline='\n', encoding='utf-8');
    outCsvWriter = csv.DictWriter(outF, fieldnames=fieldnames);
    # outCsvWriter.writeheader();

    for idx,line in enumerate(infile):
        #print(idx+1);
        j = json.loads(line);
        j["text"] = "".join(j["text"].split("\n"))
        outCsvWriter.writerow({'id': idx+1, 'stars': j['stars'], 'text':j['text']});
        print(count);
        count+=1;

        if count % 1000 == 0:
            outF.close()
            fileNo += 1
            outFileName = outfile + str(fileNo) + ".csv"
            outF = open(outFileName, 'w', newline='\n', encoding='utf-8');
            outCsvWriter = csv.DictWriter(outF, fieldnames=fieldnames);

    outF.close()
    print("-------------------------\nTotal Reviews: ", count, "\nTotal Files:", fileNo, sep="");
