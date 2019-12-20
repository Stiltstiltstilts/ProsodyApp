
import re
output_list = []


# read words file and return list
with open('/Users/courtneyhilton/Research/Projects/Prosody_app/words.txt', 'r') as f: 
    words = f.read().splitlines()


# read cmu file and return list
with open('/Users/courtneyhilton/Research/Projects/Prosody_app/cmudict.txt', 'r') as f: 
    cmu = f.read().splitlines()


stress_dict = {}
exceptions = []

# loop to find each line of cmu corresponding to words
for wordi in words: # for each selected word
    for cmu_line in cmu: # for each cmu entry
        if re.match(r'^' + str.upper(wordi) + r'\s', cmu_line):
            print(cmu_line) # print full cmudict string
            cmu_line = re.sub(r"\D", "", cmu_line) # strip letter info, leaving the stress numbers
            stress = [] # init
            for stressi in range(len(cmu_line)):
                stress += [int(cmu_line[stressi])]  
            print(stress) #print stress pattern
            stress_dict[wordi] = (stress, cmu_line)
            found = True # confirm whether there was match in database
    if not found:
        print(wordi) # if no match print word
        exceptions += [wordi]
    found = False # reset 


# determine all unique stress values
uniques = [] # create empty list
for val in stress_dict.values(): 
  if val in uniques: 
    continue 
  else:
    uniques.append(val)

with open('/Users/courtneyhilton/Research/Projects/Prosody_app/testy.txt', 'w') as f:    
    for i in words:
        if i in exceptions:
            f.writelines(i + '\t' + 'unknown' + '\n')
        else:
            f.writelines(i + '\t' + stress_dict[i][1] + '\n')