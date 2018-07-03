'''
PURPOSE: This file is a one time run file to load xlsx file
        to make a json file

AUTHOR: Ink_feather
'''

import numpy as np
import pandas as pd
import json
from autocorrect import spell
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn


tokenizer = RegexpTokenizer(r'\w+') #to remove punctuations
stopwords = stopwords.words("english") # to remove stopwords


'''
this part needs to be customized according to xlsx file
'''
#loading data_frame --- this part needs to be changed heavily depending on your xlsx file format
df0 = pd.read_excel('DATA/Travel_Chatbot.xlsx', sheet_name='Sheet2')
df0 = df0.drop(columns=["Input"])
df0 = df0.dropna()
df0["Serial No."]=df0["Serial No."].astype(int)
df0 = df0.set_index("Serial No.")
df0 = df0.drop([25])
df0.index = np.arange(1,len(df0)+1)
df0.index.name = "Serial No."
# --------------------------------------------------------------------



data = {}   #data to be put into json

'''
Please make changes in the list below according too your dataset
'''
weird_words = ['whether','would','everybody','towards']
# no one wants these words in the tags + synset of these words do not exist

for index,row in df0.iterrows():

    # for the question ----------------------
    tokens = tokenizer.tokenize(row["Question"].lower()) #making the entire string lower

    filtered_tokens = [w for w in tokens if not w in stopwords]  # filtering stopwords

    #print("Checking for spelling errors ...\n")
    print("Q{0})-----------".format(index))
    print(row["Question"])
    print("original: {0}".format(filtered_tokens))

    filtered_tokens = [spell(w) for w in filtered_tokens]
    print("Corrected Spells : {0}".format(filtered_tokens))

    list1 = []
    list2 = []
    for w in filtered_tokens:
        if wn.synsets(w):
            list1.append(w)
            #list1.append([a.name() for a in wn.synsets(w)])
        else :
            print("Tag: {0}".format(w))
            #whether would towards everybody -- need to be removed
            # some weird words are not filtered through -> need to be hardcoded and removed
            if (w not in list2) and (w not in weird_words):
                list2.append(w)



    print("Synset : {0}".format(list1))
    print("Tags : {0}\n".format(list2))


    #print(list1) # testing
    # pudding values into data

    data[index] = {
    "Question ": row["Question"],
    "Question_list" : list1,
    "Tags" : list2,
    "Answer"   : row["Answer"]
    }


#print(json.dumps(data, indent=4))

with open('DATA/data_reimbursement_reset.json', 'w') as outfile:
    json.dump(data, outfile,indent = 4)
