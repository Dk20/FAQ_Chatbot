'''
PURPOSE : main script for Reimbursement FAQ
Author : Ink_feather
'''

import json
import sys
from similarity_calc import calc2

from autocorrect import spell   #this one takes a bit of time

from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn

tokenizer = RegexpTokenizer(r'\w+') #to remove punctuations
stopwords = stopwords.words("english") # to remove stopwords

with open('DATA/data_reimbursement.json') as json_:
    data = json.load(json_)
json_.close()



print("\n-----------------------WELCOME TO REIMBURSEMENT FAQ CHAT FOR ITC-----------------------\n")
print("I take k = 5 :P\n")
#k = int(input("Enter K for topK values :"))
k = 5
userQ = input("\nAsk a Question >")
#userQ = "Claim itc product for on line purchase?, whether,would,everybody,towards"


#---------------------------Tokenizing user input-------------------------------

weird_words = data["weird_words"] # these words are not defined in synset

tokens = tokenizer.tokenize(userQ.lower()) #making the entire string lower

print("Tokenized string : {0}".format(tokens))

filtered_tokens = [w for w in tokens if not w in stopwords]  # filtering stopwords

print("After stopword removal : {0}".format(filtered_tokens))

print("Checking for spelling errors ...")
filtered_tokens = [spell(w) for w in filtered_tokens]
print("Corrected/Understood Spellings : {0}".format(filtered_tokens))

Ulist = []
Utags = []

for w in filtered_tokens:
    if wn.synsets(w):
        Ulist.append(w)
        #list1.append([a.name() for a in wn.synsets(w)])
    else :
        print("Tag: #{0}".format(w))
        #whether would towards everybody -- need to be removed
        # some weird words are not filtered through -> need to be hardcoded and removed
        if (w not in Ulist) and (w not in weird_words):
            Utags.append(w)

print("Ulist: {0}\nUtags: {1}\n".format(Ulist,Utags))
#-------------------------------------------------------------------------------

# taking down weird tags....

print("Do you find tag list incorrect?")
ans_ = input("Ans in 'y' or 'n'>")

if ans_=='y' or ans_=='Y':

    print("\npray tell which to remove ...")
    for i in range(0,len(Utags)):
        print("{0} : {1}".format(i,Utags[i]))

    index_nos = []
    while True:
        ans_ = int(input("Enter index number (-1 to quit)>"))
        if ans_ == -1: break
        index_nos.append(Utags[ans_])

    print(index_nos)
    for i in index_nos:
        Utags.remove(i)
        print("deleted {0}...".format(i))

        data["weird_words"].append(i)
        print("Appending weird_words list...")

else:
    print("Thank you for your time. :)")

print("Utags : {0}".format(Utags))

#done taking down weird tags

#---------------------------main calculations-----------------------------------
score = []

for i in range(1,len(data)):

    Qlist = data[str(i)]["Question_list"]
    Qtags = data[str(i)]["Tags"]

    similarity = calc2(Ulist,Qlist,Utags,Qtags)
    print("Final Score on Q{0} = {1}".format(i,similarity))
    score.append(similarity)



index =  sorted(range(len(score)), key=lambda i: score[i],reverse = True)
#print(index)


print("------------------------Displaying top {0} Q/A-------------------------------"\
    .format(k))


for i in index[:k]:
    print("Q{0}) {1}\n\nAns.  {2}\n".format(i+1,data[str(i+1)]["Question "],\
    data[str(i+1)]["Answer"]))

#-------------------------------------------------------------------------------

#---------------------------Modify dataset incase incorrect TopK----------------

print("\n\nPlease check if relevant Q/A is given above (0 if none of them matched)")
q = int(input("If answer is there press 1 >"))

if q==0:

    print("\n ----Showing {0} to {1} questions in sorted order of \
        possible prefernce-----\n".format(k,k*2))

    for i in index[k:k*2]:
        print("Q{0}) {1}\n\nAns. {2}\n".format(i+1,data[str(i+1)]["Question "],data[str(i+1)]["Answer"]))


    print("\nEnter the Question number that was close to what you expect (0 if none of them matched)")
    print("\nSCROLL UP to check a Bit Please\n")
    q = int(input(">"))
    if q == 0:
        print("Sorry I can't help you! :(\n")
        sys.exit()

    print("\nThank you for your time :-)\nWe will be adding this query to our file!\n")

    #updating here
    for i in Ulist:
        if i not in data[str(q)]["Question_list"]:
            print("adding {0} to Q{1}\n".format(i,q))
            data[str(q)]["Question_list"].append(i)

    #print(json.dumps(data,indent = 4))

    for i in Utags:
        if i not in data[str(q)]["Tags"]:
            print("Do I add {0} to tags in Q{1}".format(i,q))
            add_ = input("ans in 'y' or 'n'>")
            if(add_ == 'y' or add_ == 'Y'):
                print("Okay!")
                data[str(q)]["Tags"].append(i)
            else:
                print("Thank you for pointing that out!")


else:
    print("Hope I was useful :)\n")

with open('DATA/data_reimbursement.json', 'w') as outfile:
    json.dump(data, outfile,indent = 4)

outfile.close()
#-------------------------------------------------------------------------------

print("-----------------------------BYE BYE------------------------------")
