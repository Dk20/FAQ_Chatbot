from similarity_calc import calc2
import json
from autocorrect import spell   #this one takes a bit of time

from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn

tokenizer = RegexpTokenizer(r'\w+') #to remove punctuations
stopwords = stopwords.words("english") # to remove stopwords

with open('data_VIT_FAQ_reset_new.json') as json_:
    data = json.load(json_)
json_.close()

weird_words = data["weird_words"] # these words are not defined in synset
index = []
Ulist = []
Utags = []

def AskQuestion(userQ):
    global index
    index = []
    global Ulist
    Ulist = []
    global Utags
    Utags = []
    tokens = tokenizer.tokenize(userQ.lower()) #making the entire string lower
    print(tokens)
    filtered_tokens = [w for w in tokens if not w in stopwords]  # filtering stopwords
    filtered_tokens = [spell(w) for w in filtered_tokens]
    filtered_tokens = [w for w in filtered_tokens if not w in stopwords]

    for w in filtered_tokens:
        if wn.synsets(w):
            Ulist.append(w)
            #list1.append([a.name() for a in wn.synsets(w)])
        else :
            #print("Tag: #{0}".format(w))
            #whether would towards everybody -- need to be removed
            # some weird words are not filtered through -> need to be hardcoded and removed
            if (w not in Ulist) and (w not in weird_words):
                Utags.append(w)

    score = []

    for i in range(1,len(data)):

        Qlist = data[str(i)]["Question_list"]
        Qtags = data[str(i)]["Tags"]

        #print("{0} \n {1} \n {2} \n {3}".format(Ulist,Qlist,Utags,Qtags))
        similarity = calc2(Ulist,Qlist,Utags,Qtags)
        #print("Final Score on Q{0} = {1}".format(i,similarity))
        score.append(similarity)

    index =  sorted(range(len(score)), key=lambda i: score[i],reverse = True)
    return_data = {}
    for i in index[:3]:

        return_data[str(i+1)] = {
        "Question" : data[str(i+1)]["Question "],
        "Answer" : data[str(i+1)]["Answer"]
        }

    return_data_json = json.dumps(return_data)

    return return_data_json

nah = ['no','not there','n',0,'N','No','NO','nah']

def Is_it_in_top_k(response):

    if(response not in nah):
        return 'success'

    global index
    print(index)
    # returning next 3
    return_data = {}
    for i in index[3:6]:

        return_data[str(i+1)] = {
        "Question" : data[str(i+1)]["Question "],
        "Answer" : data[str(i+1)]["Answer"]
        }

    return_data_json = json.dumps(return_data)

    return return_data_json

def Is_it_there_yet(response):

    if(response not in nah):

        # update here
        for i in Ulist:
            if i not in data[str(response)]["Question_list"]:
                data[str(response)]["Question_list"].append(i)

        for i in Utags:
            if i not in data[str(response)]["Tags"]:
                data[str(response)]["Tags"].append(i)

        with open('data_VIT_FAQ_reset_new.json', 'w') as outfile:
            json.dump(data, outfile,indent = 4)
        outfile.close()

        return 'success'

    else:

        return 'fail'


#-------------------------------------------------------------------------------
