from nltk.corpus import wordnet as wn
from itertools import product

def calc(a,b):      #uses synsets

    w1 = wn.synset(a)
    w2 = wn.synset(b)

    if w2.path_similarity(w1):
        v1 = w2.path_similarity(w1)
    else :
        v1 = 0

    if w1.path_similarity(w2):
        v2 = w1.path_similarity(w2)
    else :
        v2 = 0

    val = ( v1 + v2 )/2
    #print("Calc {0} and {1} = {2}".format(a,b,val))
    return val
    #return w1.path_similarity(w2)

def calc_syn(w1,w2):      #uses synsets


    if w2.path_similarity(w1):
        v1 = w2.path_similarity(w1)
    else :
        v1 = 0

    if w1.path_similarity(w2):
        v2 = w1.path_similarity(w2)
    else :
        v2 = 0

    val = ( v1 + v2 )/2
    #print("Calc {0} and {1} = {2}".format(a,b,val))
    return val

def calc2(Alist,Blist,tagsA,tagsB):     #uses strings as args not Synset

    score = 0
    for i in tagsA:
        if i in tagsB:
            score += 0.5
            print("Tag present : {0}".format(i))

    w_all_syn = []
    w_best_syn = []
    w_best_match = []

    for A in Alist:

        Aset = wn.synsets(A)
        w_best_syn = []

        for B in Blist:

            w_all_syn = []
            Bset = wn.synsets(B)
            for wa,wb in product(Aset,Bset):
                w_all_syn.append(calc_syn(wa,wb))

            max_w = max(w_all_syn)
            #print("Score b/w ({0},{1}) = {2}".format(A,B,max_w))
            w_best_syn.append(max_w)

        '''
        tricky stuff here, basically if there are more than 1 maximums
        match ,
        say U = ['hello'] and Q = ['hello','hello','hello']
        you, dont just want the max here...
        '''
        a= sum(w_best_syn)
        if a > 1.5:
            max_match = a
        else:
            max_match = max(w_best_syn)


        #print("Best matching words ({0},{1}) = {2}".format(A,B,max_match))
        w_best_match.append(max_match)

    #print("{0}\n".format(w_best_match))
    score += sum(w_best_match)/(len(Alist)*len(Blist))

    return score
