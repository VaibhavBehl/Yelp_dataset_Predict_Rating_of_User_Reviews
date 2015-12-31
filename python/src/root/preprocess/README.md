All pre-processing code is in this directory. The code is not very 'user friendly' and is not structured well. To generate the various features needed will have to execute in the following order: (may need to run some more scripts, see file documentation before running)
 
convert_json_to_csv.py -> create_csv_with_words_greater_than_freq.py -> create_csv_with_words_greater_than_freq_f4.py

Most of these files have hard-coded relative paths of inputs/outputs which might have slightly changed since the last run, so they will have to be adjusted accordingly.