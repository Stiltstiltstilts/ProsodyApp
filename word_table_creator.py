################################################
"""
Code written by Courtney Hilton, December 2019
courtney.bryce.hilton@gmail.com

tested with python 3.6.7

This script takes as INPUT:
    1. '/words.txt' : list of words you want to use, each word on seperate line
    2. '/cmudict.txt' : database including lexical stress info (http://www.speech.cs.cmu.edu/cgi-bin/cmudict)

and OUTPUTS:
    1. /Output/word_table.txt' : table of words and their stress info in tab seperated columns format
        e.g.  - banana     010
    2. python list (uniques) that is used in tone_synthesis.py script to produce corresponding sound files
"""
################################################

################################################
################# Imports ######################
################################################

import re
import os

################################################
################## Files #######################
################################################

# path for current directory
_thisDir = os.path.abspath(os.path.dirname(__file__))
os.chdir(_thisDir)

# read file of all words to be used and return list
with open('/Users/courtneyhilton/Research/Projects/Prosody_app/words.txt', 'r') as f: 
    words = f.read().splitlines()


# reads cmu pronunciation database and returns list
with open('/Users/courtneyhilton/Research/Projects/Prosody_app/cmudict.txt', 'r') as f: 
    cmu = f.read().splitlines()

################################################
################ Main script ###################
################################################

# inits
stress_dict = {}
exceptions = []

##### 1. Extract stress info for chosen words in file: words.txt #####
for wordi in words: # iterate chosen words
    for cmu_line in cmu: # iterate entries of cmudict
        if re.match(r'^' + str.upper(wordi) + r'\s', cmu_line): # IF chosen word
            print(cmu_line) # print full cmudict string
            cmu_line = re.sub(r"\D", "", cmu_line) # strip letter info, leaving the stress numbers
            stress = [] # init
            for stressi in range(len(cmu_line)): #iterate through syllable stresses and output integer list
                stress += [int(cmu_line[stressi])]  
            stress_dict[wordi] = (stress, cmu_line) # output tuple: 0. list format, 1. number string
            found = True # confirm whether there was match in database
    if not found: # IF word is not in cmudict
        print(wordi) # if no match print word
        exceptions += [wordi]
    found = False # reset 

##### 2. determine all unique stress values #####
uniques = [] # create empty list
for val in stress_dict.values(): 
  if val in uniques: 
    continue 
  else:
    uniques.append(val)

##### 3. Write to new txt file all chosen words + stress info #####

# Create filename for data file (absolute path + name)
filename = _thisDir + os.sep + 'Output' + os.sep + 'word_table.txt'

with open(filename, 'w') as f:    
    for i in words:
        if i in exceptions:
            f.writelines(i + '\t' + 'unknown' + '\n')
        else:
            f.writelines(i + '\t' + stress_dict[i][1] + '\n')