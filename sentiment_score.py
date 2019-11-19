''''
Created on November 17, 2019

@author : Svetlana Morozov
'''
import sys
import os
import csv
import pandas as pd
import nltk as nl
import re


path = "////Users//sveta//python//myTest//"

sent_file = path + "AFINN-111.txt"

#nl.download()
st = nl.LancasterStemmer()
#ps = nl.PorterStemmer()
#lemma = nl.wordnet.WordNetLemmatizer()
#sno = nl.stem.SnowballStemmer('english')
#lemma.lemmatize('article')


def dictRead(file):
    arr=[]
    mycommand = "perl -p -i.back -e 's/\t/\,/g'"
    cmd = mycommand+' '+file
    os.system(cmd)

    hm = {}
    with open(file, 'rU') as infile:
        reader = csv.reader(infile)
        for row in reader:

            key = row[0].strip("'")
            value = int(row[1])


            arr.append(row)
            hm[key] = value


    return hm




def sentiment_score(news_text,sent_dict):


    excludelist = ['.','(',')','','i','am','my','was','but','also','get','have','using','take','not','all','who','use', 'well','&','     ','-','at','job','we','from','this','their','by','about','an','us','more','be','our','into','years','such','in','of', 'a','the', 'is','are','to','that','or','on','as', 'you','will', 'with','for','like','and','your','if','etc','plus' ]

    news_text = re.sub('\W+',' ', news_text )

    
    i = 0
    for txt in [news_text]:

        sum_rnk = 0
        i = i+1

        list1 = txt.split(" ")

        for w in list1:

            word = w.lower().strip(' \t\n\r')


            if word not in excludelist:


                #word_root = lemma.lemmatize(word,'v')
                #word_root = sno.stem(word)
                #word_root=st.stem(word)

                word_root= word

                if  word_root in sent_dict:
                    rnk = int(sent_dict[word_root])
                else:
                    rnk = 0
                sum_rnk = sum_rnk + rnk

    rank = sum_rnk
    return rank


def init_sentiment():

    sent_map = dictRead(sent_file)
    return sent_map


def test():
    sent_map = init_sentiment()

    s1 = 'U.S. stock futures declined after the monthly jobs report -- released during a holiday-shortened trading session for futures -- came in much weaker than expected.'

    rank = sentiment_score(s1,sent_map)
    print (rank)


if __name__ ==  '__main__':
    test()

